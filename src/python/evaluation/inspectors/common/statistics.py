from collections import defaultdict
from dataclasses import dataclass
from statistics import median
from typing import Dict, List, Tuple

from src.python.review.inspectors.issue import BaseIssue, IssueType, ShortIssue


@dataclass(frozen=True, eq=True)
class PenaltyIssue(BaseIssue):
    influence_on_penalty: int


@dataclass(frozen=True)
class IssuesStatistics:
    stat: Dict[ShortIssue, int]
    fragments_in_stat: int

    def print_full_statistics(self, n: int, full_stat: bool, separator: str = '') -> None:
        if self.fragments_in_stat == 0:
            print('Statistics is empty!')
            return

        print(f'{self.fragments_in_stat} fragments has additional issues')
        print(f'{self.count_unique_issues()} unique issues was found')

        self.print_top_n(n, separator)
        self.print_short_categorized_statistics()
        print(separator)

        if full_stat:
            self.print_full_inspectors_statistics()

    def print_top_n(self, n: int, separator: str) -> None:
        top_n = self.get_top_n_issues(n)
        print(separator)
        print(f'Top {n} issues:')
        for issue, freq in top_n:
            IssuesStatistics.print_issue_with_freq(issue, freq)
        print(separator)

    def print_full_inspectors_statistics(self, to_categorize: bool = True) -> None:
        if to_categorize:
            categorized_statistics: Dict[IssueType, Dict[ShortIssue, int]] = self.get_categorized_statistics()
            for category, issues in categorized_statistics.items():
                print(f'{category.value} issues:')
                self.__print_stat(issues)
        else:
            self.__print_stat(self.stat)

    @classmethod
    def __print_stat(cls, stat: Dict[ShortIssue, int]) -> None:
        for issue, freq in stat.items():
            cls.print_issue_with_freq(issue, freq, prefix='- ')

    @classmethod
    def print_issue_with_freq(cls, issue: ShortIssue, freq: int, prefix: str = '', suffix: str = '') -> None:
        print(f'{prefix}{issue.origin_class}: {freq} times{suffix}')

    def get_categorized_statistics(self) -> Dict[IssueType, Dict[ShortIssue, int]]:
        categorized_stat: Dict[IssueType, Dict[ShortIssue, int]] = defaultdict(dict)
        for issue, freq in self.stat.items():
            categorized_stat[issue.type][issue] = freq
        return categorized_stat

    # Get statistics for each IssueType: count unique issues, count fragments with these issues
    def get_short_categorized_statistics(self) -> Dict[IssueType, Tuple[int, int]]:
        categorized_statistics: Dict[IssueType, Dict[ShortIssue, int]] = self.get_categorized_statistics()
        short_categorized_statistics = defaultdict(tuple)
        for issue_type, stat in categorized_statistics.items():
            unique_issues = len(stat)
            fragments = sum(stat.values())
            short_categorized_statistics[issue_type] = (unique_issues, fragments)
        return short_categorized_statistics

    def print_short_categorized_statistics(self) -> None:
        short_categorized_statistics = self.get_short_categorized_statistics()
        for category, stat in short_categorized_statistics.items():
            print(f'{category.value}: {stat[0]} issues, {stat[1]} fragments')

    def get_top_n_issues(self, n: int) -> List[ShortIssue]:
        return sorted(self.stat.items(), key=lambda t: t[1], reverse=True)[:n]

    def count_unique_issues(self) -> int:
        return len(self.stat)


# Store list of penalty influences for each category
@dataclass
class PenaltyInfluenceStatistics:
    stat: Dict[IssueType, List[float]]

    def __init__(self, issues_stat_dict: Dict[int, List[PenaltyIssue]]):
        self.stat = defaultdict(list)
        for _, issues in issues_stat_dict.items():
            for issue in issues:
                self.stat[issue.type].append(issue.influence_on_penalty)

    def print_stat(self):
        for category, issues in self.stat.items():
            print(f'{category.value} issues: min={min(issues)}, max={max(issues)}, median={median(issues)}')


@dataclass(frozen=True)
class GeneralInspectorsStatistics:
    new_issues_stat: IssuesStatistics
    penalty_issues_stat: IssuesStatistics
    penalty_influence_stat: PenaltyInfluenceStatistics
