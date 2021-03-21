import logging
import re
from pathlib import Path
from typing import List

from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.flake8.issue_types import CODE_PREFIX_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE, \
    WPS_RANGE_TO_ISSUE_TYPE
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, CodeIssue, CyclomaticComplexityIssue, IssueType, IssueData
from src.python.review.inspectors.tips import get_cyclomatic_complexity_tip

logger = logging.getLogger(__name__)

PATH_FLAKE8_CONFIG = Path(__file__).parent / '.flake8'
FORMAT = '%(path)s:%(row)d:%(col)d:%(code)s:%(text)s'
INSPECTOR_NAME = 'flake8'


class Flake8Inspector(BaseInspector):
    inspector_type = InspectorType.FLAKE8

    @classmethod
    def inspect(cls, path: Path, config: dict) -> List[BaseIssue]:
        command = [
            'flake8',
            f'--format={FORMAT}',
            f'--config={PATH_FLAKE8_CONFIG}',
            '--max-complexity', '0',
            path
        ]
        output = run_in_subprocess(command)
        return cls.parse(output)

    @classmethod
    def parse(cls, output: str) -> List[BaseIssue]:
        row_re = re.compile(r'^(.*):(\d+):(\d+):([A-Z]+\d{3}):(.*)$', re.M)
        cc_description_re = re.compile(r"'(.+)' is too complex \((\d+)\)")

        issues: List[BaseIssue] = []
        for groups in row_re.findall(output):
            description = groups[4]
            origin_class = groups[3]
            cc_match = cc_description_re.match(description)
            file_path = Path(groups[0])
            line_no = int(groups[1])

            issue_data = IssueData.get_base_issue_data_dict(file_path, cls.inspector_type, line_number=line_no,
                                                            column_number=int(groups[2]) if int(groups[2]) > 0 else 1,
                                                            origin_class=origin_class)
            if cc_match is not None:
                issue_data['description'] = get_cyclomatic_complexity_tip()
                issue_data['cc_value'] = int(cc_match.groups()[1])
                issue_data['type'] = IssueType.CYCLOMATIC_COMPLEXITY
                issues.append(CyclomaticComplexityIssue(**issue_data))
            else:
                issue_type = cls.choose_issue_type(origin_class)
                issue_data['type'] = issue_type
                issue_data['description'] = description
                issues.append(CodeIssue(**issue_data))

        return issues

    @staticmethod
    def choose_issue_type(code: str) -> IssueType:
        # Handling individual codes
        if code in CODE_TO_ISSUE_TYPE:
            return CODE_TO_ISSUE_TYPE[code]

        regex_match = re.match(r'^([a-z]+)(\d+)$', code, re.IGNORECASE)
        code_prefix = regex_match.group(1)

        # Handling WPS issues
        if code_prefix == "WPS":
            code_number = int(regex_match.group(2))
            for wps_range, issue_type in WPS_RANGE_TO_ISSUE_TYPE.items():
                if code_number in wps_range:
                    return issue_type

        # Handling other issues
        issue_type = CODE_PREFIX_TO_ISSUE_TYPE.get(code_prefix)
        if not issue_type:
            logger.warning(f'flake8: {code} - unknown error code')
            return IssueType.BEST_PRACTICES

        return issue_type
