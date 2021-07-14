from test.python.inspectors import JAVA_DATA_FOLDER
from test.python.inspectors.conftest import gather_issues_test_info, IssuesTestInfo, use_file_metadata

import pytest
from src.python.review.common.language import Language
from src.python.review.inspectors.checkstyle.checkstyle import CheckstyleInspector
from src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues

FILE_NAMES_AND_N_ISSUES = [
    ('test_simple_valid_program.java', 0),
    ('test_spaces.java', 14),
    ('test_valid_spaces.java', 0),
    ('test_curly_braces.java', 6),
    ('test_valid_curly_braces.java', 0),
    ('test_invalid_naming.java', 14),
    ('test_valid_naming.java', 0),
    ('test_unused_imports.java', 5),
    ('test_blocks.java', 5),
    ('test_valid_blocks.java', 0),
    ('test_magic_numbers.java', 1),
    ('test_ternary_operator.java', 0),
    ('test_todo.java', 0),
    ('test_upper_ell.java', 1),
    ('test_missing_default.java', 1),
    ('test_valid_default.java', 0),
    ('test_array_type.java', 1),
    ('test_algorithm_with_scanner.java', 0),
    ('test_valid_algorithm_1.java', 0),
    ('test_nested_blocks.java', 5),
    ('test_reassigning_example.java', 4),
    ('test_switch_statement.java', 16),
    ('test_when_only_equals_overridden.java', 1),
    ('test_constants.java', 4),
    # ("test_empty_lines_btw_members.java", 2),
    ('test_covariant_equals.java', 1),
    ('test_multi_statements.java', 7),
    ('test_boolean_expr.java', 3),
    ('test_code_with_comments.java', 2),
    ('test_too_long_method.java', 4),
    ('test_cyclomatic_complexity.java', 8),
    ('test_cyclomatic_complexity_bad.java', 22),
    ('test_long_lines.java', 1),
    ('test_indentation_with_spaces.java', 5),
    ('test_indentation_with_tabs.java', 5),
    ('test_indentation_google_style.java', 6),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = CheckstyleInspector()

    path_to_file = JAVA_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})
        issues = filter_low_measure_issues(issues, Language.JAVA)

    assert len(issues) == n_issues


FILE_NAMES_AND_N_ISSUES_INFO = [
    ('test_simple_valid_program.java',
     IssuesTestInfo(n_func_len=1, n_cc=1)),

    ('test_invalid_naming.java',
     IssuesTestInfo(n_code_style=14, n_func_len=3, n_cc=3)),

    ('test_unused_imports.java',
     IssuesTestInfo(n_best_practices=5, n_func_len=1, n_cc=1)),

    ('test_switch_statement.java',
     IssuesTestInfo(n_best_practices=1, n_error_prone=2, n_func_len=5, n_cc=5)),

    ('test_boolean_expr.java',
     IssuesTestInfo(n_best_practices=2, n_func_len=3, n_cc=3, n_bool_expr_len=4)),

    ('test_too_long_method.java',
     IssuesTestInfo(n_func_len=3, n_cc=3)),

    ('test_cyclomatic_complexity.java',
     IssuesTestInfo(n_func_len=5, n_cc=5, n_bool_expr_len=1)),

    ('test_cyclomatic_complexity_bad.java',
     IssuesTestInfo(n_func_len=6, n_cc=6, n_bool_expr_len=9)),
]


@pytest.mark.parametrize(('file_name', 'expected_issues_info'),
                         FILE_NAMES_AND_N_ISSUES_INFO)
def test_file_with_issues_info(file_name: str, expected_issues_info: IssuesTestInfo):
    inspector = CheckstyleInspector()

    path_to_file = JAVA_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issues_info = gather_issues_test_info(issues)
    assert issues_info == expected_issues_info
