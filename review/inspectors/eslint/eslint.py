from pathlib import Path
from typing import List

from review.common.file_system import new_temp_dir
from review.common.subprocess_runner import run_in_subprocess
from review.inspectors.base_inspector import BaseInspector
from review.inspectors.eslint.issue_types import ESLINT_CLASS_NAME_TO_ISSUE_TYPE
from review.inspectors.inspector_type import InspectorType
from review.inspectors.issue import BaseIssue, IssueType
from review.inspectors.parsers.checkstyle_parser import parse_checkstyle_file_result

PATH_ESLINT_CONFIG = Path(__file__).parent / '.eslintrc'


class ESLintInspector(BaseInspector):
    inspector_type = InspectorType.ESLINT

    origin_class_to_pattern = {
        'complexity':
            r'complexity of (\d+)'
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path) -> List[str]:
        return [
            'eslint',
            '-c', PATH_ESLINT_CONFIG,
            '-f', 'checkstyle',
            '-o', output_path,
            path,
        ]

    def inspect(self, path: Path, config: dict) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)
            run_in_subprocess(command)

            issues = parse_checkstyle_file_result(output_path,
                                                  self.inspector_type,
                                                  self.choose_issue_type,
                                                  self.origin_class_to_pattern)

            return issues

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:
        return ESLINT_CLASS_NAME_TO_ISSUE_TYPE.get(issue_class,
                                                   IssueType.CODE_STYLE)
