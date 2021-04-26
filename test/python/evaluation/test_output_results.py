from test.python.evaluation import TARGET_XLSX_DATA_FOLDER, XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser
from typing import Union

import pandas as pd
import pytest
from src.python import MAIN_FOLDER
from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe

FILE_NAMES = [
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', False),
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', True),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', False),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', True),
]


@pytest.mark.parametrize(('test_file', 'target_file', 'output_type'), FILE_NAMES)
def test_correct_output(test_file: str, target_file: str, output_type: Union[bool, str]):

    parser = get_parser(RunToolArguments)
    parser.add_argument('-xlsx_file_path', default=XLSX_DATA_FOLDER / test_file)
    parser.add_argument('-tp', '--tool-path', default=MAIN_FOLDER.parent / 'review/run_tool.py')
    if output_type:
        parser.add_argument('-tr', '--traceback', action='store_false')
    else:
        parser.add_argument('-tr', '--traceback', action='store_true')

    args = parser.parse_args([])
    config = EvaluationConfig(args)
    test_dataframe = create_dataframe(config)

    sheet_name = 'grades'
    if output_type:
        sheet_name = 'traceback'
    target_dataframe = pd.read_excel(TARGET_XLSX_DATA_FOLDER / target_file, sheet_name=sheet_name)

    assert test_dataframe.reset_index(drop=True).equals(target_dataframe.reset_index(drop=True))
