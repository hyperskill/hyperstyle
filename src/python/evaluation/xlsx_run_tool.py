import argparse
import logging.config
import os
import pandas as pd
import re
import sys
import tempfile
import traceback

from pathlib import Path
from typing import NoReturn

sys.path.append('')
sys.path.append('../../..')

from src.python import MAIN_FOLDER
from src.python.evaluation import ScriptStructureRule
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.run_tool import positive_int
from src.python.review.reviewers.perform_review import OutputFormat

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser) -> NoReturn:
    parser.add_argument('-t', '--tool_path',
                        default=Path('src/python/review/run_tool.py').absolute(),
                        type=lambda value: Path(value).absolute(),
                        help='Path to script to run on files.')

    parser.add_argument('data_path',
                        type=lambda value: Path(value).absolute(),
                        help="Local XLSX-file path. "
                             "Your XLSX-file must include column-names: \"code\" and \"lang. "
                             "Acceptable values for \"lang\" column are: python3, java8, java11, kotlin.")

    parser.add_argument('--n_cpu', '--n-cpu',
                        help='Specify number of cpu that can be used to run inspectors.',
                        default=1,
                        type=positive_int)

    parser.add_argument('--traceback', '--traceback',
                        help='If True – grades are substituted with the full inspector feedback.',
                        default=False,
                        type=bool)

    parser.add_argument('-f', '--format',
                        default=OutputFormat.JSON.value,
                        choices=OutputFormat.values(),
                        type=str,
                        help='The output format of inspectors traceback. '
                             'Default is JSON.'
                             'More details on output format options in README.md')


def main() -> int:
    report = pd.DataFrame(
        {
            "language": [],
            "code": [],
            "grade": [],
        },
    )

    lang_suffixes = {'python3': '.py', 'java8': '.java', 'java11': '.java', 'kotlin': '.kt'}

    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        dataframe = pd.read_excel(args.data_path)

        for lang, code in zip(dataframe['lang'], dataframe['code']):
            file = tempfile.NamedTemporaryFile(
                dir=(MAIN_FOLDER.parent / 'evaluation/temporary_files'),
                suffix=lang_suffixes[lang],
                delete=False, mode="w",
            )

            file = open(file.name, "w")
            file.writelines(code)
            file.close()

            if lang == 'java8' or lang == 'java11':
                results = run_in_subprocess([
                    'python3', args.tool_path, file.name, '--language_version', lang])

            else:
                results = run_in_subprocess(['python3', args.tool_path, file.name])

            os.unlink(file.name)

            # this regular expression matches final tool grade: EXCELLENT, GOOD, MODERATE or BAD
            regex_match = re.match(r'^.*{"code":\s"([A-Z]+)"', results).group(1)

            if args.traceback:
                output = results
            else:
                output = regex_match

            report = report.append(pd.DataFrame(
                {
                    "language": [lang],
                    "code": [code],
                    "grade": [output],
                },
            ))

        with pd.ExcelWriter(args.data_path, engine='openpyxl', mode='a') as writer:
            report.to_excel(writer, sheet_name='inspection_results', index=False)
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
