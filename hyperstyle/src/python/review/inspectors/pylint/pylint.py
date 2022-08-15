import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import CodeIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.pylint.issue_types import CATEGORY_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.tips import add_complexity_tip

logger = logging.getLogger(__name__)

MSG_TEMPLATE = '{abspath}:{line}:{column}:{msg_id}:{msg}'
PATH_PYLINT_CONFIG = Path(__file__).parent / 'pylintrc'


class PylintInspector(BaseInspector):
    inspector_type = InspectorType.PYLINT
    supported_issue_types = (
        IssueType.CODE_STYLE,
        IssueType.BEST_PRACTICES,
        IssueType.ERROR_PRONE,
    )

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[CodeIssue]:
        command = [
            'pylint',
            '--load-plugins', 'pylint_django',
            f'--rcfile={PATH_PYLINT_CONFIG}',
            f'--msg-template={MSG_TEMPLATE}',
            str(path),
        ]

        output = run_in_subprocess(command)
        return cls.parse(output)

    @classmethod
    def parse(cls, output: str) -> List[CodeIssue]:
        fatal_category = 'F'
        info_category = 'I'
        row_re = re.compile(r'^(.*):(\d+):(\d+):([IRCWEF]\d+):(.*)$', re.M)

        issues: List[CodeIssue] = []

        for groups in row_re.findall(output):
            if groups[1] == info_category:
                continue

            if groups[1] == fatal_category:
                logger.error('pylint encountered fatal error')
                return issues

            origin_class = groups[3]
            description = groups[4]
            if origin_class == 'R0915':
                description = add_complexity_tip(description)
            elif origin_class == 'W1404':
                description = 'Found implicit string concatenation. If you want to concatenate strings, use "+".'
            elif origin_class == 'R1721':
                description = (
                    'Unnecessary use of a comprehension. Instead of using an identity comprehension, '
                    'consider using the list, dict or set constructor. It is faster and simpler. '
                    'For example, instead of {key: value for key, value in list_of_tuples} use dict(list_of_tuples).'
                )

            issue_type = cls.choose_issue_type(groups[3])
            if issue_type not in cls.supported_issue_types:
                logger.error('pylint: unsupported issue type %s', issue_type.__name__)
                continue

            issues.append(CodeIssue(
                file_path=Path(groups[0]),
                line_no=int(groups[1]),
                column_no=int(groups[2]) + 1,
                origin_class=origin_class,
                description=description,
                inspector_type=cls.inspector_type,
                type=issue_type,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            ))

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
