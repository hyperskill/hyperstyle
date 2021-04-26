import argparse
import enum
import logging.config
import os
import re
import sys
import traceback
from pathlib import Path
from typing import NoReturn, Union

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from openpyxl import Workbook
from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.common.util import EvaluationProcessNames, script_structure_rule
from src.python.evaluation.common.xlsx_util import remove_sheet, write_dataframe_to_xlsx_sheet
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import create_file, new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser, run_tool_arguments: enum.EnumMeta) -> NoReturn:
    parser.add_argument('xlsx_file_path',
                        type=lambda value: Path(value).absolute(),
                        help='Local XLSX-file path. '
                             'Your XLSX-file must include column-names: '
                             f'"{EvaluationProcessNames.CODE.value}" and '
                             f'"{EvaluationProcessNames.LANG.value}". Acceptable values for '
                             f'"{EvaluationProcessNames.LANG.value}" column are: '
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
                             f'Default is "{EvaluationProcessNames.RESULTS_EXT.value}"',
                        default=f'{EvaluationProcessNames.RESULTS_EXT.value}',
                        type=str)

    parser.add_argument(run_tool_arguments.FORMAT.value.short_name,
                        run_tool_arguments.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=run_tool_arguments.FORMAT.value.help)


def create_dataframe(config) -> Union[int, pd.DataFrame]:
    report = pd.DataFrame(
        {
            EvaluationProcessNames.LANGUAGE.value: [],
            EvaluationProcessNames.CODE.value: [],
            EvaluationProcessNames.GRADE.value: [],
        },
    )

    if config.traceback:
        report[EvaluationProcessNames.TRACEBACK.value] = []

    try:
        lang_code_dataframe = pd.read_excel(config.xlsx_file_path)

    except FileNotFoundError:
        logger.error('XLSX-file with the specified name does not exists.')
        return 2

    try:
        for lang, code in zip(lang_code_dataframe[EvaluationProcessNames.LANG.value],
                              lang_code_dataframe[EvaluationProcessNames.CODE.value]):

            with new_temp_dir() as create_temp_dir:
                temp_dir_path = create_temp_dir
                lang_extension = LanguageVersion.language_extension()[lang]
                temp_file_path = os.path.join(temp_dir_path, ('file' + lang_extension))
                temp_file_path = next(create_file(temp_file_path, code))

                try:
                    assert os.path.exists(temp_file_path)
                except AssertionError:
                    logger.exception('Path does not exist.')
                    return 2

                command = config.build_command(temp_file_path, lang)
                results = run_in_subprocess(command)
                os.remove(temp_file_path)
                temp_dir_path.rmdir()
                # this regular expression matches final tool grade: EXCELLENT, GOOD, MODERATE or BAD
                grades = re.match(r'^.*{"code":\s"([A-Z]+)"', results).group(1)
                output_row_values = [lang, code, grades]
                column_indices = [EvaluationProcessNames.LANGUAGE.value,
                                  EvaluationProcessNames.CODE.value,
                                  EvaluationProcessNames.GRADE.value]

                if config.traceback:
                    output_row_values.append(results)
                    column_indices.append(EvaluationProcessNames.TRACEBACK.value)

                new_file_report_row = pd.Series(data=output_row_values, index=column_indices)
                report = report.append(new_file_report_row, ignore_index=True)

        return report

    except KeyError:
        logger.error(script_structure_rule)
        return 2

    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error.')
        return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser, RunToolArguments)

    try:
        args = parser.parse_args()
        config = EvaluationConfig(args)

        workbook = Workbook()
        workbook_path = config.get_file_path()
        workbook.save(workbook_path)

        results = create_dataframe(config)

        write_dataframe_to_xlsx_sheet(workbook_path, results, 'inspection_results', 'openpyxl')
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
