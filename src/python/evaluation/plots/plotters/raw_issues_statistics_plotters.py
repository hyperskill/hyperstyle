from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable, Dict, Optional, Tuple, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.python.evaluation.issues_statistics.get_raw_issues_statistics import VALUE
from src.python.evaluation.plots.common import plotly_consts
from src.python.evaluation.plots.common.utils import create_histogram, create_line_plot, create_box_plot


@unique
class PlotTypes(Enum):
    LINE_CHART = 'line_chart'
    HISTOGRAM = 'histogram'
    BOXPLOT = 'boxplot'

    def to_plotter_function(self) -> Callable[..., go.Figure]:
        type_to_function = {
            PlotTypes.LINE_CHART: plot_line_chart,
            PlotTypes.HISTOGRAM: plot_histogram,
            PlotTypes.BOXPLOT: plot_boxplot,
        }

        return type_to_function[self]


@dataclass
class PlotConfig:
    column: str
    type: PlotTypes
    x_axis_name: Optional[str] = None
    y_axis_name: Optional[str] = None
    margin: Optional[plotly_consts.MARGIN] = None
    color: Optional[plotly_consts.COLOR] = None
    boundaries: Optional[Dict[int, Optional[str]]] = None
    range_of_values: Optional[range] = None
    n_bins: Optional[int] = None


def _prepare_stats(stats: pd.DataFrame, config: PlotConfig, x_axis_name: str, y_axis_name: str) -> pd.DataFrame:
    result_df = stats[[VALUE, config.column]]

    if config.range_of_values is not None:
        result_df = result_df[result_df[VALUE].isin(config.range_of_values)]

    result_df.set_index(VALUE, inplace=True)

    # Trim trailing zeros
    result_df = result_df.apply(lambda column: np.trim_zeros(column, trim='b')).dropna()

    # Fill in the missing intermediate values with zeros
    min_index, max_index = result_df.index.min(), result_df.index.max()
    result_df = result_df.reindex(range(min_index, max_index + 1), fill_value=0)

    result_df.reset_index(inplace=True)

    return result_df.rename(columns={VALUE: x_axis_name, config.column: y_axis_name})


def _get_axis_names(config: PlotConfig, default_x_axis_name: str, default_y_axis_name: str) -> Tuple[str, str]:
    x_axis_name = default_x_axis_name
    if config.x_axis_name is not None:
        x_axis_name = config.x_axis_name

    y_axis_name = default_y_axis_name
    if config.y_axis_name is not None:
        y_axis_name = config.y_axis_name

    return x_axis_name, y_axis_name


def plot_line_chart(stats: pd.DataFrame, config: PlotConfig) -> go.Figure:
    x_axis_name, y_axis_name = _get_axis_names(
        config, default_x_axis_name='Value', default_y_axis_name='Number of fragments',
    )

    stats = _prepare_stats(stats, config, x_axis_name, y_axis_name)

    return create_line_plot(
        stats, x_axis_name, y_axis_name, margin=config.margin, color=config.color, vertical_lines=config.boundaries,
    )


def plot_histogram(stats: pd.DataFrame, config: PlotConfig) -> go.Figure:
    x_axis_name, y_axis_name = _get_axis_names(
        config, default_x_axis_name='Value', default_y_axis_name='Number of fragments',
    )

    stats = _prepare_stats(stats, config, x_axis_name, y_axis_name)

    return create_histogram(
        stats,
        x_axis_name,
        y_axis_name,
        margin=config.margin,
        color=config.color,
        n_bins=config.n_bins,
        vertical_lines=config.boundaries,
    )


def _get_all_values_from_stats(stats: pd.DataFrame, column_name: str) -> List[int]:
    result = []
    stats.apply(lambda row: result.extend([row[VALUE]] * row[column_name]), axis=1)
    return result


def plot_boxplot(stats: pd.DataFrame, config: PlotConfig) -> go.Figure:
    x_axis_name, y_axis_name = _get_axis_names(
        config,
        default_x_axis_name="Category",
        default_y_axis_name='Values',
    )

    values = _get_all_values_from_stats(stats, config.column)

    if config.range_of_values is not None:
        values = list(filter(lambda elem: elem in config.range_of_values, values))

    values_df = pd.DataFrame.from_dict({x_axis_name: config.column, y_axis_name: values})

    return create_box_plot(values_df, x_axis_name, y_axis_name, horizontal_lines=config.boundaries)
