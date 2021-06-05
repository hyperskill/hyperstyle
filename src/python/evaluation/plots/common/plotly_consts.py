from enum import Enum


class MARGIN(Enum):
    ZERO = {'l': 0, 'r': 0, 'b': 0, 't': 0}


class SORT_ORDER(Enum):  # noqa: N801
    CATEGORY_ASCENDING = 'category ascending'
    CATEGORY_DESCENDING = 'category descending'
    TOTAL_ASCENDING = 'total ascending'
    TOTAL_DESCENDING = 'total descending'
