import argparse
from pathlib import Path
from typing import Dict

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue
from src.python.review.common.file_system import Extension, get_parent_folder

INSPECTIONS = QodanaColumnName.INSPECTIONS.value


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.QODANA_SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.QODANA_SOLUTIONS_FILE_PATH.value.description)

    parser.add_argument('inspections_path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to a CSV file with inspections list')


def __get_inspections_dict(inspections_path: str) -> Dict[str, int]:
    inspections_df = pd.read_csv(inspections_path)
    inspections_dict = inspections_df.set_index(QodanaColumnName.INSPECTION_ID.value).T.to_dict('list')
    for qodana_id, id_list in inspections_dict.items():
        inspections_dict[qodana_id] = id_list[0]
    return inspections_dict


def __replace_inspections_on_its_ids(json_issues: str, inspections_dict: Dict[str, int]) -> str:
    issues_list = QodanaIssue.parse_list_issues_from_json(json_issues)
    if len(issues_list) == 0:
        inspections = '0'
    else:
        issues_list.sort(key=lambda x: x.problem_id)
        inspections = ','.join(str(inspections_dict[i.problem_id]) for i in issues_list)
    return inspections


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)
    inspections_dict = __get_inspections_dict(args.inspections_path)

    solutions_df[INSPECTIONS] = solutions_df.apply(
        lambda row: __replace_inspections_on_its_ids(row[INSPECTIONS], inspections_dict), axis=1)

    output_path = get_parent_folder(Path(solutions_file_path))
    write_dataframe_to_csv(output_path / f'numbered_ids{Extension.CSV.value}', solutions_df)


if __name__ == '__main__':
    main()
