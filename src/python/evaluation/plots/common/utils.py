import os
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.python.evaluation.plots.common import plotly_consts
from src.python.review.common.file_system import Extension


def get_supported_extensions() -> List[str]:
    extensions = Extension.get_image_extensions()
    extensions.append(Extension.JSON)
    return [extension.value for extension in extensions]


def create_bar_plot(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
) -> go.Figure:
    fig = px.bar(df, x=x_axis, y=y_axis, text=y_axis)
    update_figure(fig, margin, sort_order, color)
    return fig


def create_box_plot(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
    horizontal_lines: Optional[Dict[int, Optional[str]]] = None,
) -> go.Figure:
    fig = px.box(df, x=x_axis, y=y_axis)
    update_figure(fig, margin=margin, sort_order=sort_order, color=color, horizontal_lines=horizontal_lines)
    return fig


def create_line_plot(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    margin: Optional[plotly_consts.MARGIN] = None,
    color: Optional[plotly_consts.COLOR] = None,
    vertical_lines: Optional[Dict[int, Optional[str]]] = None,
) -> go.Figure:
    fig = px.line(df, x=x_axis, y=y_axis)
    update_figure(fig, margin=margin, color=color, vertical_lines=vertical_lines)
    return fig


def create_histogram(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    n_bins: Optional[int] = None,
    margin: Optional[plotly_consts.MARGIN] = None,
    color: Optional[plotly_consts.COLOR] = None,
    vertical_lines: Optional[Dict[int, Optional[str]]] = None,
) -> go.Figure:
    fig = px.histogram(df, x=x_axis, y=y_axis, nbins=n_bins)
    update_figure(
        fig, margin=margin, color=color, vertical_lines=vertical_lines, x_axis_name=x_axis, y_axis_name=y_axis,
    )
    return fig


def update_figure(
    fig: go.Figure,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
    horizontal_lines: Optional[Dict[int, Optional[str]]] = None,
    vertical_lines: Optional[Dict[int, Optional[str]]] = None,
    x_axis_name: Optional[str] = None,
    y_axis_name: Optional[str] = None,
) -> None:
    new_layout = {}

    if margin is not None:
        new_layout["margin"] = margin.value

    if sort_order is not None:
        new_layout["xaxis"] = {"categoryorder": sort_order.value}

    if x_axis_name is not None:
        new_layout['xaxis_title'] = x_axis_name

    if y_axis_name is not None:
        new_layout['yaxis_title'] = y_axis_name

    fig.update_layout(**new_layout)

    new_trace = {}

    if color is not None:
        new_trace["marker"] = {"color": color.value}

    fig.update_traces(**new_trace)

    if horizontal_lines is not None:
        for y, annotation in horizontal_lines.items():
            fig.add_hline(y=y, annotation_text=annotation)

    if vertical_lines is not None:
        for x, annotation in vertical_lines.items():
            fig.add_vline(x=x, annotation_text=annotation)


def save_plot(
    fig: go.Figure,
    dir_path: Path,
    plot_name: str = "result_plot",
    extension: Extension = Extension.SVG,
) -> None:
    os.makedirs(dir_path, exist_ok=True)
    file = dir_path / f"{plot_name}{extension.value}"
    fig.write_image(str(file))
