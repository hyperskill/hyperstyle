from collections import defaultdict
from dataclasses import dataclass
from typing import Dict

from src.python.review.inspectors.issue import IssueType, ShortIssue


@dataclass(frozen=True)
class IssuesStatistics:
    stat: Dict[ShortIssue, int]
    changed_grades_count: int

    def print_statistics(self, to_categorize: bool = True):
        if to_categorize:
            categorized_statistics: Dict[IssueType, Dict[ShortIssue, int]] = self.__categorize_statistics()
            for category, issues in categorized_statistics.items():
                print(f'{category.value} issues:')
                self.__print_stat(issues)
        else:
            self.__print_stat(self.stat)

    @classmethod
    def __print_stat(cls, stat: Dict[ShortIssue, int]):
        for issue, freq in stat.items():
            print(f'- {issue.origin_class}": {freq} times')

    def __categorize_statistics(self) -> Dict[IssueType, Dict[ShortIssue, int]]:
        categorized_stat: Dict[IssueType, Dict[ShortIssue, int]] = defaultdict(dict)
        for issue, freq in self.stat.items():
            categorized_stat[issue.type][issue] = freq
        return categorized_stat
