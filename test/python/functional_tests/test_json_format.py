import json
import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder
from typing import Dict

import pytest
from jsonschema import validate


def _get_output_json(local_command: LocalCommandBuilder, new_format: bool, group_by_difficulty: bool) -> str:
    project_path = DATA_PATH / 'file_or_project' / 'project'

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = project_path
    local_command.new_format = new_format
    local_command.group_by_difficulty = group_by_difficulty

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout = process.stdout.decode()

    return json.loads(stdout)


def _get_by_difficulty_schema(item_schema: Dict) -> Dict:
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'EASY': item_schema,
            'MEDIUM': item_schema,
            'HARD': item_schema,
        },
    }


QUALITY_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'code': {'type': 'string'},
        'text': {'type': 'string'},
    },
}

QUALITY_BY_DIFFICULTY_SCHEMA = _get_by_difficulty_schema(QUALITY_SCHEMA)

INFLUENCE_ON_PENALTY_SCHEMA = {'type': 'integer'}

INFLUENCE_ON_PENALTY_BY_DIFFICULTY_SCHEMA = _get_by_difficulty_schema(INFLUENCE_ON_PENALTY_SCHEMA)


def _get_issues_schema(influence_in_penalty_schema: Dict) -> Dict:
    return {
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
                'influence_on_penalty': influence_in_penalty_schema,
                'difficulty': {'type': 'string'},
            },
        },
    }


def _get_old_format_schema(quality_schema: Dict, influence_in_penalty_schema: Dict) -> Dict:
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'quality': quality_schema,
            'issues': _get_issues_schema(influence_in_penalty_schema),
        },
    }


def _get_new_format_schema(quality_schema: Dict, influence_in_penalty_schema: Dict) -> Dict:
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'quality': quality_schema,
            'file_review_results': {
                'type': 'array',
                'additionalItems': False,
                'items': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'file_name': {'type': 'string'},
                        'quality': quality_schema,
                        'issues': _get_issues_schema(influence_in_penalty_schema),
                    },
                },
            },
        },
    }


JSON_FORMAT_SCHEMA_TEST_DATA = [
    (False, False, _get_old_format_schema(QUALITY_SCHEMA, INFLUENCE_ON_PENALTY_SCHEMA)),
    (True, False, _get_new_format_schema(QUALITY_SCHEMA, INFLUENCE_ON_PENALTY_SCHEMA)),
    (False, True, _get_old_format_schema(QUALITY_BY_DIFFICULTY_SCHEMA, INFLUENCE_ON_PENALTY_BY_DIFFICULTY_SCHEMA)),
    (True, True, _get_new_format_schema(QUALITY_BY_DIFFICULTY_SCHEMA, INFLUENCE_ON_PENALTY_BY_DIFFICULTY_SCHEMA)),
]


@pytest.mark.parametrize(('new_format', 'group_by_difficulty', 'schema'), JSON_FORMAT_SCHEMA_TEST_DATA)
def test_json_format_schema(
    local_command: LocalCommandBuilder, new_format: bool, group_by_difficulty: bool, schema: str,
):
    validate(_get_output_json(local_command, new_format, group_by_difficulty), schema)


# ----------------------------------------------------------------------------------------------------------------------


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

ISSUES_GROUP_BY_DIFFICULTY = [
    {
        'code': 'W0612',
        'text': 'Unused variable \'a\'',
        'line': 'a = 1',
        'line_number': 2,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': {
            'EASY': 0,
            'MEDIUM': 0,
            'HARD': 0,
        },
        'difficulty': 'MEDIUM',
    },
    {
        'code': 'W0612',
        'text': 'Unused variable \'b\'',
        'line': 'b = 2',
        'line_number': 3,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': {
            'EASY': 0,
            'MEDIUM': 0,
            'HARD': 0,
        },
        'difficulty': 'MEDIUM',
    },
    {
        'code': 'W0612',
        'text': 'Unused variable \'c\'',
        'line': 'c = 3',
        'line_number': 4,
        'column_number': 5,
        'category': 'BEST_PRACTICES',
        'influence_on_penalty': {
            'EASY': 0,
            'MEDIUM': 0,
            'HARD': 0,
        },
        'difficulty': 'MEDIUM',
    },
]

OLD_FORMAT_GROUPED_BY_DIFFICULTY_EXPECTED_JSON = {
    'quality': {
        'EASY': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
        'MEDIUM': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
        'HARD': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
    },
    'issues': ISSUES_GROUP_BY_DIFFICULTY,
}

NEW_FORMAT_BY_DIFFICULTY_EXPECTED_JSON = {
    'quality': {
        'EASY': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
        'MEDIUM': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
        'HARD': {
            'code': 'EXCELLENT',
            'text': 'Code quality (beta): EXCELLENT',
        },
    },
    'file_review_results': [
        {
            'file_name': '__init__.py',
            'quality': {
                'EASY': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
                'MEDIUM': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
                'HARD': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
            },
            'issues': [],
        },
        {
            'file_name': 'one.py',
            'quality': {
                'EASY': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
                'MEDIUM': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
                'HARD': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
            },
            'issues': [],
        },
        {
            'file_name': 'other.py',
            'quality': {
                'EASY': {
                    'code': 'EXCELLENT',
                    'text': 'Code quality (beta): EXCELLENT',
                },
                'MEDIUM': {
                    'code': 'GOOD',
                    'text': 'Code quality (beta): GOOD',
                },
                'HARD': {
                    'code': 'GOOD',
                    'text': 'Code quality (beta): GOOD',
                },
            },
            'issues': ISSUES_GROUP_BY_DIFFICULTY,
        },
    ],
}

JSON_FORMAT_TEST_DATA = [
    (False, False, OLD_FORMAT_EXPECTED_JSON),
    (True, False, NEW_FORMAT_EXPECTED_JSON),
    (False, True, OLD_FORMAT_GROUPED_BY_DIFFICULTY_EXPECTED_JSON),
    (True, True, NEW_FORMAT_BY_DIFFICULTY_EXPECTED_JSON),
]


@pytest.mark.parametrize(('new_format', 'group_by_difficulty', 'expected_json'), JSON_FORMAT_TEST_DATA)
def test_json_format(
    local_command: LocalCommandBuilder, new_format: bool, group_by_difficulty: bool, expected_json: str,
):
    assert _get_output_json(local_command, new_format, group_by_difficulty) == expected_json
