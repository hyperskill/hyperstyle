import json
import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder
from typing import Dict

import pytest


def _get_output_json(local_command: LocalCommandBuilder, file_path: str) -> Dict:
    file_path = DATA_PATH / 'difficulty_levels' / file_path

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = file_path
    local_command.new_format = False
    local_command.group_by_difficulty = True

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return json.loads(process.stdout.decode())


WITHOUT_ISSUES = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'HARD': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'MEDIUM': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
    },
    'issues': [],
}


HARD_ISSUES = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'MEDIUM': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'HARD': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
    },
    'issues': [
        {
            'category': 'COMPLEXITY',
            'code': 'H601',
            'column_number': 1,
            'difficulty': 'HARD',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'class BadClass:',
            'line_number': 4,
            'text': 'class has low (33.33%) cohesion',
        },
    ],
}

MEDIUM_ISSUES = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'HARD': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
        'MEDIUM': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
    },
    'issues': [
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS407',
            'column_number': 1,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'MUTABLE_CONSTANT = {"1": 1, "2": 2}',
            'line_number': 1,
            'text': 'Found mutable module constant',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 6,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'PI = 3.14',
            'line_number': 3,
            'text': 'Found approximate constant: 3.14',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 13,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'DOUBLE_PI = 6.28',
            'line_number': 4,
            'text': 'Found approximate constant: 6.28',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 5,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'E = 2.71',
            'line_number': 5,
            'text': 'Found approximate constant: 2.71',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'W0703',
            'column_number': 12,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'except Exception:',
            'line_number': 13,
            'text': 'Catching too general exception Exception',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'R504',
            'column_number': 12,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'return result',
            'line_number': 16,
            'text': 'you shouldn`t assign value to variable if it will be use ' 'only as return value',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'R1708',
            'column_number': 9,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'raise StopIteration',
            'line_number': 21,
            'text': 'Do not raise StopIteration in generator, use return ' 'statement instead',
        },
    ],
}


EASY_ISSUES = {
    'quality': {
        'EASY': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'MEDIUM': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'HARD': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
    },
    'issues': [
        {
            'code': 'N802',
            'text': "function name 'MAIN' should be lowercase",
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'column_number': 6,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
        {
            'code': 'N803',
            'text': "argument name 'Number' should be lowercase",
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'column_number': 11,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
        {
            'code': 'E221',
            'text': 'multiple spaces before operator',
            'line': 'if Number    > 0:',
            'line_number': 2,
            'column_number': 14,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
        {
            'code': 'E221',
            'text': 'multiple spaces before operator',
            'line': 'if __name__    == "__main__":',
            'line_number': 7,
            'column_number': 12,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
        {
            'code': 'E121',
            'text': 'continuation line under-indented for hanging indent',
            'line': '"Hello, World")',
            'line_number': 9,
            'column_number': 7,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
        {
            'code': 'WPS319',
            'text': 'Found bracket in wrong position',
            'line': '"Hello, World")',
            'line_number': 9,
            'column_number': 21,
            'category': 'CODE_STYLE',
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
        },
    ],
}


DIFFICULTY_LEVELS_TEST_DATA = [
    ('file_without_issues.py', WITHOUT_ISSUES),
    ('file_with_only_hard_issues.py', HARD_ISSUES),
    ('file_with_only_medium_issues.py', MEDIUM_ISSUES),
    ('file_with_only_easy_issues.py', EASY_ISSUES),
]


@pytest.mark.parametrize(('file', 'expected_json'), DIFFICULTY_LEVELS_TEST_DATA)
def test_difficulty_levels(local_command: LocalCommandBuilder, file: str, expected_json: Dict):
    assert _get_output_json(local_command, file) == expected_json
