import json
import subprocess

from jsonschema import validate

from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder

schema = {
    'type': 'object',
    'properties': {
        'quality': {
            'type': 'object',
            'properties': {
                'code': {'type': 'string'},
                'text': {'type': 'string'}
            }
        },
        'issues': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'category': {'type': 'string'},
                    'code': {'type': 'string'},
                    'column_number': {'type': 'number'},
                    'line': {'type': 'string'},
                    'line_number': {'type': 'number'},
                    'text': {'type': 'string'}
                }
            }
        }
    }
}


def test_json_format(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'json_format' / 'code_with_issues.py'

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = file_path

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout = process.stdout.decode()

    output_json = json.loads(stdout)
    validate(output_json, schema)
