import argparse
import json
from pathlib import Path
from typing import Iterable, Set

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import (
    drop_duplicates, filter_df_by_iterable_value, get_solutions_df_by_file_path, write_df_to_file,
)
from src.python.evaluation.common.util import ColumnName, parse_set_arg
from src.python.evaluation.qodana.util.issue_types import QODANA_CLASS_NAME_TO_ISSUE_TYPE
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue
from src.python.review.common.file_system import Extension, get_parent_folder
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.reviewers.utils.print_review import convert_issue_to_json


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name}_hyperstyle',
                        type=lambda value: Path(value).absolute(),
                        help=f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.description}'
                             f'\nAll code fragments from this file must be graded by hyperstyle tool'
                             f'(file contains traceback column)')

    parser.add_argument(f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name}_qodana',
                        type=lambda value: Path(value).absolute(),
                        help=f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.description}'
                             f'\nAll code fragments from this file must be graded by qodana'
                             f'(file contains inspections column)')

    parser.add_argument('-i', '--issues-to-keep',
                        help='Set of issues to keep',
                        default='')


# Drop duplicates in the CODE column and delete rows that have ids from value_to_filter
# The new dataframe will be sorted by the ID column
def __preprocess_df(df: pd.DataFrame, ids_to_filter: Iterable) -> pd.DataFrame:
    df = drop_duplicates(df)
    df = filter_df_by_iterable_value(df, ColumnName.ID.value, ids_to_filter)
    return df.sort_values(ColumnName.ID.value).set_index(ColumnName.ID.value, drop=False)


# Check if all code fragments with the same ids are equal
def __check_code_by_ids(qodana_df: pd.DataFrame, hyperstyle_df: pd.DataFrame) -> None:
    assert qodana_df.shape[0] == hyperstyle_df.shape[0], (
        f'rows count {qodana_df.shape[0]} in the qodana df does not equal rows '
        f'count {hyperstyle_df.shape[0]} in the hyperstyle df'
    )
    for i in range(0, qodana_df.shape[0]):
        if qodana_df.iloc[i][ColumnName.CODE.value] != hyperstyle_df.iloc[i][ColumnName.CODE.value]:
            raise ValueError(f'Code fragments in the {i}th row do not equal!')


# Convert qodana inspections output to hyperstyle output
# Note: keep only <issues> json field in the result
def __qodana_to_hyperstyle_output(qodana_output: str, issues_to_keep: Set[str]) -> str:
    qodana_issues = QodanaIssue.parse_list_issues_from_json(qodana_output)
    filtered_issues = filter(lambda issue: issue.problem_id in issues_to_keep, qodana_issues)
    hyperstyle_issues = map(lambda issue:
                            BaseIssue(origin_class=issue.problem_id,
                                      type=QODANA_CLASS_NAME_TO_ISSUE_TYPE.get(issue.problem_id, IssueType.INFO),
                                      description=issue.description,
                                      file_path=Path(),
                                      line_no=issue.line,
                                      column_no=issue.offset,
                                      inspector_type=InspectorType.QODANA),
                            filtered_issues)
    hyperstyle_json = {'issues': list(map(lambda issue: convert_issue_to_json(issue), hyperstyle_issues))}

    return json.dumps(hyperstyle_json)


# Resort all fields in the qodana dataframe according to the hyperstyle dataframe
# Add column with hyperstyle output (convert qodana output to hyperstyle output)
# Add grade column with grades from hyperstyle dataframe (to gather issues_statistics by diffs_between_df.py script)
def __prepare_qodana_df(qodana_df: pd.DataFrame, hyperstyle_df: pd.DataFrame,
                        issues_to_keep: Set[str]) -> pd.DataFrame:
    qodana_df = __preprocess_df(qodana_df, hyperstyle_df[ColumnName.ID.value])
    __check_code_by_ids(qodana_df, hyperstyle_df)

    qodana_df[ColumnName.TRACEBACK.value] = qodana_df.apply(
        lambda row: __qodana_to_hyperstyle_output(row[QodanaColumnName.INSPECTIONS.value], issues_to_keep), axis=1)

    qodana_df[ColumnName.GRADE.value] = hyperstyle_df[ColumnName.GRADE.value]
    return qodana_df


def __write_updated_df(old_df_path: Path, df: pd.DataFrame, name_prefix: str) -> None:
    output_path = get_parent_folder(Path(old_df_path))
    write_df_to_file(df, output_path / f'{name_prefix}_updated{Extension.CSV.value}', Extension.CSV)


def __reassign_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(ColumnName.CODE.value)
    df[ColumnName.ID.value] = df.index
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    issues_to_keep = parse_set_arg(args.issues_to_keep)

    qodana_solutions_file_path = args.solutions_file_path_qodana
    qodana_solutions_df = __reassign_ids(get_solutions_df_by_file_path(qodana_solutions_file_path))

    hyperstyle_solutions_file_path = args.solutions_file_path_hyperstyle
    hyperstyle_solutions_df = __reassign_ids(get_solutions_df_by_file_path(hyperstyle_solutions_file_path))
    hyperstyle_solutions_df = __preprocess_df(hyperstyle_solutions_df, qodana_solutions_df[ColumnName.ID.value])

    qodana_solutions_df = __prepare_qodana_df(qodana_solutions_df, hyperstyle_solutions_df, issues_to_keep)

    __write_updated_df(qodana_solutions_file_path, qodana_solutions_df, 'qodana')
    __write_updated_df(hyperstyle_solutions_file_path, hyperstyle_solutions_df, 'hyperstyle')


if __name__ == '__main__':
    main()
