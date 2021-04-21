import subprocess
from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser
from test.python.evaluation.conftest import BrokenLocalCommandBuilder

from src.python import MAIN_FOLDER
from src.python.common.tool_arguments import RunToolArguments
from src.python.evaluation.evaluation_config import EvaluationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe


def test_correct_tool_path():
    parser = get_parser(RunToolArguments)
    parser.add_argument('-xlsx_file_path', default=XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx')
    parser.add_argument('-tool_path', '--tool_path', default=MAIN_FOLDER.parent / 'review/run_tool.py')
    parser.add_argument('--traceback', '--traceback', default=False)
    args = parser.parse_args([])
    config = EvaluationConfig(args)
    create_dataframe(config)


def test_incorrect_tool_path(broken_command_builder: BrokenLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'

    broken_command_builder.path = file_path
    process = subprocess.run(
        broken_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    assert process.returncode == 1
