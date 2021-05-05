import json
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder

import pytest
from src.python.review.common.subprocess_runner import run_in_subprocess

PATH_TO_FILE = DATA_PATH / 'lines_range' / 'code_with_multiple_issues.py'

EXPECTED_JSON = {
    'quality': {
        'code': 'BAD',
        'text': 'Code quality (beta): BAD',
    },
    'issues': [{
        'category': 'CODE_STYLE',
        'code': 'E225',
        'column_number': 2,
        'line': 'a=10',
        'line_number': 1,
        'text': 'missing whitespace around operator',
        'influence_on_penalty': 0},
        {'category': 'CODE_STYLE',
         'code': 'E225',
         'column_number': 2,
         'line': 'b=20',
         'line_number': 2,
         'text': 'missing whitespace around operator',
         'influence_on_penalty': 0},
        {'category': 'CODE_STYLE',
         'code': 'E225',
         'column_number': 2,
         'line': 'c=a + b',
         'line_number': 4,
         'text': 'missing whitespace around operator',
         'influence_on_penalty': 0,
         },
    ],
}

NO_ISSUES_JSON = {
    'quality': {
        'code': 'EXCELLENT',
        'text': 'Code quality (beta): EXCELLENT'},
    'issues': [],
}


def test_range_filter_when_no_range_specified(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == EXPECTED_JSON


def test_range_filter_when_start_line_is_first(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 1

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == EXPECTED_JSON


def test_range_filter_when_start_line_is_not_first(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 3

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    expected_json_with_one_issue = {
        'quality': {
            'code': 'MODERATE',
            'text': 'Code quality (beta): MODERATE'},
        'issues': [{
            'code': 'E225',
            'text': 'missing whitespace around operator',
            'line': 'c=a + b',
            'line_number': 4,
            'column_number': 2,
            'category': 'CODE_STYLE',
            'influence_on_penalty': 0,
        }],
    }

    assert output_json == expected_json_with_one_issue


def test_range_filter_when_start_out_of_range(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 5

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    expected_json_without_issues = NO_ISSUES_JSON

    assert output_json == expected_json_without_issues


def test_range_filter_when_start_line_is_not_positive(
        local_command: LocalCommandBuilder) -> None:
    local_command.start_line = 0

    with pytest.raises(Exception):
        output = run_in_subprocess(local_command.build())
        json.loads(output)

    local_command.start_line = -1

    with pytest.raises(Exception):
        output = run_in_subprocess(local_command.build())
        json.loads(output)


def test_range_filter_when_end_line_is_last(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.end_line = 4  # last line with an error

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == EXPECTED_JSON


def test_range_filter_when_end_line_is_first(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.end_line = 1

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    expected_json_with_one_issue = {
        'quality': {
            'code': 'MODERATE',
            'text': 'Code quality (beta): MODERATE',
        },
        'issues': [{
            'code': 'E225',
            'text': 'missing whitespace around operator',
            'line': 'a=10',
            'line_number': 1,
            'column_number': 2,
            'category': 'CODE_STYLE',
            'influence_on_penalty': 0,
        }],
    }

    assert output_json == expected_json_with_one_issue


def test_range_filter_when_end_line_out_of_range(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.end_line = 10

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == output_json


def test_range_filter_when_both_start_and_end_lines_specified(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 1
    local_command.end_line = 5

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == EXPECTED_JSON


def test_range_filter_when_equal_start_and_end_lines(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 3
    local_command.end_line = 3

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == NO_ISSUES_JSON


def test_range_filter_when_both_start_and_end_lines_specified_not_equal_borders(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 2
    local_command.end_line = 4

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    expected_json = {
        'quality': {
            'code': 'BAD',
            'text': 'Code quality (beta): BAD',
        },
        'issues': [{
            'code': 'E225',
            'text': 'missing whitespace around operator',
            'line': 'b=20',
            'line_number': 2,
            'column_number': 2,
            'category': 'CODE_STYLE',
            'influence_on_penalty': 0,
        }, {
            'code': 'E225',
            'text': 'missing whitespace around operator',
            'line': 'c=a + b',
            'line_number': 4,
            'column_number': 2,
            'category': 'CODE_STYLE',
            'influence_on_penalty': 0,
        }],
    }

    assert output_json == expected_json


def test_range_filter_when_both_start_and_end_lines_out_of_range(
        local_command: LocalCommandBuilder) -> None:
    local_command.path = PATH_TO_FILE
    local_command.format = 'json'
    local_command.start_line = 10
    local_command.end_line = 11

    output = run_in_subprocess(local_command.build())
    output_json = json.loads(output)

    assert output_json == NO_ISSUES_JSON
