import string
import subprocess
from test.python.evaluation import XLSX_DATA_FOLDER
from test.python.evaluation.conftest import EvalLocalCommandBuilder

import pytest
from src.python.evaluation import ScriptStructureRule

FILE_NAMES = [
    'test_wrong_column_name.xlsx',
    'test_java_no_version.xlsx',
    'test_empty_lang_cell.xlsx',
    'test_empty_table.xlsx',
]


def compare(string_error: str):
    return string_error.translate(string.whitespace + string.punctuation)


@pytest.mark.parametrize('file_name', FILE_NAMES)
def test_wrong_column(file_name: str, eval_command_builder: EvalLocalCommandBuilder):
    file_path = XLSX_DATA_FOLDER / file_name

    eval_command_builder.path = file_path
    process = subprocess.run(
        eval_command_builder.build(),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    assert process.returncode == 2
    assert compare(process.stderr) == compare(ScriptStructureRule) + '%'
