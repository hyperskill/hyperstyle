import os
from pathlib import Path
from typing import List, Optional

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
) -> go.Figure:
    fig = px.box(df, x=x_axis, y=y_axis)
    update_figure(fig, margin, sort_order, color)
    return fig


def update_figure(
    fig: go.Figure,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
) -> None:
    new_layout = {}

    if margin is not None:
        new_layout["margin"] = margin.value

    if sort_order is not None:
        new_layout["xaxis"] = {"categoryorder": sort_order.value}

    fig.update_layout(**new_layout)

    new_trace = {}

    if color is not None:
        new_trace["marker"] = {"color": color.value}

    fig.update_traces(**new_trace)


def save_plot(
    fig: go.Figure,
    dir_path: Path,
    plot_name: str = "result_plot",
    extension: Extension = Extension.SVG,
) -> None:
    os.makedirs(dir_path, exist_ok=True)
    file = dir_path / f"{plot_name}{extension.value}"
    fig.write_image(str(file))
