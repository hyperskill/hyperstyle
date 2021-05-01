from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_testing_arguments

import pytest
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


def test_incorrect_data_path():
    with pytest.raises(FileNotFoundError):
        testing_arguments_dict = get_testing_arguments(to_add_traceback=True, to_add_tool_path=True)
        testing_arguments_dict.xlsx_file_path = XLSX_DATA_FOLDER / 'do_not_exist.xlsx'
        config = EvaluationConfig(testing_arguments_dict)
        assert create_dataframe(config)
