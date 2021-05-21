import argparse
import json
from pathlib import Path
from typing import Set

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue, QodanaJsonField
from src.python.review.common.file_system import Extension, get_parent_folder


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help='Csv file with solutions. This file must be graded by Qodana.')


def __get_inspections_ids(json_issues: str) -> Set[str]:
    issues_list = list(map(lambda i: QodanaIssue.from_json(i), json.loads(json_issues)[QodanaJsonField.ISSUES.value]))
    return set(map(lambda i: i.problem_id, issues_list))


def __get_unique_inspections(solutions_df: pd.DataFrame) -> Set[str]:
    inspections = solutions_df.apply(lambda row: __get_inspections_ids(row[QodanaColumnName.INSPECTIONS.value]),
                                     axis=1)
    return set.union(*inspections.values)


def __create_unique_inspections_df(unique_inspections: Set[str]) -> pd.DataFrame:
    id_to_inspection = {}
    for index, inspection in enumerate(unique_inspections):
        id_to_inspection[index + 1] = inspection
    return pd.DataFrame(id_to_inspection.items(),
                        columns=[QodanaColumnName.ID.value, QodanaColumnName.INSPECTION_ID.value])


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)

    inspections_df = __create_unique_inspections_df(__get_unique_inspections(solutions_df))
    output_path = get_parent_folder(Path(solutions_file_path))
    write_dataframe_to_csv(output_path / f'inspections{Extension.CSV.value}', inspections_df)


if __name__ == '__main__':
    main()
