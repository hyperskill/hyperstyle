import os
import subprocess
import time
from test.python.evaluation import RESULTS_DIR_PATH, XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder

from src.python import MAIN_FOLDER
from src.python.review.common.file_system import get_all_file_system_items


def test_temp_files_remove(eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'
    eval_command_builder.path = file_path
    subprocess.run(eval_command_builder.build())
    temporary_files = get_all_file_system_items(MAIN_FOLDER.parent / 'evaluation/temporary_files')
    assert temporary_files == []
    # wait before deleting file and directory as they appear with a delay
    time.sleep(180)
    os.remove(RESULTS_DIR_PATH / 'results.xlsx')
    os.rmdir(RESULTS_DIR_PATH)
