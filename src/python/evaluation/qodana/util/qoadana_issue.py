from dataclasses import dataclass


@dataclass(frozen=True)
class QodanaIssue:
    fragment_id: int
    line: int
    offset: int
    length: int
    highlighted_element: str
    description: str
