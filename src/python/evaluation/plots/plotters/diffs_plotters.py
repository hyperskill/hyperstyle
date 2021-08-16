from statistics import median
from typing import Any, Callable, Dict, Optional

import pandas as pd
import plotly.graph_objects as go
from src.python.evaluation.inspectors.common.statistics import IssuesStatistics, PenaltyInfluenceStatistics
from src.python.evaluation.plots.common import plotly_consts
from src.python.evaluation.plots.common.utils import create_bar_plot, create_box_plot
from src.python.review.inspectors.issue import IssueType


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


def _extract_stats_from_issues_statistics(
    statistics: IssuesStatistics,
    limit: int,
    only_unique: bool,
) -> Dict[IssueType, int]:
    categorized_statistics = statistics.get_short_categorized_statistics()

    # If you want to get only unique issues, you should use position 0 of the tuple, otherwise 1.
    position = int(not only_unique)

    return {
        issue_type: stat[position] for issue_type, stat in categorized_statistics.items() if stat[position] >= limit
    }


def get_unique_issues_by_category(
    statistics: IssuesStatistics,
    x_axis_name: str = 'Categories',
    y_axis_name: str = 'Number of unique issues',
    limit: int = 0,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
) -> go.Figure:
    filtered_stats = _extract_stats_from_issues_statistics(statistics, limit, only_unique=True)

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
    )

    return create_bar_plot(
        df,
        x_axis=x_axis_name,
        y_axis=y_axis_name,
        margin=margin,
        sort_order=sort_order,
        color=color,
    )


def get_issues_by_category(
    statistics: IssuesStatistics,
    x_axis_name: str = 'Categories',
    y_axis_name: str = 'Number of issues',
    limit: int = 0,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
) -> go.Figure:
    filtered_stats = _extract_stats_from_issues_statistics(statistics, limit, only_unique=False)

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
    )

    return create_bar_plot(
        df,
        x_axis=x_axis_name,
        y_axis=y_axis_name,
        margin=margin,
        sort_order=sort_order,
        color=color,
    )


def get_median_penalty_influence_by_category(
    statistics: PenaltyInfluenceStatistics,
    x_axis_name: str = 'Categories',
    y_axis_name: str = 'Penalty influence (%)',
    limit: int = 0,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
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

    return create_bar_plot(
        df,
        x_axis=x_axis_name,
        y_axis=y_axis_name,
        margin=margin,
        sort_order=sort_order,
        color=color,
    )


def get_penalty_influence_distribution(
    statistics: PenaltyInfluenceStatistics,
    x_axis_name: str = 'Categories',
    y_axis_name: str = 'Penalty influence (%)',
    limit: int = 0,
    margin: Optional[plotly_consts.MARGIN] = None,
    sort_order: Optional[plotly_consts.SORT_ORDER] = None,
    color: Optional[plotly_consts.COLOR] = None,
):
    stat = statistics.stat
    filtered_stats = {issue_type: influence for issue_type, influence in stat.items() if len(influence) >= limit}

    df = _get_dataframe_from_dict(
        filtered_stats,
        key_name=x_axis_name,
        value_name=y_axis_name,
        key_mapper=lambda issue_type: issue_type.name,
    )
    df = df.explode(y_axis_name)

    return create_box_plot(
        df,
        x_axis=x_axis_name,
        y_axis=y_axis_name,
        margin=margin,
        sort_order=sort_order,
        color=color,
    )
