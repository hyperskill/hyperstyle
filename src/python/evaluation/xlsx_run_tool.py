import argparse
import logging.config
import os
import re
import sys
import traceback
from pathlib import Path
from typing import NoReturn

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from openpyxl import Workbook
from src.python import MAIN_FOLDER
from src.python.evaluation import ScriptStructureRule
from src.python.evaluation.evaluation_config import ApplicationConfig
from src.python.evaluation.support_functions import remove_sheet
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser) -> NoReturn:
    parser.add_argument('data_path',
                        type=lambda value: Path(value).absolute(),
                        help='Local XLSX-file path. '
                             'Your XLSX-file must include column-names: \"code\" and \"lang. '
                             'Acceptable values for \"lang\" column are: python3, java8, java11, kotlin.')

    parser.add_argument('-t', '--tool_path',
                        default=Path('src/python/review/run_tool.py').absolute(),
                        type=lambda value: Path(value).absolute(),
                        help='Path to script to run on files.')

    parser.add_argument('--traceback', '--traceback',
                        help='If True – grades are substituted with the full inspector feedback.',
                        default=False,
                        type=bool)

    parser.add_argument('--folder_path', '--folder_path',
                        help='An absolute path to the folder where file with evaluation results'
                             'will be stored.'
                             'Default is \"hyperstyle/src/python/evaluation/results\"',
                        default=None,
                        type=str)

    parser.add_argument('--file_name', '--file_name',
                        help='Filename for that will be created to store inspection results.'
                             'Default is \"results.xlsx\"',
                        default='results.xlsx',
                        type=str)

    parser.add_argument('-f', '--format',
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help='The output format of inspectors traceback. '
                             'Default is JSON.'
                             'More details on output format options in README.md')


def create_dataframe(config) -> pd.DataFrame:
    report = pd.DataFrame(
        {
            "language": [],
            "code": [],
            "grade": [],
        },
    )

    dataframe = pd.read_excel(config.get_data_path())

    temp_dir_path = MAIN_FOLDER.parent / 'evaluation/temporary_files'
    lang_suffixes = {'python3': '.py', 'java8': '.java', 'java11': '.java', 'kotlin': '.kt'}

    for lang, code in zip(dataframe['lang'], dataframe['code']):
        temp_file_path = os.path.join(temp_dir_path, ('file' + lang_suffixes[lang]))

        try:
            assert os.path.exists(temp_file_path)
        except AssertionError:
            logger.exception('Path does not exist.')
            return 2

        with open(temp_file_path, 'w+') as file:
            file.writelines(code)

        command = config.build_command(temp_file_path, lang)
        results = run_in_subprocess(command)
        os.remove(temp_file_path)

        # this regular expression matches final tool grade: EXCELLENT, GOOD, MODERATE or BAD
        regex_match = re.match(r'^.*{"code":\s"([A-Z]+)"', results).group(1)

        output = regex_match
        if config.get_traceback():
            output = results

        report = report.append(pd.DataFrame(
            {
                "language": [lang],
                "code": [code],
                "grade": [output],
            },
        ))

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        config = ApplicationConfig(args)

        workbook = Workbook()
        workbook_path = config.get_file_path()
        workbook.save(workbook_path)

        results = create_dataframe(config)
        print(results, workbook_path)

        with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a') as writer:
            results.to_excel(writer, sheet_name='inspection_results', index=False)

        # remove empty sheet that was initially created with the workbook
        remove_sheet(workbook_path, 'Sheet')

        return 0

    except FileNotFoundError:
        logger.error('XLSX-file with the specified name does not exists.')
        return 2

    except KeyError:
        logger.error(ScriptStructureRule)
        return 2

    except Exception:
        traceback.print_exc()
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
