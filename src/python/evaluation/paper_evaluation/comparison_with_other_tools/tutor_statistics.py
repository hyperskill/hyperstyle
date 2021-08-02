from collections import Counter
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List

import pandas as pd
from src.python.evaluation.common.pandas_util import filter_df_by_single_value
from src.python.evaluation.paper_evaluation.comparison_with_other_tools.util import (
    ComparisonColumnName, ERROR_CONST, TutorTask,
)


def sort_freq_dict(freq_dict: Dict[Any, int]) -> Dict[Any, int]:
    return dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))


@dataclass
class TutorStatistics:
    unique_users: int
    task_to_freq: Dict[TutorTask, int]
    task_to_error_freq: Dict[TutorTask, int]
    error_to_freq: Dict[str, int]
    fragments_with_error: int = 0

    __separator: str = '----------'

    def __init__(self, solutions_df: pd.DataFrame, to_drop_duplicates: bool = False):
        if to_drop_duplicates:
            solutions_df = solutions_df.drop_duplicates(ComparisonColumnName.SOLUTION.value)
        self.unique_users = len(solutions_df[ComparisonColumnName.STUDENT_ID.value].unique())
        self.task_to_freq = defaultdict(int)
        self.task_to_error_freq = defaultdict(int)
        self.error_to_freq = defaultdict(int)
        for task in TutorTask:
            task_df = filter_df_by_single_value(solutions_df, ComparisonColumnName.TASK_KEY.value, task.value)
            self.task_to_freq[task] = task_df.shape[0]
            errors_list = list(map(lambda e_l: e_l.split(';'),
                                   task_df[ComparisonColumnName.TUTOR_ERROR.value].dropna().values))
            for cell_errors in errors_list:
                for error in cell_errors:
                    self.error_to_freq[error.strip()] += 1
                self.task_to_error_freq[task] += 1
                self.fragments_with_error += 1
        self.task_to_freq = sort_freq_dict(self.task_to_freq)
        self.error_to_freq = sort_freq_dict(self.error_to_freq)

    def print_tasks_stat(self) -> None:
        print(f'Unique users count: {self.unique_users}')
        print(f'Code snippets count: {sum(self.task_to_freq.values())}')
        print('Tasks statistics:')
        for task, freq in self.task_to_freq.items():
            print(f'Task {task.value}: {freq} items; {self.task_to_error_freq[task]} with tutor errors')
        print(self.__separator)

    def print_error_stat(self) -> None:
        print(f'{self.fragments_with_error} code fragments has errors during running by Tutor')
        print(f'{len(self.error_to_freq.keys())} unique errors was found in Tutor')
        print('Error statistics:')
        for error, freq in self.error_to_freq.items():
            print(f'{error}: {freq} items')
        print(self.__separator)


@dataclass
class IssuesStatistics:
    common_issue_to_freq: Dict[str, int]
    tutor_uniq_issue_to_freq: Dict[str, int]
    hyperstyle_uniq_issue_to_freq: Dict[str, int]

    code_style_issues_count: int
    fragments_count_with_code_style_issues: int

    __separator: str = '----------'

    # TODO: info and code style issues
    def __init__(self, solutions_df: pd.DataFrame, to_drop_duplicates: bool = False):
        if to_drop_duplicates:
            solutions_df = solutions_df.drop_duplicates(ComparisonColumnName.SOLUTION.value)
        self.common_issue_to_freq = defaultdict(int)
        self.tutor_uniq_issue_to_freq = defaultdict(int)
        self.hyperstyle_uniq_issue_to_freq = defaultdict(int)
        solutions_df.apply(lambda row: self.__init_solution_df_row(row), axis=1)
        self.common_issue_to_freq = sort_freq_dict(self.common_issue_to_freq)
        self.tutor_uniq_issue_to_freq = sort_freq_dict(self.tutor_uniq_issue_to_freq)
        self.hyperstyle_uniq_issue_to_freq = sort_freq_dict(self.hyperstyle_uniq_issue_to_freq)
        self.code_style_issues_count = sum(solutions_df[ComparisonColumnName.CODE_STYLE_ISSUES_COUNT.value])
        self.fragments_count_with_code_style_issues = len(list(
            filter(lambda x: x != 0, solutions_df[ComparisonColumnName.CODE_STYLE_ISSUES_COUNT.value])))

    @staticmethod
    def __parse_issues(issues_str: str) -> List[str]:
        if pd.isna(issues_str) or issues_str == ERROR_CONST:
            return []
        return list(map(lambda i: i.strip(), issues_str.split(';')))

    @staticmethod
    def __add_issues(issues_dict: Dict[str, int], issues: List[str]) -> None:
        for issue in issues:
            issues_dict[issue] += 1

    def __init_solution_df_row(self, row: pd.DataFrame) -> None:
        tutor_issues = self.__parse_issues(row[ComparisonColumnName.TUTOR_ISSUES.value])
        hyperstyle_issues = self.__parse_issues(row[ComparisonColumnName.HYPERSTYLE_ISSUES.value])
        common_issues = list((Counter(tutor_issues) & Counter(hyperstyle_issues)).elements())
        self.__add_issues(self.common_issue_to_freq, common_issues)
        self.__add_issues(self.tutor_uniq_issue_to_freq, list(set(tutor_issues) - set(common_issues)))
        self.__add_issues(self.hyperstyle_uniq_issue_to_freq, list(set(hyperstyle_issues) - set(common_issues)))

    def __print_freq_issues_stat(self, freq_stat: Dict[str, int], prefix: str) -> None:
        print(f'{prefix} issues statistics:')
        for issue, freq in freq_stat.items():
            print(f'{issue} was found {freq} times')
        print(self.__separator)

    def print_issues_stat(self) -> None:
        uniq_issues = (len(self.common_issue_to_freq)
                       + len(self.tutor_uniq_issue_to_freq)
                       + len(self.hyperstyle_uniq_issue_to_freq)
                       )
        print(f'{uniq_issues} unique issues in total was found')
        print(self.__separator)
        self.__print_freq_issues_stat(self.common_issue_to_freq, 'Common')
        self.__print_freq_issues_stat(self.tutor_uniq_issue_to_freq, 'Tutor unique')
        self.__print_freq_issues_stat(self.hyperstyle_uniq_issue_to_freq, 'Hyperstyle unique')
        print(f'{self.code_style_issues_count} code style issues (spaces, different brackets, indentations)'
              f' was found in total by hyperstyle in {self.fragments_count_with_code_style_issues}  fragments')
        print(self.__separator)
