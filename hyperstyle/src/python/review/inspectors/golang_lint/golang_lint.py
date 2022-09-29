import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import check_set_up_env_variable, new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common.base_issue_converter import convert_base_issue
from hyperstyle.src.python.review.inspectors.common.utils import is_result_file_correct
from hyperstyle.src.python.review.inspectors.golang_lint.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.golang_lint.issue_types import (
    CODE_PREFIX_TO_ISSUE_TYPE,
    CODE_TO_ISSUE_TYPE,
)
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

GOLANG_LINT_DIRECTORY_ENV = 'GOLANG_LINT_DIRECTORY'
GOLANG_LINT_CONFIG_PATH = Path(__file__).parent / 'config.yml'

logger = logging.getLogger(__name__)


class GolangLintInspector(BaseInspector):
    inspector_type = InspectorType.GOLANG_LINT

    # We don't support in-memory inspection for Golang yet
    @classmethod
    def inspect_in_memory(cls, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        return []

    @classmethod
    def _create_command(cls, input_path: Path, output_path: Path, working_directory: Path, n_cpu: int) -> List[str]:
        path_to_golang_lint_cli = os.path.join(os.environ[GOLANG_LINT_DIRECTORY_ENV], 'golangci-lint')
        # In order to analyze a folder recursively, you must add '...'.
        input_path = input_path if input_path.is_file() else input_path / '...'

        return [
            path_to_golang_lint_cli,
            'run',
            str(input_path),
            '--path-prefix',
            working_directory,
            '--out-format',
            f'json:{output_path}',
            '-c',
            GOLANG_LINT_CONFIG_PATH,
            '--go',
            '1.18',
            '--concurrency',
            str(n_cpu),
            '--allow-parallel-runners',
        ]

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        if not check_set_up_env_variable(GOLANG_LINT_DIRECTORY_ENV):
            return []

        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.json'
            working_directory = path.parent if path.is_file() else path

            command = self._create_command(path, output_path, working_directory, config['n_cpu'])
            run_in_subprocess(command, working_directory)

            return self.parse(output_path)

    @classmethod
    def parse(cls, output_path: Path) -> List[BaseIssue]:
        if not is_result_file_correct(output_path, cls.inspector_type):
            return []

        with open(output_path) as file:
            data = json.load(file)

        metalinter_description_re = re.compile(r'^([A-Za-z\-]+\d*): (.*)$')
        issue_configs_handler = IssueConfigsHandler(*ISSUE_CONFIGS)

        issues = []
        files_with_typecheck_issues = set()
        for issue_json_data in data['Issues']:
            origin_class = issue_json_data['FromLinter']
            description = issue_json_data['Text']
            file_path = Path(issue_json_data['Pos']['Filename']).resolve()

            # Skip 'typecheck' errors, as they are related to syntax errors.
            if origin_class == 'typecheck':
                # If we find 'typecheck' in the file for the first time, we should log an error message.
                if file_path not in files_with_typecheck_issues:
                    logger.error(
                        f"{cls.inspector_type.value}: there is a syntax error in the file '{file_path}'. "
                        f"Error message: {description}.",
                    )
                    files_with_typecheck_issues.add(file_path)

                continue

            # Some inspections may show additional related information as a separate issue, so such issues are skipped.
            if '(related information)' in description:
                continue

            # If the issue is from the metalinter, we need to extract
            # the issue code from the description and add it to origin_class.
            if cls._is_metalinter_issue(origin_class):
                matches = metalinter_description_re.search(description)
                if matches:
                    issue_code, description = matches.groups()
                    description = description[:1].upper() + description[1:]
                    origin_class += f'-{issue_code}'

            issue_type = cls.choose_issue_type(origin_class)

            base_issue = BaseIssue(
                origin_class=origin_class,
                type=issue_type,
                description=description,
                file_path=file_path,
                line_no=issue_json_data['Pos']['Line'],
                column_no=issue_json_data['Pos']['Column'] if issue_json_data['Pos']['Column'] > 0 else 1,
                inspector_type=cls.inspector_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            )

            issue = convert_base_issue(base_issue, issue_configs_handler)
            if issue is None:
                logger.error(f'{cls.inspector_type.value}: an error occurred during converting base issue.')
                continue

            issues.append(issue)

        return issues

    @classmethod
    def choose_issue_type(cls, code: str) -> IssueType:
        if code in CODE_TO_ISSUE_TYPE:
            return CODE_TO_ISSUE_TYPE[code]

        for code_prefix, issue_type in CODE_PREFIX_TO_ISSUE_TYPE.items():
            if code.startswith(code_prefix):
                return issue_type

        logger.warning(f'{cls.inspector_type.value}: {code} - unknown error code')
        return IssueType.BEST_PRACTICES

    @staticmethod
    def _is_metalinter_issue(origin_class: str) -> bool:
        return origin_class in {'govet', 'revive', 'gocritic', 'gosimple', 'staticcheck', 'stylecheck'}
