import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common.base_issue_converter import convert_base_issue
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler
from hyperstyle.src.python.review.inspectors.pylint.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.pylint.issue_types import CATEGORY_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE

logger = logging.getLogger(__name__)

MSG_TEMPLATE = '{abspath}:{line}:{column}:{msg_id}:{msg}'
PATH_PYLINT_CONFIG = Path(__file__).parent / 'pylintrc'

FATAL_CATEGORY = 'F'
INFO_CATEGORY = 'I'

BASE_COMMAND = [
    'pylint',
    '--load-plugins', 'pylint_django',
    f'--rcfile={PATH_PYLINT_CONFIG}',
    f'--msg-template={MSG_TEMPLATE}',
]


class PylintInspector(BaseInspector):
    inspector_type = InspectorType.PYLINT
    # noqa: SC100 TODO: Do not ignore complexity issues and add a complexity tip for R0915.
    supported_issue_types = (
        IssueType.CODE_STYLE,
        IssueType.BEST_PRACTICES,
        IssueType.ERROR_PRONE,
    )

    @classmethod
    def inspect_in_memory(cls, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        output = run_in_subprocess(BASE_COMMAND + ['--from-stdin'], subprocess_input=code)
        return cls.parse(output)

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        output = run_in_subprocess(BASE_COMMAND + [str(path)])
        return cls.parse(output)

    @classmethod
    def parse(cls, output: str) -> List[BaseIssue]:
        row_re = re.compile(r'^(.*):(\d+):(\d+):([IRCWEF]\d+):(.*)$', re.M)
        issue_configs_handler = IssueConfigsHandler(*ISSUE_CONFIGS)

        issues = []
        for groups in row_re.findall(output):
            if groups[1] == INFO_CATEGORY:
                continue

            if groups[1] == FATAL_CATEGORY:
                logger.error('pylint encountered fatal error')
                return issues

            origin_class = groups[3]
            issue_type = cls.choose_issue_type(origin_class)
            if issue_type not in cls.supported_issue_types:
                logger.error('pylint: unsupported issue type %s', issue_type.__name__)
                continue

            base_issue = BaseIssue(
                origin_class=origin_class,
                type=issue_type,
                description=groups[4],
                file_path=Path(groups[0]),
                line_no=int(groups[1]),
                column_no=int(groups[2]) + 1,
                inspector_type=cls.inspector_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            )

            issue = convert_base_issue(base_issue, issue_configs_handler)
            if issue is None:
                logger.error(f'{cls.inspector_type.value}: an error occurred during converting a base issue.')
                continue

            issues.append(issue)

        return issues

    @staticmethod
    def choose_issue_type(code: str) -> IssueType:
        if code in CODE_TO_ISSUE_TYPE:
            return CODE_TO_ISSUE_TYPE[code]

        issue_type: Optional[IssueType] = CATEGORY_TO_ISSUE_TYPE.get(code[0])
        if not issue_type:
            logger.warning(f'pylint: {code} - unknown error category')
            return IssueType.BEST_PRACTICES

        return issue_type
