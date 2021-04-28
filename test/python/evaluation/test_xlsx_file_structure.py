from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_testing_arguments

import pytest
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


FILE_NAMES = [
    'test_wrong_column_name.xlsx',
    'test_java_no_version.xlsx',
    'test_empty_lang_cell.xlsx',
    'test_empty_table.xlsx',
]


@pytest.mark.parametrize('file_name', FILE_NAMES)
def test_wrong_column(file_name: str):
    with pytest.raises(KeyError):
        testing_arguments_dict = get_testing_arguments(n_args=5)
        testing_arguments_dict['xlsx_file_path'] = XLSX_DATA_FOLDER / file_name
        config = EvaluationConfig(testing_arguments_dict)
        assert create_dataframe(config)
