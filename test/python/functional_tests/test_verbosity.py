import json
import subprocess

from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder


def test_disable_logs_text(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'verbosity' / 'some_code.py'

    local_command.verbosity = 0
    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()
    output = output.lower()

    assert 'debug' not in output
    assert 'info' not in output
    assert 'error' not in output


def test_disable_logs_json(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'verbosity' / 'some_code.py'

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = process.stdout.decode()
    json.loads(output)


def test_enable_all_logs(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'verbosity' / 'some_code.py'

    local_command.verbosity = 3
    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()
    output = output.lower()

    assert 'debug' in output
