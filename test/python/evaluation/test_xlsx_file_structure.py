from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser

import pytest
from src.python.common.tool_arguments import RunToolArguments
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
    parser = get_parser(RunToolArguments, n_args=5)
    parser.add_argument('-xlsx_file_path', '--xlsx_file_path', default=XLSX_DATA_FOLDER / file_name)
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    assert create_dataframe(config) == 2
