from enum import Enum


class MARGIN(Enum):
    ZERO = {'l': 0, 'r': 0, 'b': 0, 't': 0}


class SORT_ORDER(Enum):  # noqa: N801
    CATEGORY_ASCENDING = 'category ascending'
    CATEGORY_DESCENDING = 'category descending'
    TOTAL_ASCENDING = 'total ascending'
    TOTAL_DESCENDING = 'total descending'


class COLOR(Enum):
    # Colors from px.colors.DEFAULT_PLOTLY_COLORS
    BLUE = "rgb(31, 119, 180)"
    ORANGE = "rgb(255, 127, 14)"
    GREEN = "rgb(44, 160, 44)"
    RED = "rgb(214, 39, 40)"
    PURPLE = "rgb(148, 103, 189)"
    BROWN = "rgb(140, 86, 75)"
    PINK = "rgb(227, 119, 194)"
    GRAY = "rgb(127, 127, 127)"
    YELLOW = "rgb(188, 189, 34)"
    CYAN = "rgb(23, 190, 207)"
