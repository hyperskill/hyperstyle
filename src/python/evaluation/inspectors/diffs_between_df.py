import argparse
import json
from pathlib import Path
from typing import List

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import (
    get_inconsistent_positions, get_solutions_df, get_solutions_df_by_file_path,
)
from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.review.common.file_system import (
    Extension, get_parent_folder, get_restricted_extension, serialize_data_and_write_to_file,
)
from src.python.review.inspectors.issue import BaseIssue
from src.python.review.quality.model import QualityType
from src.python.review.reviewers.utils.print_review import convert_json_to_issues


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name}_old',
                        type=lambda value: Path(value).absolute(),
                        help=f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.description}'
                             f'\nAll code fragments from this file must be graded '
                             f'(file contains grade and traceback (optional) columns)')

    parser.add_argument(f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name}_new',
                        type=lambda value: Path(value).absolute(),
                        help=f'{RunToolArgument.SOLUTIONS_FILE_PATH.value.description}'
                             f'\nAll code fragments from this file must be graded '
                             f'(file contains grade and traceback (optional) columns)')


def __get_issues(df: pd.DataFrame, row: int) -> List[BaseIssue]:
    parsed_json = json.loads(df.iloc[row][EvaluationArgument.TRACEBACK.value])['issues']
    return convert_json_to_issues(parsed_json)


# Find difference between two dataframes. Return dict:
# {
#  grade: [list_of_fragment_ids],
#  traceback: {
#       fragment_id: [list of issues]
#     },
# }
# The key <grade> contains only fragments that increase quality in new df
# The key <traceback> contains list of new issues for each fragment
def find_diffs(old_df: pd.DataFrame, new_df: pd.DataFrame) -> dict:
    inconsistent_positions = get_inconsistent_positions(old_df, new_df)
    diffs = {
        ColumnName.GRADE.value: [],
        EvaluationArgument.TRACEBACK.value: {},
    }
    # Keep only diffs in the TRACEBACK column
    for row, _ in filter(lambda t: t[1] == EvaluationArgument.TRACEBACK.value, inconsistent_positions.index):
        old_value = old_df.iloc[row][ColumnName.GRADE.value]
        new_value = new_df.iloc[row][ColumnName.GRADE.value]
        old_quality = QualityType(old_value).to_number()
        new_quality = QualityType(new_value).to_number()
        fragment_id = old_df.iloc[row][ColumnName.ID.value]
        if new_quality > old_quality:
            # It is an unexpected keys, we should check the algorithm
            diffs[ColumnName.GRADE.value].append(fragment_id)
        else:
            # Find difference between issues
            old_issues = __get_issues(old_df, row)
            new_issues = __get_issues(new_df, row)
            if len(old_issues) > len(new_issues):
                raise ValueError(f'New dataframe contains less issues than old for fragment {id}')
            difference = set(set(new_issues) - set(old_issues))
            diffs[EvaluationArgument.TRACEBACK.value][fragment_id] = difference
    return diffs


# TODO: add description in readme
def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    old_solutions_file_path = args.solutions_file_path_old
    output_ext = get_restricted_extension(old_solutions_file_path, [Extension.XLSX, Extension.CSV])
    old_solutions_df = get_solutions_df(output_ext, old_solutions_file_path)

    new_solutions_file_path = args.solutions_file_path_new
    new_solutions_df = get_solutions_df_by_file_path(new_solutions_file_path)

    diffs = find_diffs(old_solutions_df, new_solutions_df)
    output_path = get_parent_folder(Path(old_solutions_file_path)) / f'diffs{Extension.PICKLE.value}'
    serialize_data_and_write_to_file(output_path, diffs)


if __name__ == '__main__':
    main()
