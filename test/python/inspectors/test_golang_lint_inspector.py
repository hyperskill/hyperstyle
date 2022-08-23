from pathlib import Path
from test.python.inspectors import GO_DATA_FOLDER, GOLANG_LINT_FOLDER
from test.python.inspectors.conftest import use_file_metadata
from typing import List

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.golang_lint.golang_lint import GolangLintInspector
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    CodeIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueDifficulty,
    IssueType,
    MaintainabilityLackIssue,
)
from hyperstyle.src.python.review.inspectors.tips import (
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_maintainability_index_tip,
)
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues


FILE_WITH_ISSUE_NUMBER_TEST_DATA = [
    ('case0_empty.go', 0),
    ('case1_simple_valid_program.go', 0),
    ('case2_program_with_syntax_errors.go', 0),
    ('case3_issues_with_related_information.go', 1),
    ('case4_cyclomatic_complexity.go', 1),
    ('case5_function_length.go', 1),
    ('case6_line_length.go', 1),
    ('case7_maintainability.go', 3),
    ('case8_govet_issues.go', 3),
    ('case9_revive_issues.go', 3),
    ('case10_gocritic_issues.go', 3),
    ('case11_gosimple_issues.go', 3),
    ('case12_stylecheck_issues.go', 2),
    ('case13_staticcheck_issues.go', 3),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_WITH_ISSUE_NUMBER_TEST_DATA)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = GolangLintInspector()

    path_to_file = GO_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})
        issues = list(filter(lambda i: i.type != IssueType.INFO, filter_low_measure_issues(issues, Language.GO)))

        assert len(issues) == n_issues


OUTPUT_PARSING_TEST_DATA = [
    ('non_existent_file.json', []),
    ('empty_file.json', []),
    ('single_file_project_without_issues.json', []),
    (
        'single_file_project_with_issues.json',
        [
            FuncLenIssue(
                origin_class='funlen',
                type=IssueType.FUNC_LEN,
                description=get_func_len_tip().format(6),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
                func_len=6,
            ),
            FuncLenIssue(
                origin_class='funlen',
                type=IssueType.FUNC_LEN,
                description=get_func_len_tip().format(3),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
                func_len=3,
            ),
            CodeIssue(
                origin_class='revive-indent-error-flow',
                type=IssueType.BEST_PRACTICES,
                description="If block ends with a return statement, so drop this else and outdent its block",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=8,
                column_no=9,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CyclomaticComplexityIssue(
                origin_class='cyclop',
                type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip().format(2),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                cc_value=2,
            ),
            CyclomaticComplexityIssue(
                origin_class='cyclop',
                type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip().format(1),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                cc_value=1,
            ),
            CodeIssue(
                origin_class='govet-unreachable',
                type=IssueType.ERROR_PRONE,
                description="Unreachable code",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=11,
                column_no=2,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
            ),
            MaintainabilityLackIssue(
                origin_class='maintidx',
                type=IssueType.MAINTAINABILITY,
                description=get_maintainability_index_tip().format(34),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                maintainability_lack=34,
            ),
            MaintainabilityLackIssue(
                origin_class='maintidx',
                type=IssueType.MAINTAINABILITY,
                description=get_maintainability_index_tip().format(28),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                maintainability_lack=28,
            ),
            CodeIssue(
                origin_class='stylecheck-ST1017',
                type=IssueType.CODE_STYLE,
                description="Don't use Yoda conditions",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=6,
                column_no=5,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
            ),
        ],
    ),
    (
        'multi_file_project_without_issues.json',
        [],
    ),
    (
        'multi_file_project_with_issues.json',
        [
            CodeIssue(
                origin_class='deadcode',
                type=IssueType.ERROR_PRONE,
                description="`hypotenuse` is unused",
                file_path=Path('/home/user/some_project/b.go'),
                line_no=7,
                column_no=6,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
            ),
            FuncLenIssue(
                origin_class='funlen',
                type=IssueType.FUNC_LEN,
                description=get_func_len_tip().format(6),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
                func_len=6,
            ),
            FuncLenIssue(
                origin_class='funlen',
                type=IssueType.FUNC_LEN,
                description=get_func_len_tip().format(3),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
                func_len=3,
            ),
            CodeIssue(
                origin_class='revive-indent-error-flow',
                type=IssueType.BEST_PRACTICES,
                description="If block ends with a return statement, so drop this else and outdent its block",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=8,
                column_no=9,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.MEDIUM,
            ),
            CyclomaticComplexityIssue(
                origin_class='cyclop',
                type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip().format(2),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                cc_value=2,
            ),
            CyclomaticComplexityIssue(
                origin_class='cyclop',
                type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip().format(1),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                cc_value=1,
            ),
            CyclomaticComplexityIssue(
                origin_class='cyclop',
                type=IssueType.CYCLOMATIC_COMPLEXITY,
                description=get_cyclomatic_complexity_tip().format(1),
                file_path=Path('/home/user/some_project/b.go'),
                line_no=7,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                cc_value=1,
            ),
            CodeIssue(
                origin_class='govet-unreachable',
                type=IssueType.ERROR_PRONE,
                description="Unreachable code",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=11,
                column_no=2,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
            ),
            MaintainabilityLackIssue(
                origin_class='maintidx',
                type=IssueType.MAINTAINABILITY,
                description=get_maintainability_index_tip().format(34),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=5,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                maintainability_lack=34,
            ),
            MaintainabilityLackIssue(
                origin_class='maintidx',
                type=IssueType.MAINTAINABILITY,
                description=get_maintainability_index_tip().format(28),
                file_path=Path('/home/user/some_project/a.go'),
                line_no=14,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                maintainability_lack=28,
            ),
            MaintainabilityLackIssue(
                origin_class='maintidx',
                type=IssueType.MAINTAINABILITY,
                description=get_maintainability_index_tip().format(25),
                file_path=Path('/home/user/some_project/b.go'),
                line_no=7,
                column_no=1,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.HARD,
                maintainability_lack=25,
            ),
            CodeIssue(
                origin_class='stylecheck-ST1017',
                type=IssueType.CODE_STYLE,
                description="Don't use Yoda conditions",
                file_path=Path('/home/user/some_project/a.go'),
                line_no=6,
                column_no=5,
                inspector_type=InspectorType.GOLANG_LINT,
                difficulty=IssueDifficulty.EASY,
            ),
        ],
    ),
]


@pytest.mark.parametrize(('file_name', 'expected_issues'), OUTPUT_PARSING_TEST_DATA)
def test_output_parsing(file_name: str, expected_issues: List[CodeIssue]):
    path_to_file = GOLANG_LINT_FOLDER / file_name
    assert GolangLintInspector.parse(path_to_file) == expected_issues


def test_choose_issue_type():
    error_codes = [
        'deadcode',
        'cyclop',
        'gomnd',
        'whitespace',
        'goconst',
        'gosimple-S1000',
    ]

    expected_issue_types = [
        IssueType.ERROR_PRONE,
        IssueType.CYCLOMATIC_COMPLEXITY,
        IssueType.INFO,
        IssueType.CODE_STYLE,
        IssueType.COMPLEXITY,
        IssueType.BEST_PRACTICES,
    ]

    issue_types = list(map(GolangLintInspector.choose_issue_type, error_codes))
    assert issue_types == expected_issue_types
