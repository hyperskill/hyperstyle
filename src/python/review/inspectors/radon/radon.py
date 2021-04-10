import re
from pathlib import Path
from typing import List

from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueData, IssueType, MaintainabilityLackIssue
from src.python.review.inspectors.common import convert_percentage_of_value_to_lack_of_value


class RadonInspector(BaseInspector):
    inspector_type = InspectorType.RADON

    @classmethod
    def inspect(cls, path: Path, config: dict) -> List[BaseIssue]:
        mi_command = [
            "radon", "mi",  # compute the Maintainability Index score
            "--max", "F",  # set the maximum MI rank to display
            "--show",  # actual MI value is shown in results, alongside the rank
            path,
        ]

        mi_output = run_in_subprocess(mi_command)
        return cls.mi_parse(mi_output)

    @classmethod
    def mi_parse(cls, mi_output: str) -> List[BaseIssue]:
        """
        Parses the results of the "mi" command.
        Description: https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command

        :param mi_output: "mi" command output.
        :return: list of issues.
        """
        row_re = re.compile(r"^(.*) - \w \((.*)\)$", re.M)

        issues: List[BaseIssue] = []
        for groups in row_re.findall(mi_output):
            file_path = Path(groups[0])
            maintainability_lack = convert_percentage_of_value_to_lack_of_value(float(groups[1]))

            issue_data = IssueData.get_base_issue_data_dict(file_path, cls.inspector_type)
            issue_data[IssueData.DESCRIPTION.value] = ""  # TODO: add tip
            issue_data[IssueData.MAINTAINABILITY_LACK.value] = maintainability_lack
            issue_data[IssueData.ISSUE_TYPE.value] = IssueType.MAINTAINABILITY

            issues.append(MaintainabilityLackIssue(**issue_data))

        return issues
