import json
from dataclasses import dataclass
from enum import Enum, unique
from typing import List


@dataclass(frozen=True)
class QodanaIssue:
    fragment_id: int
    line: int
    offset: int
    length: int
    highlighted_element: str
    description: str
    problem_id: str

    def to_json(self) -> str:
        issue = {
            QodanaJsonField.FRAGMENT_ID.value: self.fragment_id,
            QodanaJsonField.LINE.value: self.line,
            QodanaJsonField.OFFSET.value: self.offset,
            QodanaJsonField.LENGTH.value: self.length,
            QodanaJsonField.HIGHLIGHTED_ELEMENT.value: self.highlighted_element,
            QodanaJsonField.DESCRIPTION.value: self.description,
            QodanaJsonField.PROBLEM_ID.value: self.problem_id,
        }
        return json.dumps(issue)

    @classmethod
    def from_json(cls, str_json: str) -> 'QodanaIssue':
        issue = json.loads(str_json)
        return QodanaIssue(
            fragment_id=issue[QodanaJsonField.FRAGMENT_ID.value],
            line=issue[QodanaJsonField.LINE.value],
            offset=issue[QodanaJsonField.OFFSET.value],
            length=issue[QodanaJsonField.LENGTH.value],
            highlighted_element=issue[QodanaJsonField.HIGHLIGHTED_ELEMENT.value],
            description=issue[QodanaJsonField.DESCRIPTION.value],
            problem_id=issue[QodanaJsonField.PROBLEM_ID.value],
        )

    @classmethod
    def parse_list_issues_from_json(cls, str_json: str) -> List['QodanaIssue']:
        return list(map(lambda i: QodanaIssue.from_json(i), json.loads(str_json)[QodanaJsonField.ISSUES.value]))


@unique
class QodanaColumnName(Enum):
    INSPECTIONS = 'inspections'
    ID = 'id'
    INSPECTION_ID = 'inspection_id'
    COUNT_ALL = 'count_all'
    COUNT_UNIQUE = 'count_unique'


@unique
class QodanaJsonField(Enum):
    FRAGMENT_ID = 'fragment_id'
    LINE = 'line'
    OFFSET = 'offset'
    LENGTH = 'length'
    HIGHLIGHTED_ELEMENT = 'highlighted_element'
    DESCRIPTION = 'description'
    PROBLEM_ID = 'problem_id'

    ISSUES = 'issues'
