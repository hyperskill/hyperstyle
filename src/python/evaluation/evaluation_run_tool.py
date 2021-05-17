import argparse
import logging.config
import os
import re
import sys
import traceback
from pathlib import Path
from typing import Type

from src.python.evaluation.common.csv_util import write_dataframe_to_csv

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.util import ColumnName, EvaluationArgument, script_structure_rule
from src.python.evaluation.common.xlsx_util import (
    create_and_get_workbook_path,
    remove_sheet,
    write_dataframe_to_xlsx_sheet,
)
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import create_file, Extension
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser, run_tool_arguments: Type[RunToolArgument]) -> None:
    parser.add_argument('solutions_file_path',
                        type=lambda value: Path(value).absolute(),
                        help='Local XLSX-file or CSV-file path. '
                             'Your file must include column-names: '
                             f'"{ColumnName.CODE.value}" and '
                             f'"{ColumnName.LANG.value}". Acceptable values for '
                             f'"{ColumnName.LANG.value}" column are: '
                             f'{LanguageVersion.PYTHON_3.value}, {LanguageVersion.JAVA_8.value}, '
                             f'{LanguageVersion.JAVA_11.value}, {LanguageVersion.KOTLIN.value}.')

    parser.add_argument('-tp', '--tool-path',
                        default=Path('src/python/review/run_tool.py').absolute(),
                        type=lambda value: Path(value).absolute(),
                        help='Path to script to run on files.')

    parser.add_argument('-tr', '--traceback',
                        help='If True, column with the full inspector feedback will be added '
                             'to the output file with results.',
                        action='store_true')

    parser.add_argument('-ofp', '--output-folder-path',
                        help='An absolute path to the folder where file with evaluation results'
                             'will be stored.'
                             'Default is the path to a directory, where is the folder with xlsx or csv file.',
                        # if None default path will be specified based on xlsx_file_path.
                        default=None,
                        type=str)

    parser.add_argument('-ofn', '--output-file-name',
                        help='Filename for that will be created to store inspection results.'
                             f'Default is "{EvaluationArgument.RESULT_FILE_NAME_XLSX.value}"',
                        default=f'{EvaluationArgument.RESULT_FILE_NAME_XLSX.value}',
                        type=str)

    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=f'{run_tool_arguments.FORMAT.value.description}'
                             f'Use this argument when {EvaluationArgument.TRACEBACK.value} argument'
                             'is enabled argument will not be used otherwise.')


def get_language(lang_key: str) -> LanguageVersion:
    try:
        return LanguageVersion(lang_key)
    except ValueError as e:
        logger.error(script_structure_rule)
        # We should raise KeyError since it is incorrect value for key in a column
        raise KeyError(e)


def inspect_solutions_df(config: EvaluationConfig, inspect_solutions_df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame(
        {
            ColumnName.LANGUAGE.value: [],
            ColumnName.CODE.value: [],
            ColumnName.GRADE.value: [],
        },
    )

    if config.traceback:
        report[EvaluationArgument.TRACEBACK.value] = []

    try:
        for lang, code in zip(inspect_solutions_df[ColumnName.LANG.value],
                              inspect_solutions_df[ColumnName.CODE.value]):

            # Tool does not work correctly with tmp files from <tempfile> module on macOS
            # thus we create a real file in the file system
            extension = get_language(lang).extension_by_language().value
            tmp_file_path = config.solutions_file_path.parent.absolute() / f'inspected_code{extension}'
            temp_file = next(create_file(tmp_file_path, code))

            command = config.build_command(temp_file, lang)
            results = run_in_subprocess(command)
            os.remove(temp_file)

            # this regular expression matches final tool grade: EXCELLENT, GOOD, MODERATE or BAD
            grades = re.match(r'^.*{"code":\s"([A-Z]+)"', results).group(1)
            output_row_values = [lang, code, grades]
            column_indices = [ColumnName.LANGUAGE.value,
                              ColumnName.CODE.value,
                              ColumnName.GRADE.value]

            if config.traceback:
                output_row_values.append(results)
                column_indices.append(EvaluationArgument.TRACEBACK.value)

            new_file_report_row = pd.Series(data=output_row_values, index=column_indices)
            report = report.append(new_file_report_row, ignore_index=True)

        return report

    except KeyError as e:
        logger.error(script_structure_rule)
        raise e

    except Exception as e:
        traceback.print_exc()
        logger.exception('An unexpected error.')
        raise e


def get_solutions_df(config: EvaluationConfig) -> pd.DataFrame:
    try:
        if config.extension == Extension.XLSX:
            lang_code_dataframe = pd.read_excel(config.solutions_file_path)
        else:
            lang_code_dataframe = pd.read_csv(config.solutions_file_path)
    except FileNotFoundError as e:
        logger.error('XLSX-file or CSV-file with the specified name does not exists.')
        raise e

    return lang_code_dataframe


def write_df_to_file(df: pd.DataFrame, config: EvaluationConfig) -> None:
    if config.extension == Extension.CSV:
        write_dataframe_to_csv(config.get_output_file_path(), df)
    elif config.extension == Extension.XLSX:
        workbook_path = create_and_get_workbook_path(config)
        write_dataframe_to_xlsx_sheet(workbook_path, df, 'inspection_results')
        # remove empty sheet that was initially created with the workbook
        remove_sheet(workbook_path, 'Sheet')


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser, RunToolArgument)

    try:
        args = parser.parse_args()
        config = EvaluationConfig(args)
        lang_code_dataframe = get_solutions_df(config)
        results = inspect_solutions_df(config, lang_code_dataframe)
        write_df_to_file(results, config)
        return 0

    except FileNotFoundError:
        logger.error('XLSX-file or CSV-file with the specified name does not exists.')
        return 2

    except KeyError:
        logger.error(script_structure_rule)
        return 2

    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
