import json
import logging
import os
import re
import shutil
import sys
import traceback
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Any, Dict, Optional, Set, List

from src.python.evaluation.qodana.util.qoadana_issue import QodanaIssue

sys.path.append("../../../..")

import numpy as np
import pandas as pd
from pandas import DataFrame
from python_on_whales import docker
from src.python.evaluation.common.util import ColumnName
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import new_temp_dir
from src.python.review.run_tool import positive_int

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def configure_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "dataset_path",
        type=lambda value: Path(value).absolute(),
        help=f"Dataset path. The dataset must contain at least three columns: '{ColumnName.ID.value}', "
             f"'{ColumnName.CODE.value}' and '{ColumnName.LANG.value}', where '{ColumnName.ID.value}' is a unique "
             f"solution number, '{ColumnName.LANG.value}' is the language in which the code is written in the "
             f"'{ColumnName.CODE.value}' column. The '{ColumnName.LANG.value}' must belong to one of the following "
             f"values: {', '.join(LanguageVersion.values())}. "
             f"If '{ColumnName.LANG.value}' is not equal to any of the values, the row will be skipped.",
    )

    parser.add_argument(
        "inspections_output_path",
        type=lambda value: Path(value).absolute(),
        help="Path where id of all found inspections will be saved.",
    )

    parser.add_argument("-c", "--config", type=lambda value: Path(value).absolute(), help="Path to qodana.yaml")

    parser.add_argument(
        "-l",
        "--limit",
        type=positive_int,
        help="Allows you to read only the specified number of first rows from the dataset.",
    )

    parser.add_argument(
        "-s",
        "--chunk-size",
        type=positive_int,
        help="The number of files that qodana will process at a time.",
        default=5000,
    )

    parser.add_argument(
        "-o",
        "--dataset-output-path",
        type=lambda value: Path(value).absolute(),
        help="The path where the marked dataset will be saved. "
             "If not specified, the original dataset will be overwritten.",
    )


@dataclass(init=False)
class InspectionData:
    package: str

    def __init__(self, package: str, **kwargs: Any):
        self.package = package

    def __str__(self):
        return self.package


class DatasetMarker:
    dataset_path: Path
    config: Optional[Path]
    limit: Optional[int]
    chunk_size: Optional[int]
    inspection_to_id: Dict[str, int]
    dataset_output_path: Path
    inspections_output_path: Path

    def __init__(self, args: Namespace):
        self.dataset_path = args.dataset_path
        self.config = args.config
        self.limit = args.limit
        self.chunk_size = args.chunk_size

        self.dataset_output_path = self.dataset_path
        if args.dataset_output_path is not None:
            self.dataset_output_path = args.dataset_output_path

        self.inspections_output_path = args.inspections_output_path

        self.inspection_to_id = {}

    def mark(self):
        df = pd.read_csv(self.dataset_path, index_col=ColumnName.ID.value, nrows=self.limit)

        group_by_lang = df.groupby(ColumnName.LANG.value)
        unique_languages = df[ColumnName.LANG.value].unique()

        logger.info(f"Unique languages: {unique_languages}")

        groups = []
        for language in unique_languages:
            lang_group = group_by_lang.get_group(language)

            if language in LanguageVersion.values():
                try:
                    logger.info(f"Processing the language: {language}")
                    groups.append(self._mark_language(lang_group, LanguageVersion(language)))
                except NotImplementedError:
                    logger.warning(f"{language} needs implementation")
                    groups.append(lang_group)
            else:
                logger.warning(f"Unknown language: {language}")
                groups.append(lang_group)

        logger.info("Dataset processing finished")

        df = pd.concat(groups)

        logger.info("Writing the dataset to a file.")
        df.to_csv(self.dataset_output_path)

        id_to_inspection = {value: index for index, value in self.inspection_to_id.items()}

        id_to_inspection_df = pd.DataFrame.from_dict(id_to_inspection, orient="index", columns=["inspection"])
        id_to_inspection_df.index.name = "id"
        id_to_inspection_df.to_csv(self.inspections_output_path)

    def _mark_language(self, df: DataFrame, language: LanguageVersion) -> DataFrame:
        number_of_chunks = 1
        if self.chunk_size is not None:
            number_of_chunks = ceil(df.shape[0] / self.chunk_size)

        chunks = np.array_split(df, number_of_chunks)
        for index, chunk in enumerate(chunks):
            logger.info(f"Processing chunk: {index + 1} / {number_of_chunks}")
            self._mark_chunk(chunk, language)

        logger.info(f"{language} processing finished.")
        result = pd.concat(chunks)
        return result

    @classmethod
    def _get_fragment_id_from_fragment_file_path(cls, fragment_file_path: str) -> int:
        pass

    @classmethod
    def _parse_inspections_files(cls, inspections_files: List[Path]):
        for file in inspections_files:
            issues = json.loads(str(file))['problems']
            for issue in issues:
                qodana_issue = QodanaIssue(line=issue['line'], offset=issue['offset'], length=issue['length'],
                                           highlighted_element=issue['highlighted_element'],
                                           description=issue['description'])
            pass
        pass

    def _mark_chunk(self, chunk: DataFrame, language: LanguageVersion):
        with new_temp_dir() as temp_dir:
            project_dir = temp_dir / "project"
            results_dir = temp_dir / "results"

            logger.info("Copying the template")
            self._copy_template(project_dir, language)

            if self.config:
                logger.info("Copying the config")
                self._copy_config(project_dir)

            logger.info("Creating main files")
            self._create_main_files(project_dir, chunk, language)

            logger.info("Running qodana")
            self._run_qodana(project_dir, results_dir)

            logger.info("Getting unique inspections")
            inspections = self._get_inspections_files(results_dir)

            # Todo: open all jsons and parse inspections

            existing_inspections = set(self.inspection_to_id.keys())
            new_inspections = inspections.difference(existing_inspections)

            for inspection in new_inspections:
                self.inspection_to_id[inspection] = len(self.inspection_to_id)

            logger.info("Parsing the output of qodana")
            solution_id_to_inspection_ids = self._parse(results_dir, inspections)
            chunk["inspection_ids"] = ""
            for solution_id, inspection_ids in solution_id_to_inspection_ids.items():
                chunk.loc[solution_id, "inspection_ids"] = ",".join(map(str, inspection_ids))

    @staticmethod
    def _copy_template(project_dir: Path, language: LanguageVersion):
        if (
                language == LanguageVersion.JAVA_11
                or language == LanguageVersion.JAVA_9
                or language == LanguageVersion.JAVA_8
                or language == LanguageVersion.JAVA_7
        ):
            shutil.copytree(Path("./project_templates/java"), project_dir, dirs_exist_ok=True)
        else:
            raise NotImplementedError

    def _copy_config(self, project_dir: Path):
        shutil.copy(self.config, project_dir)

    @staticmethod
    def _create_main_files(project_dir: Path, chunk: DataFrame, language: LanguageVersion):
        if (
                language == LanguageVersion.JAVA_11
                or language == LanguageVersion.JAVA_9
                or language == LanguageVersion.JAVA_8
                or language == LanguageVersion.JAVA_7
        ):
            working_dir = project_dir / "src" / "main" / "java"
            for index, row in chunk.iterrows():
                solution_dir = working_dir / f"solution{index}"
                solution_dir.mkdir(parents=True)
                file_path = solution_dir / "Main.java"
                with open(file_path, "w") as file:
                    file.write(f"package solution{index};\n\n")
                    file.write(row[ColumnName.CODE.value])
        else:
            raise NotImplementedError

    @staticmethod
    def _run_qodana(project_dir: Path, results_dir: Path):
        results_dir.mkdir()

        docker.run(
            "jetbrains/qodana",
            remove=True,
            volumes=[(project_dir, "/data/project/"), (results_dir, "/data/results/")],
            user=os.getuid(),
        )

    @staticmethod
    def _get_inspections_files(results_dir: Path) -> Set[Path]:
        files = os.listdir(results_dir)

        file_name_regex = re.compile(r"(\w*).json")
        return set(map(lambda f: results_dir / f, filter(lambda file: file_name_regex.match(file), files)))

    def _parse(self, results_dir: Path, inspections: Set[str]):
        package_regex = re.compile(r"solution(\d*)")

        solution_id_to_inspections_ids = defaultdict(list)
        for inspection in inspections:
            inspection_id = self.inspection_to_id[inspection]
            inspection_file_path = results_dir / f"{inspection}.json"

            with open(inspection_file_path) as file:
                inspection_json = json.load(file)

            problems = inspection_json["problems"]
            for problem in problems:
                data = InspectionData(**problem)
                package_match = package_regex.match(data.package)
                if package_match:
                    solution_id = int(package_match.group(1))
                    solution_id_to_inspections_ids[solution_id].append(inspection_id)

        return solution_id_to_inspections_ids


def main():
    parser = ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        marker = DatasetMarker(args)
        marker.mark()

    except Exception:
        traceback.print_exc()
        logger.exception("An unexpected error")
        return 2


if __name__ == "__main__":
    sys.exit(main())
