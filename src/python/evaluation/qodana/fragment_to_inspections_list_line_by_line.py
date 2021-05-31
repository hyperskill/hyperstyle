import argparse
import os
from itertools import groupby
from pathlib import Path
from typing import Dict, List

import pandas as pd
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue
from src.python.evaluation.qodana.util.util import (
    configure_model_converter_arguments, get_inspections_dict, replace_inspections_on_its_ids,
)
from src.python.review.common.file_system import Extension, get_parent_folder


INSPECTIONS = QodanaColumnName.INSPECTIONS.value
CODE = ColumnName.CODE.value


# Make a new dataframe where code fragment is separated line by line and inspections are grouped line by line
def __replace_inspections_to_its_ids_in_row(row: pd.Series, inspections_dict: Dict[str, int],
                                            to_remove_duplicates: bool) -> pd.DataFrame:
    row_df = pd.DataFrame(row).transpose()
    fragment_lines = row_df.iloc[0][CODE].split(os.linesep)
    fragment_df = row_df.loc[row_df.index.repeat(len(fragment_lines))].reset_index(drop=True)

    issues_list = QodanaIssue.parse_list_issues_from_json(row_df.iloc[0][INSPECTIONS])
    line_number_to_issues = {k: list(v) for k, v in groupby(issues_list, key=lambda i: i.line)}
    for index, fragment_line in enumerate(fragment_lines):
        issues = line_number_to_issues.get(index + 1, [])
        fragment_df.iloc[index][CODE] = fragment_line
        fragment_df.iloc[index][INSPECTIONS] = replace_inspections_on_its_ids(issues, inspections_dict,
                                                                              to_remove_duplicates)
    return fragment_df


def __append_df(df: pd.DataFrame, df_list: List[pd.DataFrame]) -> None:
    df_list.append(df)


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_model_converter_arguments(parser)
    args = parser.parse_args()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)
    inspections_dict = get_inspections_dict(args.inspections_path)

    fragment_df_list = []
    solutions_df.apply(
        lambda row: __append_df(__replace_inspections_to_its_ids_in_row(row, inspections_dict, args.remove_duplicates),
                                fragment_df_list), axis=1)

    output_path = get_parent_folder(Path(solutions_file_path))
    write_dataframe_to_csv(output_path / f'numbered_ids_line_by_line{Extension.CSV.value}', pd.concat(fragment_df_list))


if __name__ == '__main__':
    main()
