import argparse
from pathlib import Path

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.qodana.util.models import QodanaColumnName, QodanaIssue
from src.python.evaluation.qodana.util.util import get_inspections_dict, replace_inspections_on_its_ids
from src.python.review.common.file_system import Extension, get_parent_folder

INSPECTIONS = QodanaColumnName.INSPECTIONS.value


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.QODANA_SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.QODANA_SOLUTIONS_FILE_PATH.value.description)

    parser.add_argument(RunToolArgument.QODANA_INSPECTIONS_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.QODANA_INSPECTIONS_PATH.value.description)


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_file_path = args.solutions_file_path
    solutions_df = get_solutions_df_by_file_path(solutions_file_path)
    inspections_dict = get_inspections_dict(args.inspections_path)

    solutions_df[INSPECTIONS] = solutions_df.apply(
        lambda row: replace_inspections_on_its_ids(QodanaIssue.parse_list_issues_from_json(row[INSPECTIONS]),
                                                   inspections_dict), axis=1)

    output_path = get_parent_folder(Path(solutions_file_path))
    write_dataframe_to_csv(output_path / f'numbered_ids{Extension.CSV.value}', solutions_df)


if __name__ == '__main__':
    main()
