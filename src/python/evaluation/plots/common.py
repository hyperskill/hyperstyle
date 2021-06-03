from enum import Enum
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.python.review.common.file_system import create_directory


class Extension(Enum):
    PNG = '.png'
    JPG = '.jpg'
    JPEG = '.jpeg'
    WEBP = '.webp'
    SVG = '.svg'
    PDF = '.pdf'
    EPS = '.eps'
    JSON = '.json'


def create_bar_plot(df: pd.DataFrame, x_axis: str, y_axis: str) -> go.Figure:
    fig = px.bar(df, x=x_axis, y=y_axis, text=y_axis)

    fig.update_layout(
        xaxis={"categoryorder": "total descending"},
        margin=dict(l=0, r=0, b=0, t=0),
    )

    return fig


def create_box_plot(df: pd.DataFrame, x_axis: str, y_axis: str) -> go.Figure:
    fig = px.box(df, x=x_axis, y=y_axis)

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

    return fig


def save_plot(
    fig: go.Figure, dir_path: Path, plot_name: str = "result_plot", extension: Extension = Extension.SVG
) -> None:
    create_directory(dir_path)
    file = dir_path / f"{plot_name}{extension.value}"
    fig.write_image(str(file))
