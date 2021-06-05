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
    D3 = px.colors.qualitative.D3
    G10 = px.colors.qualitative.G10
    T10 = px.colors.qualitative.T10
    ALPHABET = px.colors.qualitative.Alphabet
    DARK24 = px.colors.qualitative.Dark24
    LIGHT24 = px.colors.qualitative.Light24
    ANTIQUE = px.colors.qualitative.Antique
    BOLD = px.colors.qualitative.Bold
    PASTEL = px.colors.qualitative.Pastel
    PASTEL1 = px.colors.qualitative.Pastel1
    PASTEL2 = px.colors.qualitative.Pastel2
    PRISM = px.colors.qualitative.Prism
    SAFE = px.colors.qualitative.Safe
    VIVID = px.colors.qualitative.Vivid
    SET1 = px.colors.qualitative.Set1
    SET2 = px.colors.qualitative.Set2
    SET3 = px.colors.qualitative.Set3
    DARK2 = px.colors.qualitative.Dark2
