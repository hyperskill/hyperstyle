import re
import subprocess

from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder


def test_allow_duplicates(local_command: LocalCommandBuilder):
    file_with_duplicate_issue_path = DATA_PATH / 'duplicates' / 'code_with_duplicate_issues.py'

    local_command.allow_duplicates = True
    local_command.path = file_with_duplicate_issue_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_allow_duplicates = process.stdout.decode()

    local_command.allow_duplicates = False

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_filter_duplicates = process.stdout.decode()

    flake8_var_issue_re = re.compile(r'.*FLAKE8.*local variable \'var\'.*', re.DOTALL)
    pylint_var_issue_re = re.compile(r'.*PYLINT.*Unused variable \'var\'.*', re.DOTALL)

    assert len(stdout_filter_duplicates) < len(stdout_allow_duplicates)
    assert ((flake8_var_issue_re.match(stdout_allow_duplicates) is not None) and (
            pylint_var_issue_re.match(stdout_allow_duplicates) is not None))
    assert ((flake8_var_issue_re.match(stdout_filter_duplicates) is not None) ^ (
            pylint_var_issue_re.match(stdout_filter_duplicates) is not None))
