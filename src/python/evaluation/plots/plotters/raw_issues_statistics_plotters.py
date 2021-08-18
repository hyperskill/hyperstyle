import logging
from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from src.python.evaluation.issues_statistics.get_raw_issues_statistics import VALUE
from src.python.evaluation.plots.common.utils import (
    COLOR,
    COLORWAY,
    create_box_plot,
    create_box_trace,
    create_histogram,
    create_line_chart,
    create_scatter_trace,
    LINES,
    MARGIN,
    update_figure,
)

logger = logging.getLogger(__name__)


@unique
class PlotTypes(Enum):
    LINE_CHART = 'line_chart'
    HISTOGRAM = 'histogram'
    BOX_PLOT = 'box_plot'

    def to_plotter_function(self) -> Callable[[Dict[str, pd.DataFrame], 'PlotConfig', bool], Dict[str, go.Figure]]:
        type_to_function = {
            PlotTypes.LINE_CHART: plot_line_chart,
            PlotTypes.HISTOGRAM: plot_histogram,
            PlotTypes.BOX_PLOT: plot_box_plot,
        }

        return type_to_function[self]


@dataclass
class PlotConfig:
    column: str
    type: PlotTypes
    x_axis_name: Optional[str] = None
    y_axis_name: Optional[str] = None
    margin: MARGIN = None
    color: COLOR = None
    colorway: COLORWAY = None
    boundaries: LINES = None
    range_of_values: Optional[range] = None
    n_bins: Optional[int] = None


def prepare_stats(
    stats: pd.DataFrame,
    column: str,
    range_of_values: Optional[range],
    x_axis_name: str,
    y_axis_name: str,
) -> pd.DataFrame:
    result_df = stats[[VALUE, column]]

    if range_of_values is not None:
        result_df = result_df[result_df[VALUE].isin(range_of_values)]

    result_df.set_index(VALUE, inplace=True)

    # Trim trailing zeros
    result_df = result_df.apply(lambda column: np.trim_zeros(column, trim='b')).dropna()

    # Fill in the missing intermediate values with zeros
    min_index, max_index = result_df.index.min(), result_df.index.max()
    if pd.isna(min_index) or pd.isna(max_index):
        logger.warning(f'{column}: no data')
    else:
        result_df = result_df.reindex(range(min_index, max_index + 1), fill_value=0)

    result_df.reset_index(inplace=True)

    return result_df.rename(columns={VALUE: x_axis_name, column: y_axis_name})


def _get_axis_names(
    *,
    x_axis_name: Optional[str],
    y_axis_name: Optional[str],
    default_x_axis_name: str,
    default_y_axis_name: str,
) -> Tuple[str, str]:
    new_x_axis_name = default_x_axis_name
    if x_axis_name is not None:
        new_x_axis_name = x_axis_name

    new_y_axis_name = default_y_axis_name
    if y_axis_name is not None:
        new_y_axis_name = y_axis_name

    return new_x_axis_name, new_y_axis_name


def plot_line_chart(
    stats_by_lang: Dict[str, pd.DataFrame],
    config: PlotConfig,
    group_stats: bool,
) -> Dict[str, go.Figure]:
    x_axis_name, y_axis_name = _get_axis_names(
        x_axis_name=config.x_axis_name,
        y_axis_name=config.y_axis_name,
        default_x_axis_name='Value',
        default_y_axis_name='Quantity',
    )

    if not group_stats:
        plots = {}
        for lang, stats in stats_by_lang.items():
            stats = prepare_stats(stats, config.column, config.range_of_values, x_axis_name, y_axis_name)
            plots[lang] = create_line_chart(
                stats,
                x_axis=x_axis_name,
                y_axis=y_axis_name,
                color=config.color,
                margin=config.margin,
                vertical_lines=config.boundaries,
            )
        return plots

    plot = go.Figure()
    for lang, stats in stats_by_lang.items():
        stats = prepare_stats(stats, config.column, config.range_of_values, x_axis_name, y_axis_name)
        trace = create_scatter_trace(stats, x_column=x_axis_name, y_column=y_axis_name)
        trace.name = lang
        plot.add_trace(trace)

    update_figure(
        plot,
        margin=config.margin,
        vertical_lines=config.boundaries,
        x_axis_name=x_axis_name,
        y_axis_name=y_axis_name,
        colorway=config.colorway,
    )

    return {'grouped': plot}


def plot_histogram(
    stats_by_lang: Dict[str, pd.DataFrame],
    config: PlotConfig,
    group_stats: bool,
) -> Dict[str, go.Figure]:
    x_axis_name, y_axis_name = _get_axis_names(
        x_axis_name=config.x_axis_name,
        y_axis_name=config.y_axis_name,
        default_x_axis_name='Value',
        default_y_axis_name='Quantity',
    )

    if group_stats:
        logger.info(f'{config.column}: the histogram cannot be grouped.')

    plots = {}
    for lang, stats in stats_by_lang.items():
        stats = prepare_stats(stats, config.column, config.range_of_values, x_axis_name, y_axis_name)
        plots[lang] = create_histogram(
            stats,
            x_axis_name,
            y_axis_name,
            margin=config.margin,
            color=config.color,
            n_bins=config.n_bins,
            vertical_lines=config.boundaries,
        )

    return plots


def _get_values_df(stats: pd.DataFrame, config: PlotConfig, x_axis_name: str, y_axis_name: str):
    values = []
    stats.apply(lambda row: values.extend([row[VALUE]] * row[config.column]), axis=1)

    if config.range_of_values is not None:
        values = [elem for elem in values if elem in config.range_of_values]

    return pd.DataFrame.from_dict({x_axis_name: config.column, y_axis_name: values})


def plot_box_plot(
    stats_by_lang: Dict[str, pd.DataFrame],
    config: PlotConfig,
    group_stats: bool,
) -> Dict[str, go.Figure]:
    x_axis_name, y_axis_name = _get_axis_names(
        x_axis_name=config.x_axis_name,
        y_axis_name=config.y_axis_name,
        default_x_axis_name='Category',
        default_y_axis_name='Values',
    )

    if not group_stats:
        plots = {}
        for lang, stats in stats_by_lang.items():
            values_df = _get_values_df(stats, config, x_axis_name, y_axis_name)

            plots[lang] = create_box_plot(
                values_df,
                x_axis=x_axis_name,
                y_axis=y_axis_name,
                color=config.color,
                margin=config.margin,
                horizontal_lines=config.boundaries,
            )
        return plots

    plot = go.Figure()
    for lang, stats in stats_by_lang.items():
        values_df = _get_values_df(stats, config, x_axis_name, y_axis_name)

        trace = create_box_trace(values_df, y_column=y_axis_name)
        trace.name = lang

        plot.add_trace(trace)

    update_figure(
        plot,
        margin=config.margin,
        horizontal_lines=config.boundaries,
        x_axis_name=x_axis_name,
        y_axis_name=y_axis_name,
        colorway=config.colorway,
    )

    return {'grouped': plot}
