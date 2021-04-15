from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.testing_config import get_parser

from src.python import MAIN_FOLDER
from src.python.evaluation.evaluation_config import ApplicationConfig
from src.python.evaluation.xlsx_run_tool import create_dataframe
from src.python.review.common.file_system import get_all_file_system_items


def test_temp_files_remove():
    parser = get_parser()
    parser.add_argument('-data_path', '--data_path', default=XLSX_DATA_FOLDER / 'test_sorted_order.xlsx')
    parser.add_argument('-t', '--tool_path', default=MAIN_FOLDER.parent / 'review/run_tool.py')
    parser.add_argument('--traceback', '--traceback', default=False)
    args = parser.parse_args([])
    config = ApplicationConfig(args)
    create_dataframe(config)
    temporary_files = get_all_file_system_items(MAIN_FOLDER.parent / 'evaluation/temporary_files')
    assert temporary_files == []
