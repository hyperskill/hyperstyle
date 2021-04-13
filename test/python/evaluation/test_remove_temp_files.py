import subprocess

from src.python import MAIN_FOLDER

from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder
from test.python.evaluation.support_scripts.clear_up import remove_sheet_with_results

from src.python.review.common.file_system import get_all_file_system_items


def test_temp_files_remove(eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'
    eval_command_builder.path = file_path
    subprocess.run(eval_command_builder.build())
    remove_sheet_with_results(file_path)
    temporary_files = get_all_file_system_items(MAIN_FOLDER.parent / 'evaluation/temporary_files')
    assert temporary_files == []
