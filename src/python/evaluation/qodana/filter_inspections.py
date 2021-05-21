import argparse
import json
from pathlib import Path
from typing import List

import pandas as pd
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.common.util import parse_set_arg
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue, QodanaJsonField
from src.python.evaluation.qodana.util.util import to_json
from src.python.review.common.file_system import Extension, extension_file_condition, get_all_file_system_items


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('dataset_folder',
                        type=lambda value: Path(value).absolute(),
                        help='Path to a folder with csv files graded by Qodana. '
                             'Each file must have "inspections" column.')

    parser.add_argument('-i', '--inspections',
                        help='Set of inspections ids to exclude from the dataset',
                        type=str,
                        default='')


def __get_qodana_dataset(root: Path) -> pd.DataFrame:
    if not root.is_dir():
        raise ValueError(f'The {root} is not a directory')
    dataset_files = get_all_file_system_items(root, extension_file_condition(Extension.CSV))
    datasets = []
    for file_path in dataset_files:
        datasets.append(get_solutions_df_by_file_path(file_path))
    return pd.concat(datasets)


def __filter_inspections(json_issues: str, inspections_to_keep: List[str]) -> str:
    issues_list = json.loads(json_issues)[QodanaJsonField.ISSUES.value]
    filtered_issues = list(filter(lambda i: i.problem_id not in inspections_to_keep,
                                  map(lambda i: QodanaIssue.from_json(i), issues_list)))
    return to_json(filtered_issues)


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    dataset_folder = args.dataset_folder
    full_dataset = __get_qodana_dataset(dataset_folder)
    inspections_to_keep = parse_set_arg(args.inspections)

    full_dataset[QodanaColumnName.INSPECTIONS.value] = full_dataset.apply(
        lambda row: __filter_inspections(row[QodanaColumnName.INSPECTIONS.value], inspections_to_keep), axis=1)

    write_dataframe_to_csv(dataset_folder / f'filtered_issues{Extension.CSV.value}', full_dataset)


if __name__ == '__main__':
    main()
