import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder


def test_inspect_file_works(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'file_or_project' / 'file.py'

    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert file_path.name in output


def test_inspect_project_works(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'file_or_project' / 'project'

    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert 'one.py' in output
    assert 'other.py' in output
