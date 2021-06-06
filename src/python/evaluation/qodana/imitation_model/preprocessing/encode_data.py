import argparse
import logging
import sys
from itertools import chain
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.qodana.imitation_model.common.util import CustomTokens, DatasetColumnArgument
from src.python.review.common.file_system import Extension


logger = logging.getLogger(__name__)
sys.path.append('')
sys.path.append('../../../../..')


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('dataset_path',
                        type=lambda value: Path(value).absolute(),
                        help='Path to the dataset with the values to be encoded. ')

    parser.add_argument('-o', '--output_file_path',
                        help='Output file path. If not set, file will be saved to '
                             'the input file parent directory.',
                        type=str,
                        default='input_file_directory')

    parser.add_argument('-c', '--add_context',
                        help='Use for the datasets with code lines only, if set to True, '
                             'n lines before and n lines after target line will be added to each sample.'
                             ' Default is False.',
                        action='store_true')

    parser.add_argument('-n', '--n_lines_to_add',
                        help='Use only if add_context is enabled. Allows to add n-lines from the same piece of code, '
                             'before and after each line in the dataset. If there are no lines before or after a line'
                             'from the same code-sample, special token will be added. Default is 2.',
                        default=2,
                        type=int)

    parser.add_argument('-ohe', '--one_hot_encoding',
                        help='If True, target column will be represented as one-hot-encoded vector. '
                             'The length of each vector is equal to the unique number of classes. '
                             'Default is True.',
                        action='store_false')


def __one_hot_encoding(df: pd.DataFrame) -> pd.DataFrame:
    """ transform: ['1, 2', '3'] array([[1, 1, 0], [0, 0, 1]])
    """
    target = df[DatasetColumnArgument.INSPECTIONS.value].to_numpy().astype(str)
    target_list_int = [np.unique(tuple(map(int, label.split(',')))) for label in target]
    try:
        mlb = MultiLabelBinarizer()
        encoded_target = mlb.fit_transform(target_list_int)
        assert len(list(set(chain.from_iterable(target_list_int)))) == encoded_target.shape[1]
        encoded_target = pd.DataFrame(data=encoded_target, columns=range(encoded_target.shape[1]))
        return encoded_target
    except AssertionError as e:
        logger.error('encoded_target.shape[1] should be equal to number of classes')
        raise e


class Context:
    """ To each line of code add context from the same solution:
        'n_lines_before' line 'n_lines_after'.
        If there are no lines before or / and after a piece of code,
        special tokens are added.
    """
    def __init__(self, df: pd.DataFrame, n_lines: int):
        self.indices = df[DatasetColumnArgument.ID.value].to_numpy()
        self.lines = df[ColumnName.CODE.value]
        self.n_lines: int = n_lines
        self.df = df

    def add_context_to_lines(self) -> pd.DataFrame:
        lines_with_context = []
        for current_line_index, current_line in enumerate(self.lines):
            context = self.add_context_before(current_line_index, current_line)
            context = self.add_context_after(context, current_line_index)
            lines_with_context.append(context[0])
        lines_with_context = pd.Series(lines_with_context)
        self.df[ColumnName.CODE.value] = lines_with_context
        return self.df

    def add_context_before(self, current_line_index: int, current_line: str) -> List:
        context = ['']
        for n_line_index in range(current_line_index - self.n_lines, self.n_lines):
            if n_line_index >= len(self.lines):
                return context
            if n_line_index == 0 or self.indices[n_line_index] != self.indices[current_line_index]:
                context = [context[0] + CustomTokens.NOC.value]
            else:
                context = [context[0] + self.lines.iloc[n_line_index]]
            if n_line_index != self.n_lines - 1:
                context = [context[0] + '\n']
        context = [context[0] + current_line]
        return context

    def add_context_after(self, context: List, current_line_index: int) -> List:
        for n_line_index in range(current_line_index + 1, self.n_lines + current_line_index + 1):
            if n_line_index >= len(self.lines) or self.indices[n_line_index] != self.indices[current_line_index]:
                context = [context[0] + CustomTokens.NOC.value]
            else:
                context = [context[0] + self.lines.iloc[n_line_index]]
            if n_line_index != self.n_lines - 1:
                context = [context[0] + '\n']
        return context


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    dataset_path = args.dataset_path
    output_file_path = args.output_file_path

    if output_file_path == 'input_file_directory':
        output_file_path = Path(dataset_path).parent / f'encoded_dataset{Extension.CSV.value}'

    # nan -> \n (empty rows)
    df = pd.read_csv(dataset_path)
    df[ColumnName.CODE.value].fillna('\n', inplace=True)

    if args.one_hot_encoding:
        target = __one_hot_encoding(df)
        df = pd.concat([df[[ColumnName.ID.value, ColumnName.CODE.value]], target], axis=1)

    if args.add_context:
        df = Context(df, args.n_lines_to_add).add_context_to_lines()

    write_dataframe_to_csv(output_file_path, df)


if __name__ == '__main__':
    main()
