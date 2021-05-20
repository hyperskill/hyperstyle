import argparse
from pathlib import Path
from typing import List, Set

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import get_issues_from_json, get_solutions_df_by_file_path
from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.review.common.file_system import Extension, get_parent_folder, serialize_data_and_write_to_file
from src.python.review.inspectors.issue import BaseIssue


TRACEBACK = EvaluationArgument.TRACEBACK.value
ID = ColumnName.ID.value
GRADE = ColumnName.GRADE.value


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.description}'
                             f'\nAll code fragments from this file must be graded ')

    parser.add_argument('-i', '--issues',
                        help='Set of issues',
                        default='')


def __parse_issues_arg(str_issues: str) -> Set[str]:
    return set(str_issues.split(','))


def __get_new_issues(traceback: str, new_issues_classes: Set[str]) -> List[BaseIssue]:
    all_issues = get_issues_from_json(traceback)
    return list(filter(lambda i: i.origin_class in new_issues_classes, all_issues))


def __add_issues_for_fragment(fragment_id: int, new_issues: List[BaseIssue], diffs: dict) -> None:
    if len(new_issues) > 0:
        diffs[TRACEBACK][fragment_id] = new_issues


# Make a dict with the same structure as in the find_diffs function from diffs_between_df.py
def get_statistics_dict(solutions_df: pd.DataFrame, new_issues_classes: Set[str]) -> dict:
    diffs = {
        GRADE: [],
        TRACEBACK: {},
    }
    solutions_df.apply(lambda row: __add_issues_for_fragment(row[ID],
                                                             __get_new_issues(row[TRACEBACK], new_issues_classes),
                                                             diffs), axis=1)
    return diffs


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)
    issues = __parse_issues_arg(args.issues)

    diffs = get_statistics_dict(solutions_df, issues)
    output_path = get_parent_folder(Path(solutions_file_path)) / f'diffs{Extension.PICKLE.value}'
    serialize_data_and_write_to_file(output_path, diffs)


if __name__ == '__main__':
    main()
