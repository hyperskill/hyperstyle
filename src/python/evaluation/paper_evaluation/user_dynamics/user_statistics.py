from dataclasses import dataclass
from typing import List, Dict

from src.python.evaluation.inspectors.common.statistics import PenaltyIssue


@dataclass
class UserStatistics:
    traceback: List[List[PenaltyIssue]]
    top_issues: Dict[str, int]

    def get_traceback_dynamics(self) -> List[int]:
        return list(map(lambda i_l: len(i_l), self.traceback))