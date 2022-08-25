import textwrap
from test.python.inspectors import PYLINT_DATA_FOLDER, PYTHON_DATA_FOLDER

import pytest
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.inspectors.pylint.pylint import PylintInspector

from .conftest import use_file_metadata

FILE_NAMES_AND_N_ISSUES = [
    ('case0_spaces.py', 0),
    ('case1_simple_valid_program.py', 0),
    ('case2_boolean_expressions.py', 3),
    ('case3_redefining_builtin.py', 0),
    ('case4_naming.py', 3),
    ('case5_returns.py', 1),
    ('case6_unused_variables.py', 4),
    ('case8_good_class.py', 0),
    ('case20_imports_order.py', 0),
    ('case10_unused_variable_in_loop.py', 1),
    ('case11_redundant_parentheses.py', 2),
    ('case12_unreachable_code.py', 2),
    ('case14_returns_errors.py', 3),
    ('case15_redefining.py', 2),
    ('case16_comments.py', 0),
    ('case17_dangerous_default_value.py', 1),
    ('case18_comprehensions.py', 3),
    ('case19_bad_indentation.py', 2),
    ('case21_imports.py', 2),
    ('case23_merging_comparisons.py', 4),
    ('case24_long_function.py', 0),
    ('case25_django.py', 0),
    ('case27_using_requests.py', 0),
    ('case30_allow_else_return.py', 0),
    ('case36_unpacking.py', 0),
    ('case37_wildcard_import.py', 1),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = PylintInspector()

    path_to_file = PYTHON_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    assert len(issues) == n_issues


def test_parse():
    file_name = 'test.py'
    output = f"""\
        {file_name}:1:11:R0123:test 1
        {file_name}:2:12:C1444:test 2
    """
    output = textwrap.dedent(output)

    issues = PylintInspector.parse(output)

    assert all(str(issue.file_path) == file_name for issue in issues)
    assert [issue.line_no for issue in issues] == [1, 2]
    assert [issue.column_no for issue in issues] == [12, 13]  # columns start from 1
    assert [issue.description for issue in issues] == ['test 1', 'test 2']

    expected_issue_types = [IssueType.BEST_PRACTICES,
                            IssueType.CODE_STYLE]
    assert [issue.type for issue in issues] == expected_issue_types


def test_choose_issue_type():
    error_categories = ['W', 'R', 'C', 'E']
    expected_issue_types = [
        IssueType.BEST_PRACTICES,
        IssueType.BEST_PRACTICES,
        IssueType.CODE_STYLE,
        IssueType.ERROR_PRONE,
    ]

    issue_types = list(
        map(PylintInspector.choose_issue_type, error_categories))

    assert issue_types == expected_issue_types


NEW_DESCRIPTION_TEST_DATA = [
    (
        'W1404',
        'Found implicit string concatenation. If you want to concatenate strings, use "+".',
    ),
    (
        'R1721',
        'Unnecessary use of a comprehension. Instead of using an identity comprehension, '
        'consider using the list, dict or set constructor. It is faster and simpler. '
        'For example, instead of {key: value for key, value in list_of_tuples} use dict(list_of_tuples).',
    ),
]


@pytest.mark.parametrize(('origin_class', 'expected_description'), NEW_DESCRIPTION_TEST_DATA)
def test_new_issue_description(origin_class: str, expected_description: str):
    inspector = PylintInspector()

    path_to_file = PYLINT_DATA_FOLDER / 'issues' / f'{origin_class.lower()}.py'
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.description == expected_description
