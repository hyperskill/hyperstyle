import os
from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.python.evaluation.plots import plotly_consts
from src.python.review.common.file_system import Extension


def get_supported_image_extensions() -> List[str]:
    extensions = Extension.get_image_extensions()
    extensions.append(Extension.JSON)
    return [extension.value for extension in extensions]


def create_bar_plot(
    df: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    margin: plotly_consts.MARGIN = plotly_consts.MARGIN.ZERO,
    sort_order: plotly_consts.SORT_ORDER = plotly_consts.SORT_ORDER.TOTAL_DESCENDING,
) -> go.Figure:
    fig = px.bar(df, x=x_axis, y=y_axis, text=y_axis)

    fig.update_layout(
        xaxis={'categoryorder': sort_order},
        margin=margin,
    )

    return fig


def create_box_plot(
    df: pd.DataFrame, x_axis: str, y_axis: str, margin: plotly_consts.MARGIN = plotly_consts.MARGIN.ZERO,
) -> go.Figure:
    fig = px.box(df, x=x_axis, y=y_axis)

    fig.update_layout(margin=margin)

    return fig


def save_plot(
    fig: go.Figure,
    dir_path: Path,
    plot_name: str = "result_plot",
    extension: Extension = Extension.SVG,
) -> None:
    os.makedirs(dir_path, exist_ok=True)
    file = dir_path / f"{plot_name}{extension.value}"
    fig.write_image(str(file))
