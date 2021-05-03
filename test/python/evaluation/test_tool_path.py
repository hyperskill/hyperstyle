from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_testing_arguments

import pytest
from src.python import MAIN_FOLDER
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


def test_correct_tool_path():
    try:
        testing_arguments_dict = get_testing_arguments(to_add_traceback=True, to_add_tool_path=True)
        testing_arguments_dict.xlsx_file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'
        config = EvaluationConfig(testing_arguments_dict)
        create_dataframe(config)
    except Exception:
        pytest.fail("Unexpected error")


def test_incorrect_tool_path():
    with pytest.raises(Exception):
        testing_arguments_dict = get_testing_arguments(to_add_traceback=True)
        testing_arguments_dict.xlsx_file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'
        testing_arguments_dict.tool_path = MAIN_FOLDER.parent / 'review/incorrect_path.py'
        config = EvaluationConfig(testing_arguments_dict)
        assert create_dataframe(config)
