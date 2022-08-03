import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import check_set_up_env_variable, new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.golang_lint.issue_types import (
    CODE_PREFIX_TO_ISSUE_TYPE,
    CODE_TO_ISSUE_TYPE,
)
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    CodeIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueData,
    IssueDifficulty,
    IssueType,
    LineLenIssue,
    MaintainabilityLackIssue,
)
from hyperstyle.src.python.review.inspectors.tips import (
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
    get_magic_number_tip,
    get_maintainability_index_tip,
)

GOLANG_LINT_DIRECTORY_ENV = 'GOLANG_LINT_DIRECTORY'
GOLANG_LINT_CONFIG_PATH = Path(__file__).parent / 'config.yml'

logger = logging.getLogger(__name__)


class GolangLint(BaseInspector):
    inspector_type = InspectorType.GOLANG_LINT

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
        with open(output_path) as file:
            data = json.load(file)

        description_re = re.compile(r'^([A-Za-z\-]+\d*):(.*)$')
        cc_description_re = re.compile(r'^calculated cyclomatic complexity for function .* is (\d+), max is -1$')
        func_len_description_re = re.compile(r"^Function '.*' is too long \((\d+) > 1\)$")
        line_len_description_re = re.compile(r'^line is (\d+) characters$')
        maintainability_description_re = re.compile(
            r'^Function name: .*, Cyclomatic Complexity: .*, Halstead Volume: .*, Maintainability Index: (.+)$',
        )

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

            # If the issue is from the metalinter, you need to extract
            # the issue code from the description and add it to origin_class.
            if origin_class in {'govet', 'revive', 'gocritic', 'gosimple', 'staticcheck', 'stylecheck'}:
                matches = description_re.findall(description)
                if matches:
                    issue_code, description = matches[0]
                    origin_class += f'-{issue_code}'

            issue_data = IssueData.get_base_issue_data_dict(
                file_path=file_path,
                inspector_type=cls.inspector_type,
                line_number=issue_json_data['Pos']['Line'],
                column_number=issue_json_data['Pos']['Column'] if issue_json_data['Pos']['Column'] > 0 else 1,
                origin_class=origin_class,
            )

            cc_match = cc_description_re.findall(description)
            func_len_match = func_len_description_re.findall(description)
            line_len_match = line_len_description_re.findall(description)
            maintainability_match = maintainability_description_re.findall(description)

            if cc_match:  # cyclop
                issue_type = IssueType.CYCLOMATIC_COMPLEXITY
                issue_data[IssueData.DESCRIPTION.value] = get_cyclomatic_complexity_tip()
                issue_data[IssueData.CYCLOMATIC_COMPLEXITY.value] = int(cc_match[0])
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(CyclomaticComplexityIssue(**issue_data))
            elif func_len_match:  # funlen
                issue_type = IssueType.FUNC_LEN
                issue_data[IssueData.DESCRIPTION.value] = get_func_len_tip()
                issue_data[IssueData.FUNCTION_LEN.value] = int(func_len_match[0])
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(FuncLenIssue(**issue_data))
            elif line_len_match:  # lll
                issue_type = IssueType.LINE_LEN
                issue_data[IssueData.DESCRIPTION.value] = get_line_len_tip()
                issue_data[IssueData.LINE_LEN.value] = int(line_len_match[0])
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(LineLenIssue(**issue_data))
            elif maintainability_match:  # maintidx
                issue_type = IssueType.MAINTAINABILITY
                maintainability_lack = convert_percentage_of_value_to_lack_of_value(float(maintainability_match[0]))
                issue_data[IssueData.DESCRIPTION.value] = get_maintainability_index_tip()
                issue_data[IssueData.MAINTAINABILITY_LACK.value] = maintainability_lack
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(MaintainabilityLackIssue(**issue_data))
            else:
                issue_type = cls.choose_issue_type(origin_class)
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)

                if origin_class == 'gomnd':
                    description = get_magic_number_tip(description)

                issue_data[IssueData.DESCRIPTION.value] = description
                issues.append(CodeIssue(**issue_data))

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
