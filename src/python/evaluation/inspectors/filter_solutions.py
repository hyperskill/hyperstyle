import argparse
import logging
import sys
from pathlib import Path
from typing import Set

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import get_solutions_df, filter_df_by_language, write_df_to_file
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import get_restricted_extension, Extension, get_parent_folder

logger = logging.getLogger(__name__)


def parse_languages(value: str) -> Set[LanguageVersion]:
    passed_names = value.lower().split(',')
    allowed_names = {lang.value for lang in LanguageVersion}
    if not all(name in allowed_names for name in passed_names):
        raise argparse.ArgumentError('--languages', 'Incorrect --languages\' names')

    return {LanguageVersion(name) for name in passed_names}


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.SOLUTIONS_FILE_PATH.value.description)

    parser.add_argument('-l', '--languages',
                        help='Set of languages to keep in the dataset',
                        type=parse_languages,
                        default=set(LanguageVersion))


# TODO: add readme
def main() -> int:
    try:
        parser = argparse.ArgumentParser()
        configure_arguments(parser)
        args = parser.parse_args()

        solutions_file_path = args.solutions_file_path
        ext = get_restricted_extension(solutions_file_path, [Extension.XLSX, Extension.CSV])
        solutions_df = get_solutions_df(ext, args.solutions_file_path)

        filtered_df = filter_df_by_language(solutions_df, args.languages)
        output_path = get_parent_folder(Path(solutions_file_path))
        write_df_to_file(filtered_df, output_path / f'filtered_solutions{ext.value}', ext)
        return 0

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())