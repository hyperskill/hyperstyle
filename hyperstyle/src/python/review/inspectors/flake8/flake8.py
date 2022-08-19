import logging
import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.flake8.issue_configs import IssueConfigs
from hyperstyle.src.python.review.inspectors.flake8.issue_types import CODE_PREFIX_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    get_issue_class_by_issue_type,
    get_measure_name_by_measurable_issue_type,
    IssueData,
    IssueDifficulty,
    IssueType,
    Measurable,
)
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

logger = logging.getLogger(__name__)

PATH_FLAKE8_CONFIG = Path(__file__).parent / '.flake8'
# To make the whitelist, a list of words was examined based on students' solutions
# that were flagged by flake8-spellcheck as erroneous. In general, the whitelist included those words
# that belonged to library methods and which were common abbreviations.
PATH_FLAKE8_SPELLCHECK_WHITELIST = Path(__file__).parent / 'whitelist.txt'
FORMAT = '%(path)s:%(row)d:%(col)d:%(code)s:%(text)s'
INSPECTOR_NAME = 'flake8'


class Flake8Inspector(BaseInspector):
    inspector_type = InspectorType.FLAKE8

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        command = [
            'flake8',
            f'--format={FORMAT}',
            f'--config={PATH_FLAKE8_CONFIG}',
            f'--whitelist={PATH_FLAKE8_SPELLCHECK_WHITELIST}',
            '--max-complexity', '0',
            '--cohesion-below', '100',
            path,
        ]
        output = run_in_subprocess(command)
        return cls.parse(output)

    @classmethod
    def parse(cls, output: str) -> List[BaseIssue]:
        row_re = re.compile(r'^(.*):(\d+):(\d+):([A-Z]+\d{3}):(.*)$', re.M)
        issues_handler = IssueConfigsHandler(*IssueConfigs)

        issues: List[BaseIssue] = []
        for groups in row_re.findall(output):
            origin_class = groups[3]
            description = groups[4]

            issue_data = IssueData.get_base_issue_data_dict(
                Path(groups[0]),
                cls.inspector_type,
                line_number=int(groups[1]),
                column_number=int(groups[2]) if int(groups[2]) > 0 else 1,
                origin_class=origin_class,
            )

            issue_type = cls.choose_issue_type(origin_class)

            issue_data[IssueData.ISSUE_TYPE.value] = issue_type
            issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
            issue_class = get_issue_class_by_issue_type(issue_type)

            if issubclass(issue_class, Measurable):
                measure = issues_handler.parse_measure(origin_class, description)
                if measure is None:
                    logger.error(f'{cls.inspector_type.value} - unable to parse measure.')
                    continue

                issue_data[get_measure_name_by_measurable_issue_type(issue_type)] = measure

            issue_data[IssueData.DESCRIPTION.value] = issues_handler.get_description(origin_class, description)

            issues.append(issue_class(**issue_data))

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
