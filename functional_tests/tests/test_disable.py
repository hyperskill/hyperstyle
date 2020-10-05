import subprocess

from functional_tests.tests.conftest import DATA_PATH, LocalCommandBuilder


def test_disable_works(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'disable' / 'contains_flake8_issues.py'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert 'FLAKE8' in output

    local_command.disable.append('flake8')
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert 'FLAKE8' not in output
