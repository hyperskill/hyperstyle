from pathlib import Path
from typing import List

from src.python.review.common.file_system import new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.eslint.issue_types import ESLINT_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.inspectors.parsers.checkstyle_parser import parse_checkstyle_file_result

PATH_ESLINT_CONFIG = Path(__file__).parent / '.eslintrc'


class ESLintInspector(BaseInspector):
    inspector_type = InspectorType.ESLINT

    origin_class_to_pattern = {
        'complexity':
            r'complexity of (\d+)'
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path) -> List[str]:
        local_path = 'node_modules/.bin/eslint'  # used only in local dev environment
        eslint_command = local_path if Path(local_path).exists() else 'eslint'
        return [
            eslint_command,
            '-c', PATH_ESLINT_CONFIG,
            '-f', 'checkstyle',
            '-o', output_path,
            path,
        ]

    def inspect(self, path: Path, config: typing.Dict) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)
            run_in_subprocess(command)

            issues = parse_checkstyle_file_result(output_path,
                                                  self.inspector_type,
                                                  self.choose_issue_type,
                                                  self.origin_class_to_pattern)

            output_path.unlink()

            return issues

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:
        return ESLINT_CLASS_NAME_TO_ISSUE_TYPE.get(issue_class,
                                                   IssueType.CODE_STYLE)
