import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import (
    drop_duplicates, filter_df_by_single_value, get_issues_from_json, get_solutions_df, logger,
)
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.inspectors.common.statistics import PenaltyIssue
from src.python.evaluation.paper_evaluation.comparison_with_other_tools.tutor_statistics import sort_freq_dict
from src.python.evaluation.paper_evaluation.user_dynamics.user_statistics import UserStatistics
from src.python.review.common.file_system import Extension, get_parent_folder, get_restricted_extension
from src.python.review.inspectors.issue import IssueType


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help=RunToolArgument.SOLUTIONS_FILE_PATH.value)

    parser.add_argument('-fb', '--freq-boundary',
                        help='The boundary of solutions count for one student to analyze',
                        type=int,
                        default=100)

    parser.add_argument('-n', '--n',
                        help='Top n popular issues in solutions',
                        type=int,
                        default=10)


def __get_top_freq_issues(issues: List[List[PenaltyIssue]], n: int) -> Dict[str, int]:
    all_issues = list(map(lambda i: i.origin_class, [item for sublist in issues for item in sublist]))
    return dict(Counter(all_issues).most_common(n))


# Get statistics only for users that have >= freq_boundary solutions in solutions_df
# Statistics for each student has:
#  - <traceback> - list of list of issues, but without INFO issues
#  - <top_issues> - for each key of issue from <traceback> has frequency.
#    Contains only top_n issues
def __get_user_statistics(solutions_df: pd.DataFrame, freq_boundary: int = 100,
                          top_n: int = 10) -> List[UserStatistics]:
    stat = []
    counts = solutions_df[ColumnName.USER.value].value_counts()
    solutions_df = solutions_df[solutions_df[ColumnName.USER.value].isin(counts[counts > freq_boundary].index)]
    for user in solutions_df[ColumnName.USER.value].unique():
        user_df = filter_df_by_single_value(solutions_df,
                                            ColumnName.USER.value, user).sort_values(ColumnName.TIME.value)
        user_df = drop_duplicates(user_df)
        traceback = list(map(lambda t: get_issues_from_json(t),
                             list(user_df[ColumnName.TRACEBACK.value])))
        # Filter info category
        traceback = list(filter(lambda issues_list: filter(lambda i: i.type != IssueType.INFO, issues_list), traceback))
        top_issues = __get_top_freq_issues(traceback, top_n)
        stat.append(UserStatistics(traceback, top_issues))
    return stat


def __get_student_dynamics(stats: List[UserStatistics]) -> pd.DataFrame:
    dynamics = map(lambda s: s.get_traceback_dynamics(), stats)
    dynamics_dict = {i: ','.join(map(lambda d: str(d), dyn)) for (i, dyn) in enumerate(dynamics)}
    return pd.DataFrame(dynamics_dict.items(), columns=[ColumnName.USER.value, ColumnName.TRACEBACK.value])


def __get_total_top(stats: List[UserStatistics]) -> Dict[str, int]:
    total_top_n = {}
    for d in map(lambda s: s.top_issues, stats):
        for k, v in d.items():
            total_top_n.setdefault(k, 0)
            total_top_n[k] += v
    return sort_freq_dict(total_top_n)


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        solutions_file_path = args.solutions_file_path
        extension = get_restricted_extension(solutions_file_path, [Extension.CSV])
        solutions_df = get_solutions_df(extension, solutions_file_path)
        solutions_df = filter_df_by_single_value(solutions_df, ColumnName.IS_PUBLIC.value, 'YES')
        stats = __get_user_statistics(solutions_df, freq_boundary=args.freq_boundary, top_n=args.n)
        dynamics = __get_student_dynamics(stats)
        output_path = get_parent_folder(Path(solutions_file_path)) / f'student_issues_dynamics{Extension.CSV.value}'
        write_dataframe_to_csv(output_path, dynamics)
        print(f'The students dynamics was saved here: {output_path}')
        total_top = __get_total_top(stats)
        print('Total top issues:')
        for i, (key, freq) in enumerate(total_top.items()):
            print(f'{i}. {key} was found {freq} times')
        return 0

    except FileNotFoundError:
        logger.error('CSV-file with the specified name does not exists.')
        return 2

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
