import logging
import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common.base_issue_converter import convert_base_issue
from hyperstyle.src.python.review.inspectors.flake8.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.flake8.issue_types import CODE_PREFIX_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

logger = logging.getLogger(__name__)

PATH_FLAKE8_CONFIG = Path(__file__).parent / '.flake8'
# To make the whitelist, a list of words was examined based on students' solutions
# that were flagged by flake8-spellcheck as erroneous. In general, the whitelist included those words
# that belonged to library methods and which were common abbreviations.
PATH_FLAKE8_SPELLCHECK_WHITELIST = Path(__file__).parent / 'whitelist.txt'
FORMAT = '%(path)s:%(row)d:%(col)d:%(code)s:%(text)s'
INSPECTOR_NAME = 'flake8'
BASE_COMMAND = [
    'flake8',
    f'--format={FORMAT}',
    f'--config={PATH_FLAKE8_CONFIG}',
    f'--whitelist={PATH_FLAKE8_SPELLCHECK_WHITELIST}',
    '--max-complexity', '0',
    '--cohesion-below', '100',
]


class Flake8Inspector(BaseInspector):
    inspector_type = InspectorType.FLAKE8

    @classmethod
    def inspect_in_memory(cls, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        output = run_in_subprocess(BASE_COMMAND + ['-'], subprocess_input=code)
        return cls.parse(output)

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        output = run_in_subprocess(BASE_COMMAND + [str(path)])
        return cls.parse(output)

    @classmethod
    def parse(cls, output: str) -> List[BaseIssue]:
        row_re = re.compile(r'^(.*):(\d+):(\d+):([A-Z]+\d{3}):(.*)$', re.M)
        issue_configs_handler = IssueConfigsHandler(*ISSUE_CONFIGS)

        issues: List[BaseIssue] = []
        for groups in row_re.findall(output):
            origin_class = groups[3]
            issue_type = cls.choose_issue_type(origin_class)

            base_issue = BaseIssue(
                origin_class=origin_class,
                type=issue_type,
                description=groups[4],
                file_path=Path(groups[0]),
                line_no=int(groups[1]),
                column_no=int(groups[2]) if int(groups[2]) > 0 else 1,
                inspector_type=cls.inspector_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            )

            issue = convert_base_issue(base_issue, issue_configs_handler)
            if issue is None:
                logger.error(f'{cls.inspector_type.value}: an error occurred during converting base issue.')
                continue

            issues.append(issue)

        return issues

    @staticmethod
    def choose_issue_type(code: str) -> IssueType:
        # Handling individual codes
        if code in CODE_TO_ISSUE_TYPE:
            return CODE_TO_ISSUE_TYPE[code]

        regex_match = re.match(r'^([A-Z]+)(\d)\d*$', code, re.IGNORECASE)
        code_prefix = regex_match.group(1)
        first_code_number = regex_match.group(2)

        # Handling other issues
        issue_type = (CODE_PREFIX_TO_ISSUE_TYPE.get(code_prefix + first_code_number)
                      or CODE_PREFIX_TO_ISSUE_TYPE.get(code_prefix))
        if not issue_type:
            logger.warning(f'flake8: {code} - unknown error code')
            return IssueType.BEST_PRACTICES

        return issue_type
