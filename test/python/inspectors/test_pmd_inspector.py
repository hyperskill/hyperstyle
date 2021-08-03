from test.python.inspectors import JAVA_DATA_FOLDER

import pytest
from src.python.review.inspectors.pmd.pmd import PMDInspector

from .conftest import use_file_metadata

FILE_NAMES_AND_N_ISSUES = [
    ('test_algorithm_with_scanner.java', 0),
    ('test_simple_valid_program.java', 0),
    ('test_boolean_expr.java', 1),
    ('test_class_with_booleans.java', 3),
    ('test_closing_streams.java', 1),
    ('test_code_with_comments.java', 0),
    ('test_comparing_strings.java', 3),
    ('test_constants.java', 4),
    ('test_covariant_equals.java', 1),
    ('test_curly_braces.java', 0),
    ('test_double_checked_locking.java', 2),
    ('test_for_loop.java', 2),
    ('test_implementation_types.java', 0),
    ('test_manual_array_copy.java', 1),
    ('test_method_params.java', 2),
    ('test_missing_default.java', 2),
    ('test_multi_statements.java', 1),
    ('test_reassigning_example.java', 2),
    ('test_simple_valid_program.java', 0),
    ('test_switch_statement.java', 5),
    ('test_thread_run.java', 1),
    ('test_unused_imports.java', 4),
    ('test_valid_algorithm_1.java', 0),
    ('test_valid_curly_braces.java', 0),
    ('test_when_only_equals_overridden.java', 1),
    ('test_valid_spaces.java', 0),
    ('test_multiple_literals.java', 1),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = PMDInspector()

    path_to_file = JAVA_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})

    assert len(issues) == n_issues
