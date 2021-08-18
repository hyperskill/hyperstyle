import argparse
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.plots.common.utils import get_supported_extensions, save_plot
from src.python.evaluation.plots.plotters.raw_issues_statistics_plotters import prepare_stats
from src.python.review.common.file_system import Extension, parse_yaml

logger = logging.getLogger(__name__)
COLORWAY = ['rgb(47,22,84)', 'rgb(99,47,177)', 'rgb(153,110,216)']


class _ConfigFields(Enum):
    PLOT_CONFIG = 'plot_config'
    ROWS = 'rows'
    COLS = 'cols'
    SPECS = 'specs'
    HEIGHT = 'height'
    WIDTH = 'width'
    X_AXIS_NAME = 'x_axis_name'
    Y_AXIS_NAME = 'y_axis_name'

    RANGE_OF_VALUES = 'range_of_values'
    TRACE_NAME = 'trace_name'


_PLOT_CONFIG = _ConfigFields.PLOT_CONFIG.value
_ROWS = _ConfigFields.ROWS.value
_COLS = _ConfigFields.COLS.value
_SPECS = _ConfigFields.SPECS.value
_HEIGHT = _ConfigFields.HEIGHT.value
_WIDTH = _ConfigFields.WIDTH.value
_X_AXIS_NAME = _ConfigFields.X_AXIS_NAME.value
_Y_AXIS_NAME = _ConfigFields.Y_AXIS_NAME.value
_RANGE_OF_VALUES = _ConfigFields.RANGE_OF_VALUES.value
_TRACE_NAME = _ConfigFields.TRACE_NAME.value


@dataclass
class PlotConfig:
    name: str
    rows: int = 1
    cols: int = 1
    height: int = 800
    width: int = 1600
    x_axis_name: str = 'Value'
    y_axis_name: str = 'Quantity'
    specs: Optional[List] = None

    @staticmethod
    def get_from_dict(plot_name: str, config: Dict) -> 'PlotConfig':
        params = {'name': plot_name}
        params.update(config)
        return PlotConfig(**params)


@dataclass
class TraceConfig:
    column: str
    range_of_values: Optional[range] = None
    trace_name: Optional[str] = None

    @staticmethod
    def get_from_dict(column_name: str, config: Dict) -> 'TraceConfig':
        params = {'column': column_name}
        params.update(config)

        if _RANGE_OF_VALUES in params:
            params[_RANGE_OF_VALUES] = range(*params[_RANGE_OF_VALUES])

        return TraceConfig(**params)


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'stats_path',
        type=lambda value: Path(value).absolute(),
        help='Path to the statistics file. Must be an xlsx or csv file.',
    )

    parser.add_argument(
        'config_path',
        type=lambda value: Path(value).absolute(),
        help='Path to the yaml file containing information about the graphs to be plotted.',
    )

    parser.add_argument(
        'save_dir',
        type=lambda value: Path(value).absolute(),
        help='The directory where the plotted charts will be saved.',
    )

    parser.add_argument(
        '--file-extension',
        type=str,
        default=Extension.SVG.value,
        choices=get_supported_extensions(),
        help='Allows you to select the extension of output files.',
    )


def build_subplots(df: pd.DataFrame, plot_config: PlotConfig, trace_configs: List[TraceConfig]) -> go.Figure:
    fig = make_subplots(
        rows=plot_config.rows,
        cols=plot_config.cols,
        specs=plot_config.specs,
    )

    if plot_config.specs is None:
        plot_config.specs = [[{} for _ in range(plot_config.cols)] for _ in range(plot_config.rows)]

    current_index = 0
    current_row = 1
    for row in plot_config.specs:
        current_column = 1
        for cell in row:
            if cell is None:
                current_column += 1
                continue

            trace_config = trace_configs[current_index]

            stats = prepare_stats(
                df,
                trace_config.column,
                trace_config.range_of_values,
                plot_config.x_axis_name,
                plot_config.y_axis_name,
            )

            fig.add_scatter(
                x=stats[plot_config.x_axis_name],
                y=stats[plot_config.y_axis_name],
                col=current_column,
                row=current_row,
                line={'width': 5},
                marker={'size': 10},
                name=trace_config.trace_name if trace_config.trace_name is not None else trace_config.column,
            )

            current_column += 1
            current_index += 1

        current_row += 1

    fig.update_layout(
        width=plot_config.width,
        height=plot_config.height,
        font_size=22,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        colorway=COLORWAY,
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        title=plot_config.x_axis_name,
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        title=plot_config.y_axis_name,
    )

    return fig


def plot_and_save(stats: pd.DataFrame, config: Dict, output_dir: Path, extension: Extension) -> None:
    for group_name, group_config in config.items():
        plot_config = PlotConfig.get_from_dict(group_name, group_config.pop(_PLOT_CONFIG))
        trace_configs = []
        for column_name, column_config in group_config.items():
            trace_configs.append(TraceConfig.get_from_dict(column_name, column_config))
        subplots = build_subplots(stats, plot_config, trace_configs)
        save_plot(subplots, output_dir, group_name, extension)


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()

        config = parse_yaml(args.config_path)
        stats = get_solutions_df_by_file_path(args.stats_path)

        plot_and_save(stats, config, args.save_dir, Extension(args.file_extension))

        return 0

    except IndexError:
        logger.error('The number of traces must be consistent with the number of rows and columns, '
                     'as well as the specs.')
        return 2

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == "__main__":
    sys.exit(main())
