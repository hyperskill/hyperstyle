import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from pandarallel import pandarallel
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path, write_df_to_file
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.evaluation_run_tool import get_language_version
from src.python.evaluation.statistics.common.raw_issue_encoder_decoder import RawIssueEncoder
from src.python.review.common.file_system import (
    create_file,
    Extension,
    get_name_from_path,
    get_parent_folder,
)
from src.python.review.common.language import Language
from src.python.review.inspectors.issue import (
    BaseIssue,
    IssueType,
    Measurable,
)
from src.python.review.reviewers.common import LANGUAGE_TO_INSPECTORS
from src.python.review.reviewers.utils.issues_filter import filter_duplicate_issues

LANG = ColumnName.LANG.value
CODE = ColumnName.CODE.value
ID = ColumnName.ID.value
RAW_ISSUES = 'raw_issues'

ALLOWED_EXTENSION = {Extension.XLSX, Extension.CSV}

logger = logging.getLogger(__name__)


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
        type=lambda value: Path(value).absolute(),
        help=RunToolArgument.SOLUTIONS_FILE_PATH.value.description,
    )

    parser.add_argument(
        RunToolArgument.DUPLICATES.value.long_name,
        action='store_true',
        help=RunToolArgument.DUPLICATES.value.description,
    )

    parser.add_argument(
        '--allow-zero-measure-issues',
        action='store_true',
        help='Allow issues with zero measure. By default, such issues are skipped.',
    )

    parser.add_argument(
        '--allow-info-issues',
        action='store_true',
        help='Allow issues from the INFO category. By default, such issues are skipped.',
    )

    parser.add_argument(
        '--to-save-path',
        action='store_true',
        help='Allows to save the path to the file where the issue was found. By default, the path is not saved.',
    )

    parser.add_argument(
        '-o', '--output',
        type=lambda value: Path(value).absolute(),
        help='Path where the dataset with raw issues will be saved. '
             'If not specified, the dataset will be saved next to the original one.',
    )

    parser.add_argument(
        '-l', '--log-output',
        type=lambda value: Path(value).absolute(),
        help='Path where logs will be stored. If not specified, then logs will be output to stderr.',
    )


def _filter_issues(
    issues: List[BaseIssue],
    allow_duplicates: bool,
    allow_zero_measure_issues: bool,
    allow_info_issues: bool,
) -> List[BaseIssue]:

    filtered_issues = issues

    if not allow_duplicates:
        filtered_issues = filter_duplicate_issues(filtered_issues)

    if not allow_zero_measure_issues:
        filtered_issues = list(
            filter(lambda issue: not isinstance(issue, Measurable) or issue.measure() != 0, filtered_issues),
        )

    if not allow_info_issues:
        filtered_issues = list(filter(lambda issue: issue.type != IssueType.INFO, filtered_issues))

    return filtered_issues


def _inspect_row(
    fragment_id: int,
    code: str,
    language_code: str,
    solutions_file_path: Path,
    allow_duplicates: bool,
    allow_zero_measure_issues: bool,
    allow_info_issues: bool,
    to_safe_path: bool,
) -> Optional[str]:

    print(f'{fragment_id}: processing started')

    # If we were unable to identify the language version, we return None
    try:
        language_version = get_language_version(language_code)
    except KeyError:
        logger.warning(f'{fragment_id}: it was not possible to determine the language version from "{language_code}"')
        return None

    # If we were unable to identify the language, we return None
    language = Language.from_language_version(language_version)
    if language == Language.UNKNOWN:
        logger.warning(f'{fragment_id}: it was not possible to determine the language from "{language_version}"')
        return None

    # If there are no inspectors for the language, then return None
    inspectors = LANGUAGE_TO_INSPECTORS.get(language, [])
    if not inspectors:
        logger.warning(f'{fragment_id}: no inspectors were found for the {language}.')
        return None

    tmp_file_extension = language_version.extension_by_language().value
    tmp_file_path = solutions_file_path.parent.absolute() / f'fragment_{fragment_id}{tmp_file_extension}'

    try:
        temp_file = next(create_file(tmp_file_path, code))
    except Exception:
        logger.warning(f'{fragment_id}: unable to create file', exc_info=True, stack_info=True)
        return None

    inspectors_config = {
        'language_version': language_version,
        'n_cpu': 1,
    }

    raw_issues = []

    for inspector in inspectors:
        try:
            raw_issues.extend(inspector.inspect(temp_file, inspectors_config))
        except Exception:
            logger.warning(f'{fragment_id}: inspector {inspector.inspector_type.value} failed.')

    os.remove(temp_file)

    raw_issues = _filter_issues(raw_issues, allow_duplicates, allow_zero_measure_issues, allow_info_issues)

    json_issues = json.dumps(raw_issues, cls=RawIssueEncoder, to_safe_path=to_safe_path)

    print(f'{fragment_id}: processing finished.')

    return json_issues


def _is_correct_output_path(output_path: Path) -> bool:
    try:
        output_extension = Extension.get_extension_from_file(str(output_path))
    except ValueError:
        return False

    return output_extension in ALLOWED_EXTENSION


def _get_output_path(solutions_file_path: Path, output_path: Optional[Path]) -> Path:
    if output_path is not None:
        if _is_correct_output_path(output_path):
            return output_path
        logger.warning('The output path is not correct. The resulting dataset will be saved next to the original one.')

    extension = Extension.get_extension_from_file(str(solutions_file_path))
    output_dir = get_parent_folder(solutions_file_path)
    dataset_name = get_name_from_path(solutions_file_path, with_extension=False)
    return output_dir / f'{dataset_name}_with_raw_issues{extension.value}'


def inspect_solutions(
    solutions_df: pd.DataFrame,
    solutions_file_path: Path,
    allow_duplicates: bool,
    allow_zero_measure_issues: bool,
    allow_info_issues: bool,
    to_save_path: bool,
) -> pd.DataFrame:

    pandarallel.initialize()

    solutions_df[RAW_ISSUES] = solutions_df.parallel_apply(
        lambda row: _inspect_row(
            row[ID],
            row[CODE],
            row[LANG],
            solutions_file_path,
            allow_duplicates,
            allow_zero_measure_issues,
            allow_info_issues,
            to_save_path,
        ),
        axis=1,
    )

    return solutions_df


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()
    logging.basicConfig(
        filename=args.log_output, level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s',
    )

    solutions = get_solutions_df_by_file_path(args.solutions_file_path)

    logger.info("Dataset inspection started.")

    solutions_with_raw_issues = inspect_solutions(
        solutions,
        args.solutions_file_path,
        args.allow_duplicates,
        args.allow_zero_measure_issues,
        args.allow_info_issues,
        args.to_save_path,
    )

    logger.info("Dataset inspection finished.")

    output_path = _get_output_path(args.solutions_file_path, args.output)
    output_extension = Extension.get_extension_from_file(str(output_path))

    logger.info(f'Saving the dataframe to a file: {output_path}.')

    write_df_to_file(solutions_with_raw_issues, output_path, output_extension)

    logger.info('Saving complete.')


if __name__ == '__main__':
    main()
