from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_testing_arguments

import pytest
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.evaluation_run_tool import get_solutions_df, inspect_solutions_df


def test_incorrect_data_path():
    with pytest.raises(FileNotFoundError):
        testing_arguments_dict = get_testing_arguments(to_add_traceback=True, to_add_tool_path=True)
        testing_arguments_dict.solutions_file_path = XLSX_DATA_FOLDER / 'do_not_exist.xlsx'
        testing_arguments_dict.with_history = False
        config = EvaluationConfig(testing_arguments_dict)
        lang_code_dataframe = get_solutions_df(config.extension, config.solutions_file_path)
        assert inspect_solutions_df(config, lang_code_dataframe)
