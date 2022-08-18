from pathlib import Path
from test.python.inspectors import JAVA_DATA_FOLDER, PMD_DATA_FOLDER
from typing import List

import pytest
from hyperstyle.src.python.review.application_config import LanguageVersion
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import CodeIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.pmd.pmd import DEFAULT_JAVA_VERSION, PMDInspector

from .conftest import use_file_metadata

FILE_NAME_AND_ISSUES = [
    ('empty_file.csv', []),
    ('project_without_issues.csv', []),
    (
        'single_file_project.csv',
        [
            CodeIssue(
                origin_class='AvoidDuplicateLiterals', type=IssueType.BEST_PRACTICES,
                description="The String literal 'Howdy' appears 4 times in this file; "
                            "the first occurrence is on line 6",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=6, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CodeIssue(
                origin_class='UncommentedEmptyMethodBody', type=IssueType.BEST_PRACTICES,
                description='Document empty method body',
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=12, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CodeIssue(
                origin_class='UnusedLocalVariable', type=IssueType.BEST_PRACTICES,
                description="Avoid unused local variables such as 'result'.",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=31, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CodeIssue(
                origin_class='UnusedPrivateMethod', type=IssueType.BEST_PRACTICES,
                description="Avoid unused private methods such as 'emptyLoop()'.",
                file_path=Path('/home/user/Desktop/some_project/main.java'),
                line_no=61, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.MEDIUM,
            ),
        ],
    ),
    (
        'multi_file_project.csv',
        [
            CodeIssue(
                origin_class='CompareObjectsWithEquals', type=IssueType.ERROR_PRONE,
                description='Use equals() to compare object references.',
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=37, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.HARD,
            ),
            CodeIssue(
                origin_class='SuspiciousEqualsMethodName', type=IssueType.ERROR_PRONE,
                description='The method name and parameter number are suspiciously close to equals(Object)',
                file_path=Path('/home/user/Desktop/some_project/main1.java'),
                line_no=68, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.HARD,
            ),
            CodeIssue(
                origin_class='UselessParentheses', type=IssueType.CODE_STYLE,
                description='Useless parentheses.',
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=113, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.EASY,
            ),
            CodeIssue(
                origin_class='EmptyIfStmt', type=IssueType.BEST_PRACTICES,
                description='Avoid empty if statements',
                file_path=Path('/home/user/Desktop/some_project/main2.java'),
                line_no=131, column_no=1, inspector_type=InspectorType.PMD,
                difficulty=IssueDifficulty.MEDIUM,
            ),
        ],
    ),
]


@pytest.mark.parametrize(('file_name', 'expected_issues'), FILE_NAME_AND_ISSUES)
def test_output_parsing(file_name: str, expected_issues: List[CodeIssue]):
    path_to_file = PMD_DATA_FOLDER / file_name
    issues = PMDInspector().parse_output(path_to_file)
    assert issues == expected_issues


FILE_NAMES_AND_N_ISSUES = [
    ('test_algorithm_with_scanner.java', 0, DEFAULT_JAVA_VERSION),
    ('test_simple_valid_program.java', 0, DEFAULT_JAVA_VERSION),
    ('test_boolean_expr.java', 1, DEFAULT_JAVA_VERSION),
    ('test_class_with_booleans.java', 3, DEFAULT_JAVA_VERSION),
    ('test_closing_streams.java', 1, DEFAULT_JAVA_VERSION),
    ('test_code_with_comments.java', 0, DEFAULT_JAVA_VERSION),
    ('test_comparing_strings.java', 4, DEFAULT_JAVA_VERSION),
    ('test_constants.java', 4, DEFAULT_JAVA_VERSION),
    ('test_covariant_equals.java', 1, DEFAULT_JAVA_VERSION),
    ('test_curly_braces.java', 0, DEFAULT_JAVA_VERSION),
    ('test_double_checked_locking.java', 2, DEFAULT_JAVA_VERSION),
    ('test_for_loop.java', 2, DEFAULT_JAVA_VERSION),
    ('test_implementation_types.java', 0, DEFAULT_JAVA_VERSION),
    ('test_manual_array_copy.java', 1, DEFAULT_JAVA_VERSION),
    ('test_method_params.java', 2, DEFAULT_JAVA_VERSION),
    ('test_missing_default.java', 2, DEFAULT_JAVA_VERSION),
    ('test_multi_statements.java', 1, DEFAULT_JAVA_VERSION),
    ('test_reassigning_example.java', 2, DEFAULT_JAVA_VERSION),
    ('test_simple_valid_program.java', 0, DEFAULT_JAVA_VERSION),
    ('test_switch_statement.java', 5, DEFAULT_JAVA_VERSION),
    ('test_thread_run.java', 1, DEFAULT_JAVA_VERSION),
    ('test_unused_imports.java', 4, DEFAULT_JAVA_VERSION),
    ('test_valid_algorithm_1.java', 0, DEFAULT_JAVA_VERSION),
    ('test_valid_curly_braces.java', 0, DEFAULT_JAVA_VERSION),
    ('test_when_only_equals_overridden.java', 1, DEFAULT_JAVA_VERSION),
    ('test_valid_spaces.java', 0, DEFAULT_JAVA_VERSION),
    ('test_multiple_literals.java', 1, DEFAULT_JAVA_VERSION),
    ('test_pattern_matching.java', 1, LanguageVersion.JAVA_17),
    ('test_records.java', 1, LanguageVersion.JAVA_17),
    ('test_sealed_classes.java', 2, LanguageVersion.JAVA_17),
]


@pytest.mark.parametrize(('file_name', 'n_issues', 'java_version'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int, java_version: LanguageVersion):
    inspector = PMDInspector()

    path_to_file = JAVA_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1, 'language_version': java_version})

    assert len(issues) == n_issues
