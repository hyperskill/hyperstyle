from dataclasses import dataclass
from enum import Enum, unique


@dataclass(frozen=True)
class QodanaIssue:
    fragment_id: int
    line: int
    offset: int
    length: int
    highlighted_element: str
    description: str
    problem_id: str


@unique
class QodanaColumnName(Enum):
    INSPECTIONS = 'inspections'
