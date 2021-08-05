import json
import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder

import pytest
from jsonschema import validate

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
                },
            },
        },
    },
}

NEW_FORMAT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "quality": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "code": {"type": "string"},
                "text": {"type": "string"},
            },
        },
        "file_review_results": {
            "type": "array",
            "additionalItems": False,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "file_name": {"type": "string"},
                    "quality": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "code": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                    "issues": {
                        "type": "array",
                        "additionalItems": False,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "code": {"type": "string"},
                                "text": {"type": "string"},
                                "line": {"type": "string"},
                                "line_number": {"type": "integer"},
                                "column_number": {"type": "integer"},
                                "category": {"type": "string"},
                                "influence_on_penalty": {"type": "integer"},
                            },
                        },
                    },
                },
            },
        },
    },
}

JSON_FORMAT_TEST_DATA = [
    (False, OLD_FORMAT_SCHEMA),
    (True, NEW_FORMAT_SCHEMA),
]


@pytest.mark.parametrize(('new_format', 'schema'), JSON_FORMAT_TEST_DATA)
def test_json_format(local_command: LocalCommandBuilder, new_format: bool, schema: str):
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

    output_json = json.loads(stdout)
    validate(output_json, schema)
