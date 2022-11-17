from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from pathlib import Path
from typing import List

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

    def to_base_issue(self, file_path: Path) -> BaseIssue:
        return BaseIssue(
            origin_class='',
            type=IssueType.CODE_STYLE,  # TODO: make mapping
            description=self.name,
            file_path=file_path,
            line_no=self.line_number,
            column_no=self.offset,
            inspector_type=InspectorType.IJ,
            difficulty=IssueDifficulty.HARD,  # TODO: make mapping
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class IJInspectionResult:
    problems: List[IJProblem]

    def to_base_issues(self, file_path: Path) -> List[BaseIssue]:
        return [problem.to_base_issue(file_path) for problem in self.problems]
