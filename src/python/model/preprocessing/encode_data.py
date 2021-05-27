import argparse
import logging
import sys
from itertools import chain
from pathlib import Path
from typing import List

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.model.common.util import CustomTokens, MarkingArgument
from src.python.review.common.file_system import Extension


logger = logging.getLogger(__name__)
sys.path.append('')
sys.path.append('../../..')


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
                             '2 lines before and after target line will be added.'
                             'If enable context on training dataset, please, make sure you also enable '
                             'context for testing and validation. Default is False.',
                        action='store_true')

    parser.add_argument('-ohe', '--one_hot_encoding',
                        help='If True, target column will be represented as one-hot-encoded vector. '
                             'The length of each vector is equal to the unique number of classes. '
                             'Default is True.',
                        action='store_false')


def __one_hot_encoding(df: pd.DataFrame) -> pd.DataFrame:
    """ transform: ['1, 2', '3'] array([[1, 1, 0], [0, 0, 1]])
    """
    target = df[MarkingArgument.INSPECTIONS.value].to_numpy()
    tuple_target = [tuple(map(int, label.split_dataset(','))) for label in target]
    try:
        mlb = MultiLabelBinarizer()
        encoded_target = mlb.fit_transform(tuple_target)
        assert len(list(set(chain.from_iterable(tuple_target)))) == encoded_target.shape[1]
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
    def __init__(self, df: pd.DataFrame):
        self.n_lines_before: int = 2
        self.n_lines_after: int = 2
        self.indices = df[MarkingArgument.ID.value].to_numpy()
        self.lines = df[ColumnName.CODE.value]
        self.df = df

    def add_context_to_lines(self) -> pd.DataFrame:
        lines_with_context = []
        for i, line in enumerate(self.lines):
            context = self.add_line_before(i, line)
            context = self.add_line_after(context, i)
            lines_with_context.append(context[0])
        lines_with_context = pd.Series(lines_with_context)
        self.df[ColumnName.CODE.value] = lines_with_context
        return self.df

    def add_line_before(self, i: int, line: str) -> List:
        if i == 0 or self.indices[i - 1] != self.indices[i]:
            context = [f'{CustomTokens.NOC.value}\n{CustomTokens.NOC.value}\n{line}']

        elif i == 1 or self.indices[i - 2] != self.indices[i]:
            context = [f'{CustomTokens.NOC.value}\n{self.lines.iloc[i - 1]}\n{line}']

        elif self.indices[i - 1] == self.indices[i] and self.indices[i - 2] == self.indices[i]:
            context = [f'{self.lines.iloc[i - 2]}\n{self.lines.iloc[i - 1]}\n{line}']
        else:
            message = 'Unexpected error while adding lines to the context before target line.'
            logger.error(message)
            raise Exception(message)
        return context

    def add_line_after(self, context: List, i: int) -> List:
        if i == len(self.lines) - 1 or self.indices[i + 1] != self.indices[i]:
            context = [context[0] + f'\n{CustomTokens.NOC.value}\n{CustomTokens.NOC.value}']

        elif i == len(self.lines) - 2 or self.indices[i + 2] != self.indices[i]:
            context = [context[0] + f'\n{self.lines.iloc[i + 1]}\n{CustomTokens.NOC.value}']

        elif self.indices[i + 1] == self.indices[i] and self.indices[i + 2] == self.indices[i]:
            context += [context[0] + f'{self.lines.iloc[i + 1]}\n{self.lines.iloc[i + 2]}']
        else:
            message = 'Unexpected error while adding lines to the context after target line.'
            logger.error(message)
            raise Exception(message)
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
        df = df.iloc[:, 0:3]
        df = pd.concat([df, target], axis=1)

    if args.add_context:
        df = Context(df).add_context_to_lines()

    write_dataframe_to_csv(output_file_path, df)


if __name__ == '__main__':
    main()
