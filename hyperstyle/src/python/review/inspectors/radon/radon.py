import re
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    IssueData,
    IssueDifficulty,
    IssueType,
    MaintainabilityLackIssue,
)
from hyperstyle.src.python.review.inspectors.tips import get_maintainability_index_tip


MAINTAINABILITY_ORIGIN_CLASS = 'RAD100'


class RadonInspector(BaseInspector):
    inspector_type = InspectorType.RADON

    @classmethod
    def inspect(cls, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        mi_command = [
            'radon', 'mi',  # compute the Maintainability Index score
            '--max', 'F',  # set the maximum MI rank to display
            '--show',  # actual MI value is shown in results, alongside the rank
            path,
        ]

        mi_output = run_in_subprocess(mi_command)
        return cls.mi_parse(mi_output)

    @classmethod
    def mi_parse(cls, mi_output: str) -> List[BaseIssue]:
        """
        Parses the results of the 'mi' command.
        Description: https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command

        :param mi_output: 'mi' command output.
        :return: list of issues.
        """
        row_re = re.compile(r'^(.*) - \w \((.*)\)$', re.M)

        issues: List[BaseIssue] = []
        for groups in row_re.findall(mi_output):
            file_path = Path(groups[0])
            maintainability_lack = convert_percentage_of_value_to_lack_of_value(float(groups[1]))

            issue_type = cls.choose_issue_type(MAINTAINABILITY_ORIGIN_CLASS)

            issue_data = IssueData.get_base_issue_data_dict(
                file_path, cls.inspector_type, origin_class=MAINTAINABILITY_ORIGIN_CLASS,
            )
            issue_data[IssueData.DESCRIPTION.value] = get_maintainability_index_tip()
            issue_data[IssueData.MAINTAINABILITY_LACK.value] = maintainability_lack
            issue_data[IssueData.ISSUE_TYPE.value] = issue_type
            issue_data[IssueData.DIFFICULTY.value] = IssueDifficulty.get_by_issue_type(issue_type)

            issues.append(MaintainabilityLackIssue(**issue_data))

        return issues

    @staticmethod
    def choose_issue_type(code: str) -> IssueType:
        if code == MAINTAINABILITY_ORIGIN_CLASS:
            return IssueType.MAINTAINABILITY

        return IssueType.BEST_PRACTICES
