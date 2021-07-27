import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.inspectors.common.statistics import (
    GeneralInspectorsStatistics, IssuesStatistics, PenaltyInfluenceStatistics, PenaltyIssue,
)
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
    return len(diffs_dict.get(ColumnName.GRADE.value, [])) > 0


def has_decreased_grades(diffs_dict: dict) -> bool:
    return len(diffs_dict.get(ColumnName.DECREASED_GRADE.value, [])) > 0


def __gather_issues_stat(issues_stat_dict: Dict[int, List[PenaltyIssue]]) -> IssuesStatistics:
    fragments_in_stat = len(issues_stat_dict)
    issues_dict: Dict[ShortIssue, int] = defaultdict(int)
    for _, issues in issues_stat_dict.items():
        for issue in issues:
            short_issue = ShortIssue(origin_class=issue.origin_class, type=issue.type)
            issues_dict[short_issue] += 1
    return IssuesStatistics(issues_dict, fragments_in_stat)


def gather_statistics(diffs_dict: dict) -> GeneralInspectorsStatistics:
    new_issues_stat = __gather_issues_stat(diffs_dict.get(ColumnName.TRACEBACK.value, {}))
    penalty_issues_stat = __gather_issues_stat(diffs_dict.get(ColumnName.PENALTY.value, {}))
    return GeneralInspectorsStatistics(new_issues_stat, penalty_issues_stat,
                                       PenaltyInfluenceStatistics(diffs_dict.get(ColumnName.PENALTY.value, {})))


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

    if not has_decreased_grades(diffs):
        print('All grades are equal.')
    else:
        print(f'Decreased grades was found in {len(diffs[ColumnName.DECREASED_GRADE.value])} fragments')
    print(f'{diffs.get(ColumnName.USER.value, 0)} unique users was found!')
    print(separator)

    statistics = gather_statistics(diffs)
    n = args.top_n
    print('NEW INSPECTIONS STATISTICS:')
    statistics.new_issues_stat.print_full_statistics(n, args.full_stat, separator)
    print(separator)

    print('PENALTY INSPECTIONS STATISTICS;')
    statistics.penalty_issues_stat.print_full_statistics(n, args.full_stat, separator)
    print(separator)

    print('INFLUENCE ON PENALTY STATISTICS;')
    statistics.penalty_influence_stat.print_stat()
    print(separator)


if __name__ == '__main__':
    main()
