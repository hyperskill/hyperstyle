import json
import subprocess

from functional_tests.tests.conftest import DATA_PATH, LocalCommandBuilder

EXPECTED_JSON = {
    'quality': {
        'code': 'EXCELLENT',
        'text': 'Code quality (beta): EXCELLENT'
    },
    'file_review_results': [
        {
            'file_name': '__init__.py',
            'quality': {
                'code': 'EXCELLENT',
                'text': 'Code quality (beta): EXCELLENT'
            },
            'issues': []
        },
        {
            'file_name': 'one.py',
            'quality': {
                'code': 'EXCELLENT',
                'text': 'Code quality (beta): EXCELLENT'
            },
            'issues': []
        },
        {
            'file_name': 'other.py',
            'quality': {
                'code': 'GOOD',
                'text': 'Code quality (beta): GOOD'
            },
            'issues': [
                {
                    'code': 'W0612',
                    'text': 'Unused variable \'a\'',
                    'line': 'a = 1',
                    'line_number': 2,
                    'column_number': 5,
                    'category': 'BEST_PRACTICES'
                },
                {
                    'code': 'W0612',
                    'text': 'Unused variable \'b\'',
                    'line': 'b = 2',
                    'line_number': 3,
                    'column_number': 5,
                    'category': 'BEST_PRACTICES'
                },
                {
                    'code': 'W0612',
                    'text': 'Unused variable \'c\'',
                    'line': 'c = 3',
                    'line_number': 4,
                    'column_number': 5,
                    'category': 'BEST_PRACTICES'
                }
            ]
        },
    ]
}


def test_json_format(local_command: LocalCommandBuilder):
    file_path = DATA_PATH / 'file_or_project' / 'project'

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = file_path
    local_command.new_format = True

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout = process.stdout.decode()
    print(stdout)

    output_json = json.loads(stdout)

    assert output_json == EXPECTED_JSON
