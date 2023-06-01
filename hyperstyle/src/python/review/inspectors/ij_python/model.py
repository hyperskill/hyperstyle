from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from pathlib import Path
from typing import List

from hyperstyle.src.python.review.inspectors.ij_python.issue_types import IJ_PYTHON_CODE_TO_ISSUE_TYPE, \
    ISSUE_TYPE_EXCEPTIONS
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IJCode:
    text: str
    language_id: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IJProblem:
    name: str
    inspector: str
    line_number: int
    offset: int
    length: int

    @staticmethod
    def choose_issue_type(inspector: str, description: str) -> IssueType:
        if inspector in ISSUE_TYPE_EXCEPTIONS:
            for key, value in ISSUE_TYPE_EXCEPTIONS[inspector].items():
                if description in key:
                    return value

        if inspector in IJ_PYTHON_CODE_TO_ISSUE_TYPE:
            return IJ_PYTHON_CODE_TO_ISSUE_TYPE[inspector]

        # PEP-8 inspection
        return IssueType.CODE_STYLE

    def to_base_issue(self, file_path: Path) -> BaseIssue:
        issue_type = self.choose_issue_type(self.inspector, self.name)
        return BaseIssue(
            origin_class=self.inspector,
            type=issue_type,
            description=self.name,
            file_path=file_path,
            line_no=self.line_number,
            column_no=self.offset,
            inspector_type=InspectorType.IJ,
            difficulty=IssueDifficulty.get_by_issue_type(issue_type),
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IJInspectionResult:
    problems: List[IJProblem]

    def to_base_issues(self, file_path: Path) -> List[BaseIssue]:
        return [problem.to_base_issue(file_path) for problem in self.problems]
