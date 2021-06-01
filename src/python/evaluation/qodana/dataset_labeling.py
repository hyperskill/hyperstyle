import json
import logging
import os
import re
import sys
import traceback
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from math import ceil
from pathlib import Path
from typing import Dict, List, Optional

sys.path.append('../../../..')

import numpy as np
import pandas as pd
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue
from src.python.evaluation.qodana.util.util import to_json
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import (
    copy_directory,
    copy_file,
    create_directory,
    create_file,
    Extension,
    get_all_file_system_items,
    get_content_from_file,
    get_name_from_path,
    get_parent_folder,
    match_condition,
    remove_directory,
)
from src.python.review.common.subprocess_runner import run_and_wait
from src.python.review.run_tool import positive_int

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TEMPLATE_FOLDER = Path(__file__).parents[3] / 'resources' / 'evaluation' / 'qodana' / 'project_templates'


def configure_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        'dataset_path',
        type=lambda value: Path(value).absolute(),
        help=f"Dataset path. The dataset must contain at least three columns: '{ColumnName.ID.value}', "
             f"'{ColumnName.CODE.value}' and '{ColumnName.LANG.value}', where '{ColumnName.ID.value}' is a unique "
             f"solution number, '{ColumnName.LANG.value}' is the language in which the code is written in the "
             f"'{ColumnName.CODE.value}' column. The '{ColumnName.LANG.value}' must belong to one of the following "
             f"values: {', '.join(LanguageVersion.values())}. "
             f"If '{ColumnName.LANG.value}' is not equal to any of the values, the row will be skipped.",
    )

    parser.add_argument('-c', '--config', type=lambda value: Path(value).absolute(), help='Path to qodana.yaml')

    parser.add_argument(
        '-l',
        '--limit',
        type=positive_int,
        help='Allows you to read only the specified number of first rows from the dataset.',
    )

    parser.add_argument(
        '-s',
        '--chunk-size',
        type=positive_int,
        help='The number of files that qodana will process at a time.',
        default=5000,
    )

    parser.add_argument(
        '-o',
        '--output-path',
        type=lambda value: Path(value).absolute(),
        help='The path where the labeled dataset will be saved. '
             'If not specified, the labeled dataset will be saved next to the original one.',
    )


class DatasetLabel:
    """
    DatasetLabel allows you to label a dataset using the found Qodana inspections.
    Accepts dataset_path, config, limit, chunk_size and output_path.
    """

    dataset_path: Path
    config: Optional[Path]
    limit: Optional[int]
    chunk_size: Optional[int]
    inspection_to_id: Dict[str, int]
    output_path: Path

    def __init__(self, args: Namespace):
        self.dataset_path = args.dataset_path
        self.config = args.config
        self.limit = args.limit
        self.chunk_size = args.chunk_size

        self.output_path = args.output_path
        if self.output_path is None:
            output_dir = get_parent_folder(self.dataset_path)
            dataset_name = get_name_from_path(self.dataset_path)
            self.output_path = output_dir / f'labeled_{dataset_name}'

    def label(self) -> None:
        """
        Runs Qodana on each row of the dataset and writes the found inspections in the 'inspections' column.
        """
        dataset = pd.read_csv(self.dataset_path, nrows=self.limit)

        group_by_lang = dataset.groupby(ColumnName.LANG.value)
        unique_languages = dataset[ColumnName.LANG.value].unique()

        logger.info(f'Unique languages: {unique_languages}')

        groups = []
        for language in unique_languages:
            lang_group = group_by_lang.get_group(language)

            if language in LanguageVersion.values():
                # TODO: languages need implementation
                try:
                    logger.info(f'Processing the language: {language}')
                    groups.append(self._label_language(lang_group, LanguageVersion(language)))
                except NotImplementedError:
                    # If we find a language that is in the LanguageVersion,
                    # but is not supported in this script, we should skip this fragment.
                    logger.warning(f'{language} needs implementation')
                    groups.append(lang_group)
            else:
                logger.warning(f'Unknown language: {language}')
                groups.append(lang_group)

        logger.info('Dataset processing finished')

        dataset = pd.concat(groups)

        logger.info('Writing the dataset to a file.')
        write_dataframe_to_csv(self.output_path, dataset)

    def _label_language(self, df: pd.DataFrame, language: LanguageVersion) -> pd.DataFrame:
        number_of_chunks = 1
        if self.chunk_size is not None:
            number_of_chunks = ceil(df.shape[0] / self.chunk_size)

        chunks = np.array_split(df, number_of_chunks)
        labeled_chunks = []
        # Todo: run this in parallel
        for index, chunk in enumerate(chunks):
            logger.info(f'Processing chunk: {index + 1} / {number_of_chunks}')
            labeled_chunks.append(self._label_chunk(chunk, language, index))

        logger.info(f'{language} processing finished.')
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
    def _parse_inspections_files(cls, inspections_files: List[Path]) -> Dict[int, List[QodanaIssue]]:
        id_to_issues: Dict[int, List[QodanaIssue]] = defaultdict(list)
        for file in inspections_files:
            issues = json.loads(get_content_from_file(file))['problems']
            for issue in issues:
                fragment_id = int(cls._get_fragment_id_from_fragment_file_path(issue['file']))
                qodana_issue = QodanaIssue(
                    line=issue['line'],
                    offset=issue['offset'],
                    length=issue['length'],
                    highlighted_element=issue['highlighted_element'],
                    description=issue['description'],
                    fragment_id=fragment_id,
                    problem_id=issue['problem_class']['id'],
                )
                id_to_issues[fragment_id].append(qodana_issue)
        return id_to_issues

    def _label_chunk(self, chunk: pd.DataFrame, language: LanguageVersion, chunk_id: int) -> pd.DataFrame:
        tmp_dir_path = self.dataset_path.parent.absolute() / f'qodana_project_{chunk_id}'
        create_directory(tmp_dir_path)

        project_dir = tmp_dir_path / 'project'
        results_dir = tmp_dir_path / 'results'

        logger.info('Copying the template')
        self._copy_template(project_dir, language)

        if self.config:
            logger.info('Copying the config')
            copy_file(self.config, project_dir)

        logger.info('Creating main files')
        self._create_main_files(project_dir, chunk, language)

        logger.info('Running qodana')
        self._run_qodana(project_dir, results_dir)

        logger.info('Getting inspections')
        inspections_files = self._get_inspections_files(results_dir)
        inspections = self._parse_inspections_files(inspections_files)

        logger.info('Write inspections')
        chunk[QodanaColumnName.INSPECTIONS.value] = chunk.apply(
            lambda row: to_json(inspections.get(row[ColumnName.ID.value], [])), axis=1,
        )

        remove_directory(tmp_dir_path)
        return chunk

    @staticmethod
    def _copy_template(project_dir: Path, language: LanguageVersion) -> None:
        if language.is_java():
            java_template = TEMPLATE_FOLDER / "java"
            copy_directory(java_template, project_dir)
        else:
            raise NotImplementedError(f'{language} needs implementation.')

    def _create_main_files(self, project_dir: Path, chunk: pd.DataFrame, language: LanguageVersion) -> None:
        if language.is_java():
            working_dir = project_dir / 'src' / 'main' / 'java'

            chunk.apply(
                lambda row: next(
                    create_file(
                        file_path=(working_dir / f'solution{row[ColumnName.ID.value]}' / f'Main{Extension.JAVA.value}'),
                        content=row[ColumnName.CODE.value],
                    ),
                ),
                axis=1,
            )
        else:
            raise NotImplementedError(f'{language} needs implementation.')

    @staticmethod
    def _run_qodana(project_dir: Path, results_dir: Path) -> None:
        results_dir.mkdir()
        command = [
            'docker', 'run',
            '-u', str(os.getuid()),
            '--rm',
            '-v', f'{project_dir}/:/data/project/',
            '-v', f'{results_dir}/:/data/results/',
            'jetbrains/qodana',
        ]
        run_and_wait(command)

    @staticmethod
    def _get_inspections_files(results_dir: Path) -> List[Path]:
        condition = match_condition(r'\w*.json')
        return get_all_file_system_items(results_dir, condition, without_subdirs=True)


def main():
    parser = ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        dataset_label = DatasetLabel(args)
        dataset_label.label()

    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error')
        return 2


if __name__ == '__main__':
    sys.exit(main())
