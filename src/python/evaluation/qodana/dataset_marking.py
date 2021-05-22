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
from typing import Any, Dict, List, Optional, Set

sys.path.append("../../../..")

import numpy as np
import pandas as pd
from pandas import DataFrame
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue, QodanaJsonField
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import (
    create_directory, get_content_from_file, get_name_from_path, get_parent_folder, remove_directory, remove_slash,
)
from src.python.review.common.subprocess_runner import run_and_wait
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

    def mark(self):
        df = pd.read_csv(self.dataset_path, nrows=self.limit)

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
        write_dataframe_to_csv(self.dataset_output_path, df)

    def _mark_language(self, df: DataFrame, language: LanguageVersion) -> DataFrame:
        number_of_chunks = 1
        if self.chunk_size is not None:
            number_of_chunks = ceil(df.shape[0] / self.chunk_size)

        chunks = np.array_split(df, number_of_chunks)
        labeled_chunks = []
        # Todo: run this in parallel
        for index, chunk in enumerate(chunks):
            logger.info(f"Processing chunk: {index + 1} / {number_of_chunks}")
            labeled_chunks.append(self._mark_chunk(chunk, language, index))

        logger.info(f"{language} processing finished.")
        result = pd.concat(labeled_chunks)
        return result

    @classmethod
    def _extract_fragment_id(cls, folder_name: str) -> int:
        numbers = re.findall(r'\d+', folder_name)
        if len(numbers) != 1:
            raise ValueError(f'Can not extract fragment id from {folder_name}')
        return numbers[0]

    @classmethod
    def _get_fragment_id_from_fragment_file_path(cls, fragment_file_path: str) -> int:
        folder_name = get_name_from_path(get_parent_folder(fragment_file_path), with_extension=False)
        return cls._extract_fragment_id(folder_name)

    @classmethod
    def _parse_inspections_files(cls, inspections_files: Set[Path]) -> Dict[int, List[QodanaIssue]]:
        id_to_issues: Dict[int, List[QodanaIssue]] = defaultdict(list)
        for file in inspections_files:
            issues = json.loads(get_content_from_file(file))['problems']
            for issue in issues:
                fragment_id = int(cls._get_fragment_id_from_fragment_file_path(issue['file']))
                qodana_issue = QodanaIssue(line=issue['line'], offset=issue['offset'], length=issue['length'],
                                           highlighted_element=issue['highlighted_element'],
                                           description=issue['description'], fragment_id=fragment_id,
                                           problem_id=issue['problem_class']['id'])
                id_to_issues[fragment_id].append(qodana_issue)
        return id_to_issues

    @classmethod
    def _to_json(cls, issues: List[QodanaIssue]) -> str:
        issues_json = {
            QodanaJsonField.ISSUES.value: list(map(lambda i: i.to_json(), issues)),
        }
        return json.dumps(issues_json)

    def _mark_chunk(self, chunk: DataFrame, language: LanguageVersion, chunk_id: int) -> pd.DataFrame:
        tmp_dir_path = self.dataset_path.parent.absolute() / f'qodana_project_{chunk_id}'
        create_directory(tmp_dir_path)

        project_dir = tmp_dir_path / "project"
        results_dir = tmp_dir_path / "results"

        logger.info("Copying the template")
        self._copy_template(project_dir, language)

        if self.config:
            logger.info("Copying the config")
            self._copy_config(project_dir)

        logger.info("Creating main files")
        self._create_main_files(project_dir, chunk, language)

        logger.info("Running qodana")
        self._run_qodana(project_dir, results_dir)

        logger.info("Getting inspections")
        inspections_files = self._get_inspections_files(results_dir)
        inspections = self._parse_inspections_files(inspections_files)

        logger.info("Write inspections")
        chunk[QodanaColumnName.INSPECTIONS.value] = chunk.apply(
            lambda row: self._to_json(inspections.get(row[ColumnName.ID.value], [])), axis=1)

        remove_directory(tmp_dir_path)
        return chunk

    @staticmethod
    def _copy_template(project_dir: Path, language: LanguageVersion):
        if (
                language == LanguageVersion.JAVA_11
                or language == LanguageVersion.JAVA_9
                or language == LanguageVersion.JAVA_8
                or language == LanguageVersion.JAVA_7
        ):
            shutil.copytree(Path(f"{remove_slash(os.path.dirname(os.path.abspath(__file__)))}/project_templates/java"),
                            project_dir, dirs_exist_ok=True)
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
            for _, row in chunk.iterrows():
                solution_dir = working_dir / f"solution{row[ColumnName.ID.value]}"
                solution_dir.mkdir(parents=True)
                file_path = solution_dir / "Main.java"
                with open(file_path, "w") as file:
                    file.write(f"package solution{row[ColumnName.ID.value]};\n\n")
                    file.write(row[ColumnName.CODE.value])
        else:
            raise NotImplementedError

    @staticmethod
    def _run_qodana(project_dir: Path, results_dir: Path):
        results_dir.mkdir()
        command = ['docker', 'run', '-u', str(os.getuid()), '--rm', '-v', f'{project_dir}/:/data/project/', '-v',
                   f'{results_dir}/:/data/results/', 'jetbrains/qodana']
        run_and_wait(command)

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
