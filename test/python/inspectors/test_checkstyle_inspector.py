from pathlib import Path
from test.python.inspectors import CHECKSTYLE_DATA_FOLDER, JAVA_DATA_FOLDER
from test.python.inspectors.conftest import gather_issues_test_info, IssuesTestInfo, use_file_metadata
from typing import List

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.checkstyle.checkstyle import CheckstyleInspector
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BoolExprLenIssue,
    CodeIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueDifficulty,
    IssueType,
    LineLenIssue,
)
from hyperstyle.src.python.review.inspectors.parsers.xml_parser import parse_xml_file_result
from hyperstyle.src.python.review.inspectors.tips import (
    get_bool_expr_len_tip,
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
)
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues

FILE_NAME_AND_ISSUES = [
    ('empty_file.xml', []),
    ('single_file_project_without_issues.xml', []),
    ('multi_file_project_without_issues.xml', []),
    (
        'single_file_project_without_metric_issues.xml',
        [
            CodeIssue(
                origin_class='MultipleStringLiteralsCheck', type=IssueType.BEST_PRACTICES,
                description='The String "Howdy" appears 4 times in the file.',
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=6, column_no=13, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CodeIssue(
                origin_class='WhitespaceAroundCheck', type=IssueType.CODE_STYLE,
                description="'{' is not followed by whitespace.",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=12, column_no=32, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.EASY,
            ),
            CodeIssue(
                origin_class='StringLiteralEqualityCheck', type=IssueType.ERROR_PRONE,
                description="Literal Strings should be compared using equals(), not '=='.",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=37, column_no=33, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.HARD,
            ),
        ],
    ),
    (
        'single_file_project_with_metric_issues.xml',
        [
            FuncLenIssue(
                origin_class='JavaNCSSCheck', type=IssueType.FUNC_LEN,
                description=get_func_len_tip(),
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=5, column_no=5, inspector_type=InspectorType.CHECKSTYLE,
                func_len=42, difficulty=IssueDifficulty.EASY,
            ),
            CyclomaticComplexityIssue(
                origin_class='CyclomaticComplexityCheck', type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip(),
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=5, column_no=5, inspector_type=InspectorType.CHECKSTYLE,
                cc_value=69, difficulty=IssueDifficulty.HARD,
            ),
            CodeIssue(
                origin_class='WhitespaceAroundCheck', type=IssueType.CODE_STYLE,
                description="'switch' is not followed by whitespace.",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=31, column_no=25, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.EASY,
            ),
        ],
    ),
    (
        'multi_file_project_without_metric_issues.xml',
        [
            CodeIssue(
                origin_class='EmptyBlockCheck', type=IssueType.BEST_PRACTICES,
                description='Must have at least one statement.',
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=62, column_no=38, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CodeIssue(
                origin_class='CovariantEqualsCheck', type=IssueType.ERROR_PRONE,
                description='covariant equals without overriding equals(java.lang.Object).',
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=68, column_no=20, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.HARD,
            ),
            CodeIssue(
                origin_class='IndentationCheck', type=IssueType.CODE_STYLE,
                description="'if' child has incorrect indentation level 2, expected level should be 12.",
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=116, column_no=3, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.EASY,
            ),
            CodeIssue(
                origin_class='UpperEllCheck', type=IssueType.BEST_PRACTICES,
                description="Should use uppercase 'L'.",
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=123, column_no=15, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.MEDIUM,
            ),
        ],
    ),
    (
        'multi_file_project_with_metric_issues.xml',
        [
            CodeIssue(
                origin_class='OneStatementPerLineCheck', type=IssueType.CODE_STYLE,
                description='Only one statement per line allowed.',
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=69, column_no=31, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.EASY,
            ),
            BoolExprLenIssue(
                origin_class='BooleanExpressionComplexityCheck', type=IssueType.BOOL_EXPR_LEN,
                description=get_bool_expr_len_tip(),
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=112, column_no=9, inspector_type=InspectorType.CHECKSTYLE, bool_expr_len=77,
                difficulty=IssueDifficulty.EASY,
            ),
            LineLenIssue(
                origin_class='LineLengthCheck', type=IssueType.LINE_LEN,
                description=get_line_len_tip(),
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=62, column_no=1, inspector_type=InspectorType.CHECKSTYLE, line_len=228,
                difficulty=IssueDifficulty.EASY,
            ),
            CodeIssue(
                origin_class='WhitespaceAfterCheck', type=IssueType.CODE_STYLE,
                description="',' is not followed by whitespace.",
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=136, column_no=19, inspector_type=InspectorType.CHECKSTYLE,
                difficulty=IssueDifficulty.EASY,
            ),
        ],
    ),
]


@pytest.mark.parametrize(('file_name', 'expected_issues'), FILE_NAME_AND_ISSUES)
def test_output_parsing(file_name: str, expected_issues: List[CodeIssue]):
    path_to_file = CHECKSTYLE_DATA_FOLDER / file_name
    issues = parse_xml_file_result(
        path_to_file,
        InspectorType.CHECKSTYLE,
        CheckstyleInspector.choose_issue_type,
        IssueDifficulty.get_by_issue_type,
        CheckstyleInspector.origin_class_to_pattern,
        {},
    )
    assert issues == expected_issues


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
    ('test_boolean_expr.java', 4),
    ('test_code_with_comments.java', 2),
    ('test_too_long_method.java', 4),
    ('test_cyclomatic_complexity.java', 8),
    ('test_cyclomatic_complexity_bad.java', 22),
    ('test_long_lines.java', 1),
    ('test_indentation_with_spaces.java', 5),
    ('test_indentation_with_tabs.java', 5),
    ('test_indentation_google_style.java', 6),
    ('test_multiple_literals.java', 1),
    ('test_pattern_matching.java', 2),
    ('test_records.java', 2),
    ('test_sealed_classes.java', 5),
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
