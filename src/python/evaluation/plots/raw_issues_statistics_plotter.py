import argparse
import sys
from enum import Enum, unique
from pathlib import Path
from typing import Dict, List, Optional

sys.path.append('../../../..')

import plotly.graph_objects as go
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.plots.common import plotly_consts
from src.python.evaluation.plots.common.utils import (
    get_supported_extensions,
    save_plot,
)
from src.python.evaluation.plots.plotters.raw_issues_statistics_plotters import PlotConfig, PlotTypes
from src.python.review.common.file_system import Extension, parse_yaml


@unique
class ConfigFields(Enum):
    X_AXIS_NAME = 'x_axis_name'
    Y_AXIS_NAME = 'y_axis_name'
    MARGIN = 'margin'
    COLOR = 'color'
    COLORWAY = 'colorway'
    BOUNDARIES = 'boundaries'
    COMMON = 'common'
    STATS = 'stats'
    RANGE_OF_VALUES = 'range_of_values'
    N_BINS = 'n_bins'


X_AXIS_NAME = ConfigFields.X_AXIS_NAME.value
Y_AXIS_NAME = ConfigFields.Y_AXIS_NAME.value
MARGIN = ConfigFields.MARGIN.value
COLOR = ConfigFields.COLOR.value
COLORWAY = ConfigFields.COLORWAY.value
BOUNDARIES = ConfigFields.BOUNDARIES.value
COMMON = ConfigFields.COMMON.value
STATS = ConfigFields.STATS.value
RANGE_OF_VALUES = ConfigFields.RANGE_OF_VALUES.value
N_BINS = ConfigFields.N_BINS.value


def configure_arguments(parser: argparse.ArgumentParser) -> None:
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

    parser.add_argument(
        '--group-stats',
        action='store_true',
        help='If present, there will be several languages on the charts at once.',
    )


def _get_plot_config(
    column_name: str,
    plot_type: str,
    plot_config: Optional[Dict],
    common: Optional[Dict],
) -> PlotConfig:
    params = {'column': column_name, 'type': PlotTypes(plot_type.lower())}

    if common is not None:
        params.update(common)

    if plot_config is not None:
        params.update(plot_config)

    if MARGIN in params:
        margin_value = params.get(MARGIN).upper()
        params[MARGIN] = plotly_consts.MARGIN[margin_value]

    if COLOR in params:
        color_value = params.get(COLOR).upper()
        params[COLOR] = plotly_consts.COLOR[color_value]

    if RANGE_OF_VALUES in params:
        params[RANGE_OF_VALUES] = range(*params[RANGE_OF_VALUES])

    if COLORWAY in params:
        colorway_value = params.get(COLORWAY).upper()
        params[COLORWAY] = plotly_consts.COLORWAY[colorway_value]

    return PlotConfig(**params)


def get_plot_configs(column_name: str, column_config: Dict) -> List[PlotConfig]:
    common = column_config.pop(COMMON, None)

    plot_configs = []
    for plot_type, plot_config in column_config.items():
        plot_configs.append(_get_plot_config(column_name, plot_type, plot_config, common))

    return plot_configs


def _save_plots(plots: Dict[str, go.Figure], save_dir: Path, extension: Extension, column: str, plot_type: str) -> None:
    for output_name, plot in plots.items():
        subdir = save_dir / column
        save_plot(plot, subdir, plot_name=f'{column}_{plot_type}_{output_name}', extension=extension)


def plot_and_save(config: Dict, save_dir: Path, extension: Extension, group_stats: bool) -> None:
    stats_by_lang = {
        lang: get_solutions_df_by_file_path(Path(lang_stats)) for lang, lang_stats in config.pop(STATS).items()
    }

    for column_name, column_config in config.items():
        plot_configs = get_plot_configs(column_name, column_config)
        for plot_config in plot_configs:
            plotter_function = plot_config.type.to_plotter_function()
            plots = plotter_function(stats_by_lang, plot_config, group_stats)
            _save_plots(plots, save_dir, extension, plot_config.column, plot_config.type.value)


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    extension = Extension(args.file_extension)
    config = parse_yaml(args.config_path)

    plot_and_save(config, args.save_dir, extension, args.group_stats)


if __name__ == "__main__":
    main()
