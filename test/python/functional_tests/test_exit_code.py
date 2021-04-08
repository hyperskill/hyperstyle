import subprocess
from pathlib import Path

from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder


def test_exit_code_zero(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'exit_codes' / 'no_issues.py'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert process.returncode == 0


def test_exit_code_one(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'exit_codes' / 'with_issues.py'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert process.returncode == 1


def test_exit_code_two(local_command: LocalCommandBuilder):
    file_path = Path('no_such_file.py')

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert process.returncode == 2
