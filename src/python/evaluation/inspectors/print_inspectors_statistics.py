import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.evaluation.inspectors.common.statistics import IssuesStatistics
from src.python.review.common.file_system import deserialize_data_from_file
from src.python.review.inspectors.issue import ShortIssue


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.DIFFS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.DIFFS_FILE_PATH.value.description)

    parser.add_argument('--categorize',
                        help='If True, statistics will be categorized by several categories.',
                        action='store_true')

    parser.add_argument('-n', '--top-n',
                        help='The top N items will be printed',
                        type=int,
                        default=10)

    parser.add_argument('--full-stat',
                        help='If True, full statistics will be printed.',
                        action='store_true')


def has_incorrect_grades(diffs_dict: dict) -> bool:
    return len(diffs_dict[ColumnName.GRADE.value]) > 0


def gather_statistics(diffs_dict: dict) -> IssuesStatistics:
    changed_grades_count = len(diffs_dict[EvaluationArgument.TRACEBACK.value])
    issues_dict: Dict[ShortIssue, int] = defaultdict(int)
    for _, issues in diffs_dict[EvaluationArgument.TRACEBACK.value].items():
        for issue in issues:
            short_issue = ShortIssue(origin_class=issue.origin_class, type=issue.type)
            issues_dict[short_issue] += 1
    return IssuesStatistics(issues_dict, changed_grades_count)


def __print_top_n(statistics: IssuesStatistics, n: int, separator: str) -> None:
    top_n = statistics.get_top_n_issues(n)
    print(separator)
    print(f'Top {n} issues:')
    for issue, freq in top_n:
        IssuesStatistics.print_issue_with_freq(issue, freq)
    print(separator)


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    separator = '______'

    diffs = deserialize_data_from_file(args.diffs_file_path)
    if has_incorrect_grades(diffs):
        print(f'WARNING! Was found incorrect grades in the following fragments: {diffs[ColumnName.GRADE.value]}.')
    else:
        print('SUCCESS! Was not found incorrect grades.')
    print(separator)

    statistics = gather_statistics(diffs)
    print(f'{statistics.changed_grades_count} fragments has additional issues')
    print(f'{statistics.count_unique_issues()} unique issues was found')

    n = args.top_n
    __print_top_n(statistics, n, separator)

    statistics.print_short_categorized_statistics()
    print(separator)

    if args.full_stat:
        statistics.print_full_statistics()


if __name__ == '__main__':
    main()
