import argparse
import sys
import uuid
from pathlib import Path
from typing import List

import pandas as pd
from src.python.common.tool_arguments import RunToolArgument
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.pandas_util import get_solutions_df, logger
from src.python.evaluation.common.util import ColumnName
from src.python.review.common.file_system import Extension, get_parent_folder, get_restricted_extension


'''
This scripts allows unpacking solutions to the solutions dataframe.
The initial dataframe has only several obligatory columns user_id,times,codes,
where <times> is an array with times separated by ; symbol and
<codes> is an array with code fragments separated by ₣ symbol.
The <times> and <codes> arrays have to has the same length.
The resulting dataset will have several: columns user_id,time,code,
where each row contains obly one time and one code fragment
'''


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(RunToolArgument.SOLUTIONS_FILE_PATH.value.long_name,
                        type=lambda value: Path(value).absolute(),
                        help='Path to the compressed solutions')


def __parse_time_and_solutions(times_str: str, solutions_str: str) -> pd.DataFrame:
    times = times_str.split(',')[:100]
    solutions = solutions_str.split('₣')[:100]
    time_to_solution = dict(zip(times, solutions))
    user_df = pd.DataFrame(time_to_solution.items(), columns=[ColumnName.TIME.value, ColumnName.CODE.value])
    user_df[ColumnName.USER.value] = uuid.uuid4()
    return user_df


def __add_user_df(user_df_list: List[pd.DataFrame], user_df: pd.DataFrame):
    user_df_list.append(user_df)


def main() -> int:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)

    try:
        args = parser.parse_args()
        solutions_file_path = args.solutions_file_path
        extension = get_restricted_extension(solutions_file_path, [Extension.CSV])
        solutions_df = get_solutions_df(extension, solutions_file_path)
        user_df_list = []
        solutions_df.apply(lambda row: __add_user_df(user_df_list,
                                                     __parse_time_and_solutions(row['times'], row['codes'])), axis=1)
        unpacked_solutions = pd.concat(user_df_list)
        output_path = get_parent_folder(Path(solutions_file_path)) / f'unpacked_solutions{Extension.CSV.value}'
        write_dataframe_to_csv(output_path, unpacked_solutions)
        return 0

    except FileNotFoundError:
        logger.error('CSV-file with the specified name does not exists.')
        return 2

    except Exception:
        logger.exception('An unexpected error.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
