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
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame
from python_on_whales import docker
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import new_temp_dir
from src.python.review.run_tool import positive_int

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def configure_arguments(parser: ArgumentParser) -> None:
    parser.add_argument("dataset_path", type=lambda value: Path(value).absolute(), help="Path to dataset")  # TODO

    parser.add_argument(
        "inspections_output",
        type=lambda value: Path(value).absolute(),
        help="The path where the id of the inspections will be saved",
    )

    parser.add_argument("-c", "--config", type=lambda value: Path(value).absolute(), help="Path to qodana.yaml")  # TODO

    parser.add_argument("-l", "--limit", type=positive_int, help="dataset head limit. ONLY FOR DEBUG")  # TODO

    parser.add_argument("-s", "--chunk-size", type=positive_int, help="The size of the chunk")  # TODO

    parser.add_argument(
        "-o",
        "--dataset-output",
        type=lambda value: Path(value).absolute(),
        help="The path where the tagged dataset will be saved. "
             "If not specified, the original dataset will be overwritten",
    )  # TODO


@dataclass(init=False)
class InspectionData:
    package: str

    def __init__(self, package: str, **kwargs: Any):
        self.package = package

    def __str__(self):
        return self.package


IGNORE = [LanguageVersion.KOTLIN.value, LanguageVersion.PYTHON_3.value]


class DatasetMarker:
    dataset_path: Path
    config: Optional[Path]
    limit: Optional[int]
    chunk_size: Optional[int]
    inspection_to_id: Dict[str, int]
    dataset_output: Path
    inspections_output: Path

    def __init__(self, args: Namespace):
        self.dataset_path = args.dataset_path
        self.config = args.config
        self.limit = args.limit
        self.chunk_size = args.chunk_size

        self.dataset_output = self.dataset_path
        if args.dataset_output is not None:
            self.dataset_output = args.dataset_output

        self.inspections_output = args.inspections_output

        self.inspection_to_id = {}

    def mark(self):
        df = pd.read_csv(self.dataset_path, index_col="id", nrows=self.limit)

        grouped_df = df.groupby("lang")
        unique_languages = df["lang"].unique()

        logger.info(f"Unique languages: {unique_languages}")

        groups = []
        for language in unique_languages:
            lang_df = grouped_df.get_group(language)

            if language in LanguageVersion.values() and language not in IGNORE:
                logger.info(f"Processing the language: {language}")
                groups.append(self._mark_language(lang_df, LanguageVersion(language)))
            else:
                logger.warning(f"Unknown language: {language}")
                groups.append(lang_df)

        logger.info("Dataset processing finished")

        result = pd.concat(groups)

        logger.info("Writing the dataset to a file.")
        result.to_csv(self.dataset_output)

        id_to_inspection = {value: index for index, value in self.inspection_to_id.items()}
        id_to_inspection_df = pd.DataFrame.from_dict(id_to_inspection, "index")
        id_to_inspection_df.index.name = "id"
        id_to_inspection_df.columns = ["inspection"]
        id_to_inspection_df.to_csv(self.inspections_output)
        print(self.inspection_to_id)
        print(id_to_inspection)

    def _mark_language(self, df: DataFrame, language: LanguageVersion):
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

    def _mark_chunk(self, chunk: DataFrame, language: LanguageVersion):
        with new_temp_dir() as temp_dir:
            logger.info("Copying the template")
            self._copy_template(temp_dir, language)

            if self.config:
                logger.info("Copying the config")
                self._copy_config(temp_dir)

            logger.info("Creating main files")
            self._create_main_files(temp_dir, chunk, language)

            logger.info("Running qodana")
            self._run_qodana(temp_dir)

            logger.info("Getting unique inspections")
            inspections = self._get_inspections(temp_dir)
            existing_inspections = set(self.inspection_to_id.keys())
            new_inspections = inspections.difference(existing_inspections)

            for inspection in new_inspections:
                self.inspection_to_id[inspection] = len(self.inspection_to_id)

            logger.info("Parsing the output of qodana")
            student_id_to_inspection_ids = self._parse(temp_dir, inspections)
            chunk["inspection_ids"] = ""
            for student_id, inspection_ids in student_id_to_inspection_ids.items():
                chunk.loc[student_id, "inspection_ids"] = ",".join(map(str, inspection_ids))

    @staticmethod
    def _copy_template(temp_dir: Path, language: LanguageVersion):
        if (
                language == LanguageVersion.JAVA_11
                or language == LanguageVersion.JAVA_9
                or language == LanguageVersion.JAVA_8
                or language == LanguageVersion.JAVA_7
        ):
            shutil.copytree(Path("./project_templates/java"), temp_dir, dirs_exist_ok=True)
        else:
            logger.warning(f"{language} is not supported yet")

    def _copy_config(self, temp_dir: Path):
        shutil.copy(self.config, temp_dir)

    @staticmethod
    def _create_main_files(temp_dir: Path, chunk: DataFrame, language: LanguageVersion):
        if (
                language == LanguageVersion.JAVA_11
                or language == LanguageVersion.JAVA_9
                or language == LanguageVersion.JAVA_8
                or language == LanguageVersion.JAVA_7
        ):
            (temp_dir / "results").mkdir()
            dist_path = temp_dir / "src" / "main" / "java"
            for index, row in chunk.iterrows():
                directory = dist_path / f"student{index}"
                directory.mkdir(parents=True)
                file_path = directory / "Main.java"
                with open(file_path, "w") as file:
                    file.write(f"package student{index};\n\n")
                    file.write(row["code"])
        else:
            logger.warning(f"{language} is not supported yet")

    @staticmethod
    def _run_qodana(temp_dir: Path):
        docker.run(
            "jetbrains/qodana",
            remove=True,
            volumes=[(temp_dir, "/data/project/"), ((temp_dir / "results/"), "/data/results/")],
            user=os.getuid(),
        )

    @staticmethod
    def _get_inspections(temp_dir: Path) -> set[str]:
        results_dir = temp_dir / "results"
        files = os.listdir(results_dir)

        file_name_regex = re.compile(r"(\w*).json")
        inspection_files = filter(lambda file: file_name_regex.match(file), files)

        return {file_name_regex.match(file).group(1) for file in inspection_files}

    def _parse(self, temp_dir: Path, inspections: set[str]):
        results_dir = temp_dir / "results"
        package_regex = re.compile(r"student(\d*)")

        student_id_to_inspections_ids = defaultdict(list)
        for inspection in inspections:
            inspection_id = self.inspection_to_id[inspection]
            file_path = results_dir / f"{inspection}.json"

            with open(file_path) as file:
                inspection_json = json.load(file)

            problems = inspection_json["problems"]
            for problem_data in problems:
                data = InspectionData(**problem_data)
                student_match = package_regex.match(data.package)
                if student_match:
                    student_id = int(student_match.group(1))
                    student_id_to_inspections_ids[student_id].append(inspection_id)

        return student_id_to_inspections_ids


def main():
    parser = ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        dm = DatasetMarker(args)
        dm.mark()

    except Exception:
        traceback.print_exc()
        logger.exception("An unexpected error")
        return 2


if __name__ == "__main__":
    sys.exit(main())
