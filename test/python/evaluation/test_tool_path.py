import os
import subprocess
import time
from test.python.evaluation import RESULTS_DIR_PATH, XLSX_DATA_FOLDER
from test.python.evaluation.conftest import BrokenLocalCommandBuilder, EvalLocalCommandBuilder


def test_correct_tool_path(eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'

    eval_command_builder.path = file_path
    process = subprocess.run(
        eval_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    assert process.returncode == 0
    # wait before deleting file and directory as they appear with a delay
    time.sleep(180)
    os.remove(RESULTS_DIR_PATH / 'results.xlsx')
    os.rmdir(RESULTS_DIR_PATH)


def test_incorrect_tool_path(broken_command_builder: BrokenLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'

    broken_command_builder.path = file_path
    process = subprocess.run(
        broken_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    assert process.returncode == 1
