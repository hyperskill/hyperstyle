import argparse
import os
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.model.common.util import MarkingArgument
from src.python.review.common.file_system import create_directory, Extension


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path',
                        type=str,
                        help=f'Path to the dataset received by either'
                             f' src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             f'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('-d', '--directory_path',
                        type=str,
                        default=None,
                        help=f'Path to the directory where folders for train, test and validation datasets'
                             f'will be created'
                             f'src.python.evaluation.qodana.fragment_to_inspections_list{Extension.PY.value}'
                             f'or src.python.evaluation.qodana.fragment_to_inspections_list_line_by_line'
                             f'{Extension.PY.value}script.')

    parser.add_argument('-ts', '--test_size',
                        type=int,
                        default=0.2,
                        help='Rate of test size from the whole dataset. Default is 0.2')

    parser.add_argument('-vs', '--val_size',
                        type=int,
                        default=0.3,
                        help='Rate of validation dataset from the train dataset. Default is 0.3 ')

    parser.add_argument('-sh', '--shuffle',
                        type=bool,
                        default=True,
                        help='If true, data will be shuffled before splitting. Default is True.')

    return parser


def split_dataset(dataset_path: str, output_folder: str, val_size: float, test_size: float, shuffle: bool):
    df = pd.read_csv(dataset_path)
    target = df.iloc[:, 3:]
    code_bank = df[ColumnName.CODE.value]

    code_train, code_test, target_train, target_test = train_test_split(code_bank,
                                                                        target,
                                                                        test_size=test_size,
                                                                        random_state=MarkingArgument.SEED.value,
                                                                        shuffle=shuffle)

    code_train, code_val, target_train, target_val = train_test_split(code_train,
                                                                      target_train,
                                                                      test_size=val_size,
                                                                      random_state=MarkingArgument.SEED.value,
                                                                      shuffle=shuffle)
    if output_folder is None:
        output_folder = Path(dataset_path).parent

    for holdout in [("train", code_train, target_train),
                    ("val", code_val, target_val),
                    ("test", code_test, target_test)]:
        df = pd.concat([holdout[1], holdout[2]], axis=1)
        create_directory(os.path.join(output_folder, holdout[0]))
        write_dataframe_to_csv(Path(output_folder) / holdout[0] / f'{holdout[0]}{Extension.CSV.value}', df)


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()

    split_dataset(args.dataset_path, args.directory_path, args.val_size, args.test_size, args.shuffle)
