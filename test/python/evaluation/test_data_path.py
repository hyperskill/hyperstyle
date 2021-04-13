import subprocess

from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder


def test_incorrect_data_path(eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / 'do_not_exist.xlsx'

    eval_command_builder.path = file_path
    process = subprocess.run(
        eval_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    assert process.returncode == 2
    assert 'XLSX-file with the specified name does not exists.\n' == process.stderr
