import pandas as pd
import pytest
import subprocess

from test.python.evaluation import TARGET_XLSX_DATA_FOLDER, XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder
from test.python.evaluation.support_scripts.clear_up import remove_sheet_with_results

FILE_NAMES = [
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', 'grades'),
    ('test_sorted_order.xlsx', 'target_sorted_order.xlsx', 'traceback'),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', 'grades'),
    ('test_unsorted_order.xlsx', 'target_unsorted_order.xlsx', 'traceback'),
]


@pytest.mark.parametrize(('test_file', 'target_file', 'output_type'), FILE_NAMES)
def test_correct_output(test_file: str, target_file: str, output_type: str,
                        eval_command_builder: EvalLocalCommandBuilder):
    eval_command_builder.path = XLSX_DATA_FOLDER / test_file

    if output_type == 'traceback':
        eval_command_builder.traceback = str(True)

    subprocess.run(eval_command_builder.build())

    test_dataframe = pd.read_excel(XLSX_DATA_FOLDER / test_file, sheet_name='inspection_results')
    target_dataframe = pd.read_excel(TARGET_XLSX_DATA_FOLDER / target_file, sheet_name=output_type)

    remove_sheet_with_results(XLSX_DATA_FOLDER / test_file)

    assert test_dataframe.equals(target_dataframe)
