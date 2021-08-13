import argparse
import sys
from enum import Enum, unique
from pathlib import Path
from typing import Any, Callable, Dict, Union

sys.path.append('../../../..')

import plotly.graph_objects as go
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.inspectors.common.statistics import (
    GeneralInspectorsStatistics,
    IssuesStatistics,
    PenaltyInfluenceStatistics,
)
from src.python.evaluation.inspectors.print_inspectors_statistics import gather_statistics
from src.python.evaluation.plots.common import plotly_consts
from src.python.evaluation.plots.common.utils import get_supported_extensions, save_plot
from src.python.evaluation.plots.plotters.diffs_plotters import (
    get_issues_by_category,
    get_median_penalty_influence_by_category,
    get_penalty_influence_distribution,
    get_unique_issues_by_category,
)
from src.python.review.common.file_system import deserialize_data_from_file, Extension, parse_yaml


@unique
class ConfigFields(Enum):
    X_AXIS_NAME = 'x_axis_name'
    Y_AXIS_NAME = 'y_axis_name'
    LIMIT = 'limit'
    MARGIN = 'margin'
    SORT_ORDER = 'sort_order'
    COLOR = 'color'


X_AXIS_NAME = ConfigFields.X_AXIS_NAME.value
Y_AXIS_NAME = ConfigFields.Y_AXIS_NAME.value
LIMIT = ConfigFields.LIMIT.value
MARGIN = ConfigFields.MARGIN.value
SORT_ORDER = ConfigFields.SORT_ORDER.value
COLOR = ConfigFields.COLOR.value


@unique
class PlotTypes(Enum):
    UNIQUE_ISSUES_BY_CATEGORY = 'unique_issues_by_category'
    ISSUES_BY_CATEGORY = 'issues_by_category'
    UNIQUE_PENALTY_ISSUES_BY_CATEGORY = 'unique_penalty_issues_by_category'
    PENALTY_ISSUES_BY_CATEGORY = 'penalty_issues_by_category'
    MEDIAN_PENALTY_INFLUENCE_BY_CATEGORY = 'median_penalty_influence_by_category'
    PENALTY_INFLUENCE_DISTRIBUTION = 'penalty_influence_distribution'

    def to_plotter_function(self) -> Callable[..., go.Figure]:
        type_to_function = {
            PlotTypes.UNIQUE_ISSUES_BY_CATEGORY: get_unique_issues_by_category,
            PlotTypes.ISSUES_BY_CATEGORY: get_issues_by_category,
            PlotTypes.UNIQUE_PENALTY_ISSUES_BY_CATEGORY: get_unique_issues_by_category,
            PlotTypes.PENALTY_ISSUES_BY_CATEGORY: get_issues_by_category,
            PlotTypes.MEDIAN_PENALTY_INFLUENCE_BY_CATEGORY: get_median_penalty_influence_by_category,
            PlotTypes.PENALTY_INFLUENCE_DISTRIBUTION: get_penalty_influence_distribution,
        }

        return type_to_function[self]

    def extract_statistics(
        self,
        statistics: GeneralInspectorsStatistics,
    ) -> Union[IssuesStatistics, PenaltyInfluenceStatistics]:
        type_to_statistics = {
            PlotTypes.UNIQUE_ISSUES_BY_CATEGORY: statistics.new_issues_stat,
            PlotTypes.ISSUES_BY_CATEGORY: statistics.new_issues_stat,
            PlotTypes.UNIQUE_PENALTY_ISSUES_BY_CATEGORY: statistics.penalty_issues_stat,
            PlotTypes.PENALTY_ISSUES_BY_CATEGORY: statistics.penalty_issues_stat,
            PlotTypes.MEDIAN_PENALTY_INFLUENCE_BY_CATEGORY: statistics.penalty_influence_stat,
            PlotTypes.PENALTY_INFLUENCE_DISTRIBUTION: statistics.penalty_influence_stat,
        }

        return type_to_statistics[self]


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        RunToolArgument.DIFFS_FILE_PATH.value.long_name,
        type=lambda value: Path(value).absolute(),
        help=RunToolArgument.DIFFS_FILE_PATH.value.description,
    )

    parser.add_argument(
        'save_dir',
        type=lambda value: Path(value).absolute(),
        help='The directory where the plotted charts will be saved',
    )

    parser.add_argument(
        'config_path',
        type=lambda value: Path(value).absolute(),
        help='Path to the yaml file containing information about the graphs to be plotted.',
    )

    parser.add_argument(
        '--file-extension',
        type=str,
        default=Extension.SVG.value,
        choices=get_supported_extensions(),
        help='Allows you to select the extension of output files',
    )


def get_plot_params(config: Dict, plot_type: PlotTypes) -> Dict[str, Any]:
    config_params = config.get(plot_type.value)
    params = {}

    if config_params is None:
        return params

    if config_params.get(MARGIN) is not None:
        margin_value = config_params.get(MARGIN).upper()
        params[MARGIN] = plotly_consts.MARGIN[margin_value]

    if config_params.get(SORT_ORDER) is not None:
        sort_order_value = config_params.get(SORT_ORDER)
        params[SORT_ORDER] = plotly_consts.SORT_ORDER(sort_order_value)

    if config_params.get(LIMIT) is not None:
        params[LIMIT] = config_params.get(LIMIT)

    if config_params.get(X_AXIS_NAME) is not None:
        params[X_AXIS_NAME] = config_params.get(X_AXIS_NAME)

    if config_params.get(Y_AXIS_NAME) is not None:
        params[Y_AXIS_NAME] = config_params.get(Y_AXIS_NAME)

    if config_params.get(COLOR) is not None:
        color_value = config_params.get(COLOR)
        params[COLOR] = plotly_consts.COLOR[color_value]

    return params


def plot_and_save(
    config: Dict,
    general_statistics: GeneralInspectorsStatistics,
    save_dir: Path,
    extension: Extension,
) -> None:
    for plot_type in PlotTypes:
        if plot_type.value in config:
            params = get_plot_params(config, plot_type)
            plotter_function = plot_type.to_plotter_function()
            statistics = plot_type.extract_statistics(general_statistics)
            plot = plotter_function(statistics, **params)
            save_plot(plot, save_dir, plot_name=plot_type.value, extension=extension)


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    diffs = deserialize_data_from_file(args.diffs_file_path)
    general_statistics = gather_statistics(diffs)

    extension = Extension(args.file_extension)
    config = parse_yaml(args.config_path)

    plot_and_save(config, general_statistics, args.save_dir, extension)


if __name__ == '__main__':
    main()
