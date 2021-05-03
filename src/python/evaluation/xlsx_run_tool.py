import argparse
import enum
import logging.config
import os
import re
import sys
import traceback
from pathlib import Path

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
from src.python.review.common.file_system import create_file, new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser, run_tool_arguments: enum.EnumMeta) -> None:
    parser.add_argument('xlsx_file_path',
                        type=lambda value: Path(value).absolute(),
                        help='Local XLSX-file path. '
                             'Your XLSX-file must include column-names: '
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
                             'Default is the path to a directory, where is the folder with xlsx_file.',
                        # if None default path will be specified based on xlsx_file_path.
                        default=None,
                        type=str)

    parser.add_argument('-ofn', '--output-file-name',
                        help='Filename for that will be created to store inspection results.'
                             f'Default is "{EvaluationArgument.RESULT_FILE_NAME_EXT.value}"',
                        default=f'{EvaluationArgument.RESULT_FILE_NAME_EXT.value}',
                        type=str)

    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=f'{run_tool_arguments.FORMAT.value.description}'
                             f'Use this argument when {EvaluationArgument.TRACEBACK.value} argument'
                             'is enabled argument will not be used otherwise.')


def create_dataframe(config) -> pd.DataFrame:
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
        lang_code_dataframe = pd.read_excel(config.xlsx_file_path)

    except FileNotFoundError as e:
        logger.error('XLSX-file with the specified name does not exists.')
        raise e

    try:
        for lang, code in zip(lang_code_dataframe[ColumnName.LANG.value],
                              lang_code_dataframe[ColumnName.CODE.value]):

            with new_temp_dir() as create_temp_dir:
                temp_dir_path = create_temp_dir
                lang_extension = LanguageVersion.language_by_extension(lang)
                temp_file_path = os.path.join(temp_dir_path, ('file' + lang_extension))
                temp_file_path = next(create_file(temp_file_path, code))

                try:
                    assert os.path.exists(temp_file_path)
                except AssertionError as e:
                    logger.exception('Path does not exist.')
                    raise e

                command = config.build_command(temp_file_path, lang)
                results = run_in_subprocess(command)
                os.remove(temp_file_path)
                temp_dir_path.rmdir()
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


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser, RunToolArgument)

    try:
        args = parser.parse_args()
        config = EvaluationConfig(args)
        workbook_path = create_and_get_workbook_path(config)
        results = create_dataframe(config)
        write_dataframe_to_xlsx_sheet(workbook_path, results, 'inspection_results')
        # remove empty sheet that was initially created with the workbook
        remove_sheet(workbook_path, 'Sheet')
        return 0

    except FileNotFoundError:
        logger.error('XLSX-file with the specified name does not exists.')
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
