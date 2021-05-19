import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict

from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.evaluation.inspectors.common.statistics import IssuesStatistics
from src.python.review.common.file_system import deserialize_data_from_file
from src.python.review.inspectors.issue import ShortIssue


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('diffs_file_path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to a file with serialized diffs that were founded by diffs_between_df.py')

    parser.add_argument('--categorize',
                        help='If True, statistics will be categorized by several categories.',
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


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    diffs = deserialize_data_from_file(args.diffs_file_path)
    if has_incorrect_grades(diffs):
        print(f'WARNING! Was found incorrect grades in the following fragments: {diffs[ColumnName.GRADE.value]}.')
    else:
        print('SUCCESS! Was not found incorrect grades.')

    statistics = gather_statistics(diffs)
    print(f'{statistics.changed_grades_count} fragments has additional issues')

    statistics.print_statistics(to_categorize=args.categorize)


if __name__ == '__main__':
    main()
