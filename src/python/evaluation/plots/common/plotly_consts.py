from enum import Enum

import plotly.express as px


class MARGIN(Enum):
    ZERO = {'l': 0, 'r': 0, 'b': 0, 't': 0}


class SORT_ORDER(Enum):  # noqa: N801
    CATEGORY_ASCENDING = 'category ascending'
    CATEGORY_DESCENDING = 'category descending'
    TOTAL_ASCENDING = 'total ascending'
    TOTAL_DESCENDING = 'total descending'


class COLOR(Enum):
    """
    Colors from px.colors.DEFAULT_PLOTLY_COLORS
    """

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


class COLORWAY(Enum):  # noqa: N801
    """
    Colors from px.colors.qualitative
    """

    PLOTLY = px.colors.qualitative.Plotly
    D3 = px.colors.qualitative.D3
    G10 = px.colors.qualitative.G10
    T10 = px.colors.qualitative.T10
    ALPHABET = px.colors.qualitative.Alphabet
    DARK24 = px.colors.qualitative.Dark24
    LIGHT24 = px.colors.qualitative.Light24
    SET1 = px.colors.qualitative.Set1
    PASTEL1 = px.colors.qualitative.Pastel1
    DARK2 = px.colors.qualitative.Dark2
    SET2 = px.colors.qualitative.Set2
    PASTEL2 = px.colors.qualitative.Pastel2
    SET3 = px.colors.qualitative.Set3
    ANTIQUE = px.colors.qualitative.Antique
    BOLD = px.colors.qualitative.Bold
    PASTEL = px.colors.qualitative.Pastel
    PRISM = px.colors.qualitative.Prism
    SAFE = px.colors.qualitative.Safe
    VIVID = px.colors.qualitative.Vivid
