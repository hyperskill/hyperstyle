import re
from math import floor
from pathlib import Path
from typing import List

from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueData, IssueType, MaintainabilityLackIssue


class RadonInspector(BaseInspector):
    inspector_type = InspectorType.RADON

    @classmethod
    def inspect(cls, path: Path, config: dict) -> List[BaseIssue]:
        mi_command = [
            "radon", "mi",
            "--max", "F",
            "--show",
            path,
        ]

        hal_command = [
            "radon", "hal",
            path,
        ]

        mi_output = run_in_subprocess(mi_command)
        mi_issues = cls.mi_parse(mi_output)

        hal_output = run_in_subprocess(hal_command)
        hal_issues = cls.hal_parse(hal_output)

        return mi_issues + hal_issues

    @classmethod
    def mi_parse(cls, mi_output: str) -> List[BaseIssue]:
        """
        Parses the results of the "mi" command.

        :param mi_output: "mi" command output.
        :return: list of issues.
        """
        row_re = re.compile(r"^(.*) - \w \((.*)\)$", re.M)

        issues: List[BaseIssue] = []
        for groups in row_re.findall(mi_output):
            file_path = Path(groups[0])
            maintainability_lack = cls.__get_maintainability_lack(float(groups[1]))

            issue_data = IssueData.get_base_issue_data_dict(file_path, cls.inspector_type)
            issue_data[IssueData.DESCRIPTION.value] = ""  # TODO: add tip
            issue_data[IssueData.MAINTAINABILITY_LACK.value] = maintainability_lack
            issue_data[IssueData.ISSUE_TYPE.value] = IssueType.MAINTAINABILITY

            issues.append(MaintainabilityLackIssue(**issue_data))

        return issues

    @staticmethod
    def __get_maintainability_lack(maintainability_index: float) -> int:
        """
        Converts maintainability index to lack of maintainability.
        Calculated by the formula: floor(100 - maintainability_index).

        :param maintainability_index: value in the range from 0 to 100.
        :return: lack of maintainability.
        """
        return floor(100 - maintainability_index)

    # TODO: add Halstead complexity
    @classmethod
    def hal_parse(cls, hal_output: str) -> List[BaseIssue]:
        return []
