import os
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
    def _get_eslint_local_path(cls) -> str:
        common_path = 'node_modules/.bin/eslint'
        standard_path = f'./{common_path}'
        prod_path = f'./review/{common_path}'
        if os.path.exists(standard_path):
            return standard_path
        elif os.path.exists(prod_path):
            return prod_path
        raise FileNotFoundError('Eslint was not configured!')

    @classmethod
    def _create_command(cls, path: Path, output_path: Path, is_local: bool = False) -> List[str]:
        eslint_command = 'eslint' if not is_local else cls._get_eslint_local_path()
        return [
            eslint_command,
            '-c', PATH_ESLINT_CONFIG,
            '-f', 'checkstyle',
            '-o', output_path,
            path,
        ]

    def inspect(self, path: Path, config: dict, is_local: bool = False) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path, is_local)
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
