import subprocess

from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder, BrokenLocalCommandBuilder
from test.python.evaluation.support_scripts.clear_up import remove_sheet_with_results


def test_correct_tool_path(eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'

    eval_command_builder.path = file_path
    process = subprocess.run(
        eval_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    remove_sheet_with_results(file_path)
    assert process.returncode == 0


def test_incorrect_tool_path(broken_command_builder: BrokenLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'test_unsorted_order.xlsx'

    broken_command_builder.path = file_path
    process = subprocess.run(
        broken_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    assert process.returncode == 2
