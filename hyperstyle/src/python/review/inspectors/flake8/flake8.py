import logging
import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.flake8.issue_types import CODE_PREFIX_TO_ISSUE_TYPE, CODE_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    CodeIssue,
    CohesionIssue,
    CyclomaticComplexityIssue,
    IssueData,
    IssueDifficulty,
    IssueType,
    LineLenIssue,
)
from hyperstyle.src.python.review.inspectors.tips import (
    get_augmented_assign_pattern_tip, get_cohesion_tip, get_cyclomatic_complexity_tip, get_line_len_tip,
    get_magic_number_tip,
)

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
        cc_description_re = re.compile(r"'(.+)' is too complex \((\d+)\)")
        cohesion_description_re = re.compile(r"class has low \((\d*\.?\d*)%\) cohesion")
        line_len_description_re = re.compile(r"line too long \((\d+) > \d+ characters\)")

        issues: List[BaseIssue] = []
        for groups in row_re.findall(output):
            description = groups[4]
            origin_class = groups[3]
            cc_match = cc_description_re.match(description)
            cohesion_match = cohesion_description_re.match(description)
            line_len_match = line_len_description_re.match(description)
            file_path = Path(groups[0])
            line_no = int(groups[1])

            column_number = int(groups[2]) if int(groups[2]) > 0 else 1
            issue_data = IssueData.get_base_issue_data_dict(file_path,
                                                            cls.inspector_type,
                                                            line_number=line_no,
                                                            column_number=column_number,
                                                            origin_class=origin_class)
            if cc_match is not None:  # mccabe: cyclomatic complexity
                issue_type = IssueType.CYCLOMATIC_COMPLEXITY
                issue_data[IssueData.DESCRIPTION.value] = get_cyclomatic_complexity_tip()
                issue_data[IssueData.CYCLOMATIC_COMPLEXITY.value] = int(cc_match.groups()[1])
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(CyclomaticComplexityIssue(**issue_data))
            elif cohesion_match is not None:  # flake8-cohesion
                issue_type = IssueType.COHESION
                issue_data[IssueData.DESCRIPTION.value] = f'{get_cohesion_tip(f"{description.capitalize()}.")}'
                issue_data[IssueData.COHESION_LACK.value] = convert_percentage_of_value_to_lack_of_value(
                    float(cohesion_match.group(1)),
                )
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(CohesionIssue(**issue_data))
            elif line_len_match is not None:
                issue_type = IssueType.LINE_LEN
                issue_data[IssueData.DESCRIPTION.value] = get_line_len_tip()
                issue_data[IssueData.LINE_LEN.value] = int(line_len_match.groups()[0])
                issue_data[IssueData.ISSUE_TYPE.value] = IssueType.LINE_LEN
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                issues.append(LineLenIssue(**issue_data))
            else:
                issue_type = cls.choose_issue_type(origin_class)
                issue_data[IssueData.ISSUE_TYPE.value] = issue_type
                issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)
                # Magic number
                if origin_class == 'WPS432':
                    issue_data[IssueData.DESCRIPTION.value] = get_magic_number_tip(description)
                # Bad assign pattern
                elif origin_class == 'WPS350':
                    issue_data[IssueData.DESCRIPTION.value] = get_augmented_assign_pattern_tip()
                elif origin_class == 'B007':
                    issue_data[IssueData.DESCRIPTION.value] = (
                        'Loop control variable not used within the loop body. '
                        'If this is intended, replace it with an underscore.'
                    )
                else:
                    issue_data[IssueData.DESCRIPTION.value] = description
                issues.append(CodeIssue(**issue_data))

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
