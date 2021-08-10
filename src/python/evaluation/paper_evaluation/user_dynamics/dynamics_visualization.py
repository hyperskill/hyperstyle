import argparse
import sys
from pathlib import Path
from statistics import median

import pandas as pd
import plotly.graph_objects as go
from src.python.evaluation.common.pandas_util import logger
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.paper_evaluation.user_dynamics.user_statistics import DynamicsColumn
from src.python.review.common.file_system import Extension, extension_file_condition, get_all_file_system_items


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('dynamics_folder_path',
                        type=lambda value: Path(value).absolute(),
                        help='Add description here')


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        dynamics_folder_path = args.dynamics_folder_path
        dynamics_paths = get_all_file_system_items(dynamics_folder_path, extension_file_condition(Extension.CSV))
        dynamic_fig = go.Figure()

        medians = []
        for i, dynamic in enumerate(dynamics_paths):
            dynamic_df = pd.read_csv(dynamic)

            dynamic_df = dynamic_df.head(100)
            dynamic_fig.add_trace(go.Scatter(
                x=dynamic_df[ColumnName.TIME.value],
                y=dynamic_df[DynamicsColumn.ISSUE_COUNT.value],
                name=f'user {i}',
            ))
            medians.append(median(dynamic_df[DynamicsColumn.ISSUE_COUNT.value]))

        dynamic_fig.update_layout(title='Code quality issues dynamics for Python',
                                  xaxis_title='Submission number',
                                  yaxis_title='Code quality issues count')
        dynamic_fig.show()

        medians = go.Figure(data=go.Scatter(x=list(range(len(medians))), y=medians))
        medians.update_layout(title='Median values for code quality issues dynamics for Python',
                              xaxis_title='Student number',
                              yaxis_title='Median of code quality issues count')
        medians.show()
        return 0

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
