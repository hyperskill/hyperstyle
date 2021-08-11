from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List

from src.python.evaluation.inspectors.common.statistics import PenaltyIssue


@unique
class DynamicsColumn(Enum):
    ALL_ISSUES_COUNT = 'all_issues_count'
    FORMATTING_ISSUES_COUNT = 'formatting_issues_count'
    OTHER_ISSUES_COUNT = 'other_issues_count'

    ISSUE_COUNT = 'issue_count'


@dataclass
class UserStatistics:
    traceback: List[List[PenaltyIssue]]
    top_issues: Dict[str, int]

    def get_traceback_dynamics(self) -> List[int]:
        return list(map(lambda i_l: len(i_l), self.traceback))
