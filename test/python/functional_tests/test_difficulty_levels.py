import json
import subprocess
from test.python.functional_tests.conftest import DATA_PATH, LocalCommandBuilder
from typing import Dict, Optional

import pytest


def _get_output_json(local_command: LocalCommandBuilder, file_path: str, history: Optional[str] = None) -> Dict:
    file_path = DATA_PATH / 'difficulty_levels' / file_path

    local_command.verbosity = 0
    local_command.format = 'json'
    local_command.path = file_path
    local_command.new_format = False
    local_command.group_by_difficulty = True
    local_command.history = history

    process = subprocess.run(
        local_command.build(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return json.loads(process.stdout.decode())


WITHOUT_ISSUES = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'MEDIUM': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'HARD': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
    },
    'issues': [],
}

HARD_ISSUES = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'MEDIUM': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'HARD': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
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
            'text': 'class has low (20.00%) cohesion',
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
        'EASY': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
        'MEDIUM': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
        'HARD': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
    },
    'issues': [
        {
            'category': 'CODE_STYLE',
            'code': 'N802',
            'column_number': 6,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'text': "function name 'MAIN' should be lowercase",
        },
        {
            'category': 'CODE_STYLE',
            'code': 'N803',
            'column_number': 11,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'text': "argument name 'Number' should be lowercase",
        },
        {
            'category': 'CODE_STYLE',
            'code': 'E121',
            'column_number': 7,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': '"Hello, World")',
            'line_number': 10,
            'text': 'continuation line under-indented for hanging indent',
        },
    ],
}


ALL_DIFFICULTY_LEVEL_ISSUES = {
    'quality': {
        'EASY': {'code': 'GOOD', 'text': 'Code quality (beta): GOOD'},
        'MEDIUM': {'code': 'GOOD', 'text': 'Code quality (beta): GOOD'},
        'HARD': {'code': 'MODERATE', 'text': 'Code quality (beta): MODERATE'},
    },
    'issues': [
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS407',
            'column_number': 1,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'MUTABLE_CONSTANT = {"1": 1, "2": 2}',
            'line_number': 3,
            'text': 'Found mutable module constant',
        },
        {
            'category': 'COMPLEXITY',
            'code': 'H601',
            'column_number': 1,
            'difficulty': 'HARD',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'class BadClass:',
            'line_number': 5,
            'text': 'class has low (20.00%) cohesion',
        },
        {
            'category': 'CODE_STYLE',
            'code': 'N802',
            'column_number': 10,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'HARD': 0, 'MEDIUM': 0},
            'line': 'def Length(x: int, y: int) -> float:',
            'line_number': 11,
            'text': "function name 'Length' should be lowercase",
        },
    ],
}


DIFFICULTY_LEVELS_TEST_DATA = [
    ('file_without_issues.py', WITHOUT_ISSUES),
    ('file_with_only_hard_issues.py', HARD_ISSUES),
    ('file_with_only_medium_issues.py', MEDIUM_ISSUES),
    ('file_with_only_easy_issues.py', EASY_ISSUES),
    ('file_with_all_difficulty_levels.py', ALL_DIFFICULTY_LEVEL_ISSUES),
]


@pytest.mark.parametrize(('file', 'expected_json'), DIFFICULTY_LEVELS_TEST_DATA)
def test_difficulty_levels(local_command: LocalCommandBuilder, file: str, expected_json: Dict):
    assert _get_output_json(local_command, file) == expected_json


HISTORY = {
    'python': [
        {
            'origin_class': 'N802',
            'number': 5,
        },
        {
            'origin_class': 'WPS407',
            'number': 10,
        },
        {
            'origin_class': 'H601',
            'number': 5,
        },
    ],
}

HARD_ISSUES_WITH_INFLUENCE = {
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
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 100},
            'line': 'class BadClass:',
            'line_number': 4,
            'text': 'class has low (20.00%) cohesion',
        },
    ],
}

MEDIUM_ISSUES_WITH_INFLUENCE = {
    'quality': {
        'EASY': {'code': 'EXCELLENT', 'text': 'Code quality (beta): EXCELLENT'},
        'MEDIUM': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'HARD': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
    },
    'issues': [
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS407',
            'column_number': 1,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 100, 'HARD': 100},
            'line': 'MUTABLE_CONSTANT = {"1": 1, "2": 2}',
            'line_number': 1,
            'text': 'Found mutable module constant',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 6,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'PI = 3.14',
            'line_number': 3,
            'text': 'Found approximate constant: 3.14',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 13,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'DOUBLE_PI = 6.28',
            'line_number': 4,
            'text': 'Found approximate constant: 6.28',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS446',
            'column_number': 5,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'E = 2.71',
            'line_number': 5,
            'text': 'Found approximate constant: 2.71',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'W0703',
            'column_number': 12,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'except Exception:',
            'line_number': 13,
            'text': 'Catching too general exception Exception',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'R504',
            'column_number': 12,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'return result',
            'line_number': 16,
            'text': 'you shouldn`t assign value to variable if it will be use ' 'only as return value',
        },
        {
            'category': 'BEST_PRACTICES',
            'code': 'R1708',
            'column_number': 9,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'raise StopIteration',
            'line_number': 21,
            'text': 'Do not raise StopIteration in generator, use return ' 'statement instead',
        },
    ],
}

EASY_ISSUES_WITH_INFLUENCE = {
    'quality': {
        'EASY': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'MEDIUM': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'HARD': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
    },
    'issues': [
        {
            'category': 'CODE_STYLE',
            'code': 'N802',
            'column_number': 6,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 100, 'MEDIUM': 100, 'HARD': 100},
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'text': "function name 'MAIN' should be lowercase",
        },
        {
            'category': 'CODE_STYLE',
            'code': 'N803',
            'column_number': 11,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': 'def MAIN(Number):',
            'line_number': 1,
            'text': "argument name 'Number' should be lowercase",
        },
        {
            'category': 'CODE_STYLE',
            'code': 'E121',
            'column_number': 7,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 0},
            'line': '"Hello, World")',
            'line_number': 10,
            'text': 'continuation line under-indented for hanging indent',
        },
    ],
}

ALL_DIFFICULTY_LEVEL_ISSUES_WITH_INFLUENCE = {
    'quality': {
        'EASY': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'MEDIUM': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
        'HARD': {'code': 'BAD', 'text': 'Code quality (beta): BAD'},
    },
    'issues': [
        {
            'category': 'BEST_PRACTICES',
            'code': 'WPS407',
            'column_number': 1,
            'difficulty': 'MEDIUM',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 64, 'HARD': 52},
            'line': 'MUTABLE_CONSTANT = {"1": 1, "2": 2}',
            'line_number': 3,
            'text': 'Found mutable module constant',
        },
        {
            'category': 'COMPLEXITY',
            'code': 'H601',
            'column_number': 1,
            'difficulty': 'HARD',
            'influence_on_penalty': {'EASY': 0, 'MEDIUM': 0, 'HARD': 17},
            'line': 'class BadClass:',
            'line_number': 5,
            'text': 'class has low (20.00%) cohesion',
        },
        {
            'category': 'CODE_STYLE',
            'code': 'N802',
            'column_number': 10,
            'difficulty': 'EASY',
            'influence_on_penalty': {'EASY': 100, 'MEDIUM': 35, 'HARD': 29},
            'line': 'def Length(x: int, y: int) -> float:',
            'line_number': 11,
            'text': "function name 'Length' should be lowercase",
        },
    ],
}

DIFFICULTY_LEVELS_WITH_HISTORY_TEST_DATA = [
    ('file_without_issues.py', WITHOUT_ISSUES),
    ('file_with_only_hard_issues.py', HARD_ISSUES_WITH_INFLUENCE),
    ('file_with_only_medium_issues.py', MEDIUM_ISSUES_WITH_INFLUENCE),
    ('file_with_only_easy_issues.py', EASY_ISSUES_WITH_INFLUENCE),
    ('file_with_all_difficulty_levels.py', ALL_DIFFICULTY_LEVEL_ISSUES_WITH_INFLUENCE),
]


@pytest.mark.parametrize(('file', 'expected_json'), DIFFICULTY_LEVELS_WITH_HISTORY_TEST_DATA)
def test_difficulty_levels_with_history(local_command: LocalCommandBuilder, file: str, expected_json: Dict):
    assert _get_output_json(local_command, file, json.dumps(HISTORY)) == expected_json
