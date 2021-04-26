from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser

import pandas as pd
from src.python import MAIN_FOLDER
from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


def test_correct_tool_path(run_tool_arguments=RunToolArguments):
    parser = get_parser(run_tool_arguments, n_args=5)
    parser.add_argument('-xlsx_file_path', default=XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx')
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    assert type(create_dataframe(config)) == pd.DataFrame


def test_incorrect_tool_path(run_tool_arguments=RunToolArguments):
    parser = get_parser(run_tool_arguments, n_args=4)
    parser.add_argument('-xlsx_file_path', default=XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx')
    parser.add_argument('-tp', '--tool-path', default=MAIN_FOLDER.parent / 'review/incorrect_path.py')
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    assert create_dataframe(config) == 2
