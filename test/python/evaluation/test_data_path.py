from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser

from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


def test_incorrect_data_path():
    parser = get_parser(RunToolArguments, n_args=5)
    parser.add_argument('-xlsx_file_path', default=XLSX_DATA_FOLDER / 'do_not_exist.xlsx')
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    assert create_dataframe(config) == 2
