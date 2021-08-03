import argparse
import logging.config
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Optional

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from pandarallel import pandarallel
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import get_solutions_df, write_df_to_file
from src.python.evaluation.common.util import ColumnName, EvaluationArgument, script_structure_rule
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import create_file
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.SOLUTIONS_FILE_PATH.value.description)

    parser.add_argument('-tp', '--tool-path',
                        default=Path(f'{os.path.dirname(os.path.abspath(__file__))}/../review/run_tool.py'),
                        type=lambda value: Path(value).absolute(),
                        help='Path to script to run on files.')

    parser.add_argument('--traceback',
                        help='If True, column with the full inspector feedback will be added '
                             'to the output file with results.',
                        action='store_true')

    parser.add_argument('-ofp', '--output-folder-path',
                        help='An absolute path to the folder where file with evaluation results'
                             'will be stored.'
                             'Default is the path to a directory, where is the folder with xlsx or csv file.',
                        # if None default path will be specified based on solutions_file_path.
                        default=None,
                        type=str)

    parser.add_argument('-ofn', '--output-file-name',
                        help='Filename for that will be created to store inspection results.'
                             f'Default is "{EvaluationArgument.RESULT_FILE_NAME.value}" '
                             f'with the same extension as the input file has',
                        default=None,
                        type=str)

    parser.add_argument(RunToolArgument.FORMAT.value.short_name,
                        RunToolArgument.FORMAT.value.long_name,
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help=f'{RunToolArgument.FORMAT.value.description}'
                             f'Use this argument when {EvaluationArgument.TRACEBACK.value} argument'
                             'is enabled argument will not be used otherwise.')

    parser.add_argument('--with-history',
                        help=f'If True, then history will be taken into account when calculating the grade. '
                             f'In that case, for each fragment, the "{ColumnName.HISTORY.value}" column '
                             'must contain the history of previous errors.',
                        action='store_true')

    parser.add_argument('--to_drop_nan',
                        help='If True, empty code fragments will be deleted from df',
                        action='store_true')


def get_language_version(lang_key: str) -> LanguageVersion:
    try:
        return LanguageVersion(lang_key)
    except ValueError as e:
        logger.error(script_structure_rule)
        # We should raise KeyError since it is incorrect value for key in a column
        raise KeyError(e)


def __inspect_row(lang: str, code: str, fragment_id: int, history: Optional[str],
                  config: EvaluationConfig) -> Optional[str]:
    print(f'current id: {fragment_id}')
    # Tool does not work correctly with tmp files from <tempfile> module on macOS
    # thus we create a real file in the file system
    extension = get_language_version(lang).extension_by_language().value
    tmp_file_path = config.solutions_file_path.parent.absolute() / f'inspected_code_{fragment_id}{extension}'
    temp_file = next(create_file(tmp_file_path, code))
    command = config.build_command(temp_file, lang, history)
    results = run_in_subprocess(command)
    os.remove(temp_file)
    return results


def __get_grade_from_traceback(traceback: str) -> str:
    # this regular expression matches final tool grade: EXCELLENT, GOOD, MODERATE or BAD
    return re.match(r'^.*{"code":\s"([A-Z]+)"', traceback).group(1)


# TODO: calculate grade after it
def inspect_solutions_df(config: EvaluationConfig, lang_code_dataframe: pd.DataFrame,
                         to_drop_nan: bool = True) -> pd.DataFrame:
    report = pd.DataFrame(columns=lang_code_dataframe.columns)
    report[ColumnName.TRACEBACK.value] = []

    pandarallel.initialize()
    if config.traceback:
        report[ColumnName.TRACEBACK.value] = []
    try:
        if to_drop_nan:
            lang_code_dataframe = lang_code_dataframe.dropna()
        lang_code_dataframe[ColumnName.TRACEBACK.value] = lang_code_dataframe.parallel_apply(
            lambda row: __inspect_row(row[ColumnName.LANG.value],
                                      row[ColumnName.CODE.value],
                                      row[ColumnName.ID.value],
                                      row.get(ColumnName.HISTORY.value),
                                      config), axis=1)

        lang_code_dataframe[ColumnName.GRADE.value] = lang_code_dataframe.parallel_apply(
            lambda row: __get_grade_from_traceback(row[ColumnName.TRACEBACK.value]), axis=1)

        if not config.traceback:
            del lang_code_dataframe[ColumnName.TRACEBACK.value]
        return lang_code_dataframe

    except ValueError as e:
        logger.error(script_structure_rule)
        # parallel_apply can raise ValueError but it connected to KeyError: not all columns exist in df
        raise KeyError(e)

    except Exception as e:
        traceback.print_exc()
        logger.exception('An unexpected error.')
        raise e


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        start = time.time()
        args = parser.parse_args()
        config = EvaluationConfig(args)
        lang_code_dataframe = get_solutions_df(config.extension, config.solutions_file_path)
        results = inspect_solutions_df(config, lang_code_dataframe)
        write_df_to_file(results, config.get_output_file_path(), config.extension)
        end = time.time()
        print(f'All time: {end - start}')
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
