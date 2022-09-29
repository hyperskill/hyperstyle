from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common.xml_parser import parse_xml_file_result
from hyperstyle.src.python.review.inspectors.eslint.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.eslint.issue_types import ESLINT_CLASS_NAME_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

PATH_ESLINT_CONFIG = Path(__file__).parent / '.eslintrc'


class ESLintInspector(BaseInspector):
    inspector_type = InspectorType.ESLINT

    # We don't support in-memory inspection for ESLint yet
    @classmethod
    def inspect_in_memory(cls, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        return []

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

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        issue_configs_handler = IssueConfigsHandler(*ISSUE_CONFIGS)
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)
            run_in_subprocess(command)

            issues = parse_xml_file_result(
                output_path,
                self.inspector_type,
                self.choose_issue_type,
                IssueDifficulty.get_by_issue_type,
                issue_configs_handler,
            )

            output_path.unlink()

            return issues

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:
        return ESLINT_CLASS_NAME_TO_ISSUE_TYPE.get(issue_class,
                                                   IssueType.CODE_STYLE)
