import argparse
import sys
from collections import Counter
from pathlib import Path
from statistics import median
from typing import List

import pandas as pd
import plotly.express as px
from src.python.evaluation.common.pandas_util import logger
from src.python.evaluation.paper_evaluation.user_dynamics.user_statistics import DynamicsColumn
from src.python.review.common.file_system import (
    Extension, extension_file_condition, get_all_file_system_items, get_parent_folder,
)

MEDIAN_COLUMN = ('Median number of code quality issues in submissions<br>'
                 'by the same students before and after using Big Brother')
FREQ_COLUMN = 'Number of users'
TYPE = 'Submissions\' type'


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('dynamics_folder_path',
                        type=lambda value: Path(value).absolute(),
                        help='Folder with dynamics after embedding tool')

    parser.add_argument('old_dynamics_folder_path',
                        type=lambda value: Path(value).absolute(),
                        help='Folder with dynamics before embedding tool')


def __get_medians(dynamics_folder_path: Path) -> List[float]:
    dynamics_paths = get_all_file_system_items(dynamics_folder_path, extension_file_condition(Extension.CSV))
    medians = []
    for dynamic in dynamics_paths:
        dynamic_df = pd.read_csv(dynamic)
        medians.append(int(median(dynamic_df[DynamicsColumn.ISSUE_COUNT.value])))
    return medians


def __group_medians(path_to_dynamics: Path, dynamics_type: str, threshold: int = 8) -> pd.DataFrame:
    medians = __get_medians(path_to_dynamics)
    grouped_medians = dict(Counter(medians))
    more_threshold = sum([freq for m, freq in grouped_medians.items() if m > threshold])
    others = {str(m): freq for m, freq in grouped_medians.items() if m <= threshold}
    others[f'> {threshold}'] = more_threshold
    new_df = pd.DataFrame(others.items(), columns=[MEDIAN_COLUMN, FREQ_COLUMN])
    new_df[TYPE] = dynamics_type
    return new_df


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        old_df = __group_medians(args.old_dynamics_folder_path, 'Before embedding tool')
        new_df = __group_medians(args.dynamics_folder_path, 'After embedding tool')
        union_df = old_df.append(new_df).sort_values([MEDIAN_COLUMN, TYPE], ascending=[True, False])
        fig = px.bar(union_df, x=MEDIAN_COLUMN, y=FREQ_COLUMN, width=1000, height=800, color=TYPE,
                     color_discrete_sequence=['rgb(253,251,220)', 'rgb(47,22,84)'])
        fig.update_layout(legend={
            'yanchor': 'top',
            'y': 0.99,
            'xanchor': 'right',
            'x': 0.99,
        },
            font_size=22,
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        # Add borders around plot
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        # Add borders around bars
        fig.update_traces(marker_line_color='black', marker_line_width=1.5, opacity=0.9)

        output_path = get_parent_folder(args.old_dynamics_folder_path) / f'evaluation_chart{Extension.PDF.value}'
        fig.write_image(str(output_path))
        fig.show()
        return 0

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
