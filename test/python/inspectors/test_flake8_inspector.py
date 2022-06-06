from test.python.inspectors import PYTHON_DATA_FOLDER
from test.python.inspectors.conftest import gather_issues_test_info, IssuesTestInfo, use_file_metadata
from textwrap import dedent

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.flake8.flake8 import Flake8Inspector
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues

FILE_NAMES_AND_N_ISSUES = [
    ('case0_spaces.py', 5),
    ('case1_simple_valid_program.py', 0),
    ('case2_boolean_expressions.py', 7),
    ('case3_redefining_builtin.py', 2),
    ('case4_naming.py', 8),
    ('case5_returns.py', 1),
    ('case6_unused_variables.py', 3),
    ('case8_good_class.py', 0),
    ('case7_empty_lines.py', 1),
    ('case10_unused_variable_in_loop.py', 1),
    ('case13_complex_logic.py', 12),
    ('case13_complex_logic_2.py', 2),
    ('case11_redundant_parentheses.py', 0),
    ('case14_returns_errors.py', 4),
    ('case16_comments.py', 0),
    ('case17_dangerous_default_value.py', 1),
    ('case18_comprehensions.py', 9),
    ('case19_bad_indentation.py', 3),
    ('case21_imports.py', 2),
    ('case25_django.py', 0),
    ('case31_spellcheck.py', 0),
    ('case32_string_format.py', 34),
    ('case33_commas.py', 14),
    ('case34_cohesion.py', 1),
    ('case35_line_break.py', 11),
    ('case36_unpacking.py', 0),
    ('case37_wildcard_import.py', 1),
    ('case38_spellcheck.py', 0),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = Flake8Inspector()

    path_to_file = PYTHON_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})
        issues = list(filter(lambda i: i.type != IssueType.INFO, filter_low_measure_issues(issues, Language.PYTHON)))

        assert len(issues) == n_issues


FILE_NAMES_AND_N_ISSUES_INFO = [
    ('case0_spaces.py', IssuesTestInfo(n_code_style=5)),
    ('case1_simple_valid_program.py', IssuesTestInfo()),
    ('case2_boolean_expressions.py', IssuesTestInfo(n_code_style=1,
                                                    n_best_practices=4,
                                                    n_error_prone=1,
                                                    n_cc=8,
                                                    n_other_complexity=1)),
    ('case3_redefining_builtin.py', IssuesTestInfo(n_error_prone=2)),
    ('case4_naming.py', IssuesTestInfo(n_code_style=7, n_cc=5, n_cohesion=1)),
    ('case6_unused_variables.py', IssuesTestInfo(n_best_practices=3,
                                                 n_cc=1)),
    ('case8_good_class.py', IssuesTestInfo(n_cc=1, n_cohesion=1)),
    ('case7_empty_lines.py', IssuesTestInfo(n_cc=5, n_cohesion=2)),
    ('case10_unused_variable_in_loop.py', IssuesTestInfo(n_best_practices=1,
                                                         n_cc=1)),
    ('case13_complex_logic.py', IssuesTestInfo(n_cc=5, n_other_complexity=10)),
    ('case13_complex_logic_2.py', IssuesTestInfo(n_cc=2, n_other_complexity=1)),
    ('case14_returns_errors.py', IssuesTestInfo(n_best_practices=1,
                                                n_error_prone=3,
                                                n_cc=4)),
    ('case35_line_break.py', IssuesTestInfo(n_best_practices=1,
                                            n_code_style=10,
                                            n_cc=1)),
    ('case32_string_format.py', IssuesTestInfo(n_error_prone=28, n_other_complexity=6)),
    ('case33_commas.py', IssuesTestInfo(n_code_style=14, n_cc=4)),
    ('case34_cohesion.py', IssuesTestInfo(n_cc=6, n_cohesion=2)),
    ('case36_unpacking.py', IssuesTestInfo(n_cc=1)),
    ('case37_wildcard_import.py', IssuesTestInfo(n_best_practices=1, n_cc=1)),
]


@pytest.mark.parametrize(('file_name', 'expected_issues_info'), FILE_NAMES_AND_N_ISSUES_INFO)
def test_file_with_issues_info(file_name: str, expected_issues_info: IssuesTestInfo):
    inspector = Flake8Inspector()

    path_to_file = PYTHON_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issues_info = gather_issues_test_info(issues)
    assert issues_info == expected_issues_info


def test_parse():
    file_name = 'test.py'
    output = f"""\
        {file_name}:1:11:W602:test 1
        {file_name}:2:12:E703:test 2
        {file_name}:3:13:SC200:test 3
    """
    output = dedent(output)

    issues = Flake8Inspector.parse(output)

    assert all(str(issue.file_path) == file_name for issue in issues)
    assert [issue.line_no for issue in issues] == [1, 2, 3]
    assert [issue.column_no for issue in issues] == [11, 12, 13]
    assert [issue.description for issue in issues] == ['test 1', 'test 2', 'test 3']
    assert [issue.type for issue in issues] == [IssueType.CODE_STYLE,
                                                IssueType.CODE_STYLE,
                                                IssueType.INFO]


def test_choose_issue_type():
    error_codes = ['B006', 'SC100', 'R503', 'ABC123', 'E101']
    expected_issue_types = [
        IssueType.ERROR_PRONE, IssueType.INFO,
        IssueType.ERROR_PRONE, IssueType.BEST_PRACTICES,
        IssueType.CODE_STYLE,
    ]

    issue_types = list(map(Flake8Inspector.choose_issue_type, error_codes))

    assert issue_types == expected_issue_types
