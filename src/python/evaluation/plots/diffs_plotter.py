import argparse
from pathlib import Path
from statistics import median
from typing import Any, Callable, Dict

import pandas as pd
import plotly.graph_objects as go
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.inspectors.common.statistics import IssuesStatistics, PenaltyInfluenceStatistics
from src.python.evaluation.inspectors.print_inspectors_statistics import gather_statistics
from src.python.evaluation.plots.common import create_bar_plot, create_box_plot, save_plot
from src.python.review.common.file_system import create_directory, deserialize_data_from_file


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        RunToolArgument.DIFFS_FILE_PATH.value.long_name,
        type=lambda value: Path(value).absolute(),
        help=RunToolArgument.DIFFS_FILE_PATH.value.description,
    )

    parser.add_argument(
        "save_dir",
        type=lambda value: Path(value).absolute(),
        help="The directory where the plotted charts will be saved",
    )


def _get_dataframe_from_dict(
    data_dict: Dict[Any, Any],
    key_name: str,
    value_name: str,
    key_mapper: Callable = lambda x: x,
    value_mapper: Callable = lambda y: y,
):
    """
    Converts 'data_dict' to a dataframe consisting of two columns: 'key_name', 'value_name'.
    'key_name' contains all keys of 'data_dict', 'value_name' contains all corresponding
    values of 'data_dict'. With the functions 'key_mapper' and 'value_mapper' you can
    additionally convert keys and values respectively.
    """
    converted_dict = {
        key_name: list(map(key_mapper, data_dict.keys())),
        value_name: list(map(value_mapper, data_dict.values())),
    }

    return pd.DataFrame.from_dict(converted_dict)


def get_unique_issues_by_category(
    statistics: IssuesStatistics,
    x_axis_name: str = "Categories",
    y_axis_name: str = "Number of unique issues",
    limit: int = 0,
) -> go.Figure:
    categorized_statistics = statistics.get_short_categorized_statistics()
    filtered_stats = {issue_type: stat[0] for issue_type, stat in categorized_statistics.items() if stat[0] >= limit}

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
    )

    return create_bar_plot(df, x_axis_name, y_axis_name)


def get_issues_by_category(
    statistics: IssuesStatistics,
    x_axis_name: str = "Categories",
    y_axis_name: str = "Number of issues",
    limit: int = 0,
) -> go.Figure:
    categorized_statistics = statistics.get_short_categorized_statistics()
    filtered_stats = {issue_type: stat[1] for issue_type, stat in categorized_statistics.items() if stat[1] >= limit}

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
    )

    return create_bar_plot(df, x_axis_name, y_axis_name)


def get_median_penalty_influence_by_category(
    statistics: PenaltyInfluenceStatistics,
    x_axis_name: str = "Categories",
    y_axis_name: str = "Penalty influence (%)",
    limit: int = 0,
) -> go.Figure:
    stat = statistics.stat
    filtered_stats = {issue_type: influence for issue_type, influence in stat.items() if median(influence) >= limit}

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
        value_mapper=lambda influence: median(influence),
    )

    return create_bar_plot(df, x_axis_name, y_axis_name)


def get_penalty_influence_distribution(
    statistics: PenaltyInfluenceStatistics, x_axis_name: str = "Categories", y_axis_name: str = "Penalty influence (%)",
):
    stat = statistics.stat

    df = _get_dataframe_from_dict(
        stat, key_name=x_axis_name, value_name=y_axis_name, key_mapper=lambda issue_type: issue_type.name,
    )
    df = df.explode(y_axis_name)

    return create_box_plot(df, x_axis_name, y_axis_name)


def main():
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    diffs = deserialize_data_from_file(args.diffs_file_path)
    statistics = gather_statistics(diffs)

    create_directory(args.save_dir)

    plot = get_unique_issues_by_category(statistics.new_issues_stat)
    save_plot(plot, args.save_dir, plot_name="unique-issues-by-category")

    plot = get_issues_by_category(statistics.new_issues_stat)
    save_plot(plot, args.save_dir, plot_name="issues-by-category")

    plot = get_unique_issues_by_category(statistics.penalty_issues_stat, y_axis_name="Number of unique penalty issues")
    save_plot(plot, args.save_dir, plot_name="unique-penalty-issues-by-category")

    plot = get_issues_by_category(statistics.penalty_issues_stat, y_axis_name="Number of penalty issues")
    save_plot(plot, args.save_dir, plot_name="penalty-issues-by-category")

    plot = get_median_penalty_influence_by_category(statistics.penalty_influence_stat)
    save_plot(plot, args.save_dir, plot_name="median-penalty-influence-by-category")

    plot = get_penalty_influence_distribution(statistics.penalty_influence_stat)
    save_plot(plot, args.save_dir, plot_name="penalty_influence_distribution")


if __name__ == "__main__":
    main()
