import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd
from pandarallel import pandarallel
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.pandas_util import (
    get_issues_from_json,
    get_solutions_df_by_file_path,
    write_df_to_file,
)
from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.review.common.file_system import Extension, get_name_from_path, get_parent_folder

TRACEBACK = EvaluationArgument.TRACEBACK.value
GRADE = ColumnName.GRADE.value
HISTORY = ColumnName.HISTORY.value
USER = ColumnName.USER.value
TIME = ColumnName.TIME.value
EXTRACTED_ISSUES = 'extracted_issues'


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
        type=lambda value: Path(value).absolute(),
        help=f'Path to csv file. Your dataset must include column-names: "{USER}", "{TIME}, "{TRACEBACK}".',
    )

    parser.add_argument(
        '-o', '--output-path',
        type=lambda value: Path(value).absolute(),
        help='The path where the dataset with history will be saved. '
             'If not specified, the dataset will be saved next to the original one.',
    )

    parser.add_argument(
        '--dont-drop-traceback',
        help=f'The "{TRACEBACK}" column will not be removed from the final dataset.',
        action='store_true',
    )

    parser.add_argument(
        '--dont-drop-grade',
        help=f'The "{GRADE}" column will not be removed from the final dataset.',
        action='store_true',
    )


def update_counter(history: str, counter: Counter) -> None:
    issue_classes = []
    if history:
        issue_classes = history.split(',')
    counter.update(issue_classes)


def add_history(row, solutions_df: pd.DataFrame) -> str:
    counter = Counter()

    filtered_df = solutions_df[(solutions_df[USER] == row[USER]) & (solutions_df[TIME] < row[TIME])]
    filtered_df.apply(lambda row: update_counter(row[EXTRACTED_ISSUES], counter), axis=1)

    history = {'python': [{'origin_class': key, 'number': value} for key, value in counter.items()]}

    return json.dumps(history)


def extract_issues(traceback: str) -> str:
    issue_classes = []
    issues = get_issues_from_json(traceback)
    for issue in issues:
        issue_classes.append(issue.origin_class)
    return ','.join(issue_classes)


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    pandarallel.initialize()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)
    solutions_df[EXTRACTED_ISSUES] = solutions_df.parallel_apply(lambda row: extract_issues(row[TRACEBACK]), axis=1)
    solutions_df[HISTORY] = solutions_df.parallel_apply(add_history, axis=1, args=(solutions_df,))

    columns_to_drop = [EXTRACTED_ISSUES]

    if not args.dont_drop_grade:
        columns_to_drop.append(GRADE)

    if not args.dont_drop_traceback:
        columns_to_drop.append(TRACEBACK)

    solutions_df.drop(columns=columns_to_drop, inplace=True)

    output_path = args.output_path
    if output_path is None:
        output_dir = get_parent_folder(solutions_file_path)
        dataset_name = get_name_from_path(solutions_file_path, with_extension=False)
        output_path = output_dir / f'{dataset_name}_with_history{Extension.CSV.value}'

    write_df_to_file(solutions_df, output_path, Extension.CSV)


if __name__ == '__main__':
    main()
