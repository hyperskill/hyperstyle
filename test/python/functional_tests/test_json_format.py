import json
import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder

import pytest
from jsonschema import validate


def _get_output_json(local_command: LocalCommandBuilder, new_format: bool) -> str:
    project_path = DATA_PATH / 'file_or_project' / 'project'

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = project_path
    local_command.new_format = new_format

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout = process.stdout.decode()

    return json.loads(stdout)


OLD_FORMAT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'quality': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'code': {'type': 'string'},
                'text': {'type': 'string'},
            },
        },
        'issues': {
            'type': 'array',
            'additionalItems': False,
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'category': {'type': 'string'},
                    'code': {'type': 'string'},
                    'column_number': {'type': 'integer'},
                    'line': {'type': 'string'},
                    'line_number': {'type': 'integer'},
                    'text': {'type': 'string'},
                    'influence_on_penalty': {'type': 'integer'},
                    'difficulty': {'type': 'string'},
                },
            },
        },
    },
}

NEW_FORMAT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'quality': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'code': {'type': 'string'},
                'text': {'type': 'string'},
            },
        },
        'file_review_results': {
            'type': 'array',
            'additionalItems': False,
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'file_name': {'type': 'string'},
                    'quality': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': {
                            'code': {'type': 'string'},
                            'text': {'type': 'string'},
                        },
                    },
                    'issues': {
                        'type': 'array',
                        'additionalItems': False,
                        'items': {
                            'type': 'object',
                            'additionalProperties': False,
                            'properties': {
                                'code': {'type': 'string'},
                                'text': {'type': 'string'},
                                'line': {'type': 'string'},
                                'line_number': {'type': 'integer'},
                                'column_number': {'type': 'integer'},
                                'category': {'type': 'string'},
                                'influence_on_penalty': {'type': 'integer'},
                                'difficulty': {'type': 'string'},
                            },
                        },
                    },
                },
            },
        },
    },
}

JSON_FORMAT_SCHEMA_TEST_DATA = [
    (False, OLD_FORMAT_SCHEMA),
    (True, NEW_FORMAT_SCHEMA),
]


@pytest.mark.parametrize(('new_format', 'schema'), JSON_FORMAT_SCHEMA_TEST_DATA)
def test_json_format_schema(local_command: LocalCommandBuilder, new_format: bool, schema: str):
    validate(_get_output_json(local_command, new_format), schema)


ISSUES = [
    {
        'code': 'W0612',
        'text': 'Unused variable \'a\'',
        'line': 'a = 1',
        'line_number': 2,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': 0,
        'difficulty': 'MEDIUM',
    },
    {
        'code': 'W0612',
        'text': 'Unused variable \'b\'',
        'line': 'b = 2',
        'line_number': 3,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': 0,
        'difficulty': 'MEDIUM',
    },
    {
        'code': 'W0612',
        'text': 'Unused variable \'c\'',
        'line': 'c = 3',
        'line_number': 4,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': 0,
        'difficulty': 'MEDIUM',
    },
]

OLD_FORMAT_EXPECTED_JSON = {
    'quality': {
        'code': 'EXCELLENT',
        'text': 'Code quality (beta): EXCELLENT',
    },
    'issues': ISSUES,
}

NEW_FORMAT_EXPECTED_JSON = {
    'quality': {
        'code': 'EXCELLENT',
        'text': 'Code quality (beta): EXCELLENT',
    },
    'file_review_results': [
        {
            'file_name': '__init__.py',
            'quality': {
                'code': 'EXCELLENT',
                'text': 'Code quality (beta): EXCELLENT',
            },
            'issues': [],
        },
        {
            'file_name': 'one.py',
            'quality': {
                'code': 'EXCELLENT',
                'text': 'Code quality (beta): EXCELLENT',
            },
            'issues': [],
        },
        {
            'file_name': 'other.py',
            'quality': {
                'code': 'GOOD',
                'text': 'Code quality (beta): GOOD',
            },
            'issues': ISSUES,
        },
    ],
}

JSON_FORMAT_TEST_DATA = [
    (False, OLD_FORMAT_EXPECTED_JSON),
    (True, NEW_FORMAT_EXPECTED_JSON),
]


@pytest.mark.parametrize(('new_format', 'expected_json'), JSON_FORMAT_TEST_DATA)
def test_json_format(local_command: LocalCommandBuilder, new_format: bool, expected_json: str):
    assert _get_output_json(local_command, new_format) == expected_json
