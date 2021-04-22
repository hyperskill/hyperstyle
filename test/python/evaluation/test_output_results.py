import logging.config
from test.python.evaluation import TARGET_XLSX_DATA_FOLDER, XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser
from typing import Union

import pandas as pd
import pytest
from openpyxl import Workbook
from src.python import MAIN_FOLDER
from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.common.xlsx_util import remove_sheet, write_dataframe_to_xlsx_sheet
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe

FILE_NAMES = [
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', False, 'test1.xlsx'),
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', 'True', 'test2.xlsx'),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', False, 'test3.xlsx'),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', 'True', 'test4.xlsx'),
]

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(('test_file', 'target_file', 'output_type', 'output_file_name'), FILE_NAMES)
def test_correct_output(test_file: str, target_file: str, output_type: Union[bool, str],
                        output_file_name: str):

    parser = get_parser(RunToolArguments)
    parser.add_argument('-xlsx_file_path', '--xlsx_file_path', default=XLSX_DATA_FOLDER / test_file)
    parser.add_argument('-tool_path', '--tool_path', default=MAIN_FOLDER.parent / 'review/run_tool.py')
    parser.add_argument('--traceback', '--traceback', default=output_type)
    parser.add_argument('--output_file_name', '--output_file_name', default=output_file_name)
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    test_dataframe = create_dataframe(config)
    workbook = Workbook()
    workbook_path = config.get_file_path()
    workbook.save(workbook_path)
    write_dataframe_to_xlsx_sheet(workbook_path, test_dataframe, 'inspection_results', 'openpyxl')
    remove_sheet(workbook_path, 'Sheet')
    sheet_name = 'grades'
    if output_type:
        sheet_name = 'traceback'
    target_dataframe = pd.read_excel(TARGET_XLSX_DATA_FOLDER / target_file, sheet_name=sheet_name)

    assert test_dataframe.reset_index(drop=True).equals(target_dataframe.reset_index(drop=True))
