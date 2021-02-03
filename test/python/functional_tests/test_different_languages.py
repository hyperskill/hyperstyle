import subprocess

from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder


def test_python(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'different_languages' / 'python'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert 'a.py' in output
    assert 'b.py' in output


def test_java(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'different_languages' / 'java'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert 'First.java' in output
    assert 'Second.java' in output


def test_kotlin(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'different_languages' / 'kotlin'

    local_command.path = file_path
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert 'main.kt' in output
    assert 'person.kt' in output


def test_all_java_inspectors(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'different_languages' / 'java'

    local_command.path = file_path
    local_command.disable = []
    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.stdout.decode()

    assert process.returncode == 1
    assert 'First.java' in output
    assert 'Second.java' in output
