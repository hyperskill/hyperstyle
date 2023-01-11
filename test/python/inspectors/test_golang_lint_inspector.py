from pathlib import Path
from test.python.inspectors import GO_DATA_FOLDER, GOLANG_LINT_FOLDER
from test.python.inspectors.conftest import gather_issues_test_info, IssuesTestInfo, use_file_metadata
from typing import List

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.tips import (
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
    get_magic_number_tip,
    get_maintainability_index_tip,
)
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
    ('case14_whitespace.go', 0),
    ('case15_deadcode.go', 4),
    ('case16_errcheck.go', 11),
    ('case17_magic_numbers.go', 0),  # 0 because all INFO issues have been filtered out
    ('case18_generics.go', 1),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_WITH_ISSUE_NUMBER_TEST_DATA)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = GolangLintInspector()

    path_to_file = GO_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})
        issues = list(filter(lambda i: i.type != IssueType.INFO, filter_low_measure_issues(issues, Language.GO)))

        assert len(issues) == n_issues


FILE_WITH_ISSUE_INFO_TEST_DATA = [
    ('case0_empty.go', IssuesTestInfo()),
    ('case1_simple_valid_program.go', IssuesTestInfo(n_cc=1, n_maintainability=1)),
    ('case2_program_with_syntax_errors.go', IssuesTestInfo()),
    (
        'case3_issues_with_related_information.go',
        IssuesTestInfo(n_cc=2, n_maintainability=2, n_error_prone=1, n_func_len=1),
    ),
    ('case4_cyclomatic_complexity.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=1, n_info=3)),
    ('case5_function_length.go', IssuesTestInfo(n_func_len=1, n_cc=2, n_maintainability=2, n_info=96)),
    ('case6_line_length.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_line_len=1)),
    ('case7_maintainability.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=1)),
    ('case8_govet_issues.go', IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_error_prone=3)),
    (
        'case9_revive_issues.go',
        IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_code_style=1, n_best_practices=1, n_error_prone=1),
    ),
    ('case10_gocritic_issues.go', IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_best_practices=3)),
    (
        'case11_gosimple_issues.go',
        IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_code_style=1, n_best_practices=2),
    ),
    (
        'case12_stylecheck_issues.go',
        IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_code_style=2),
    ),
    ('case13_staticcheck_issues.go', IssuesTestInfo(n_cc=1, n_maintainability=1, n_func_len=1, n_error_prone=3)),
    ('case14_whitespace.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=2, n_code_style=0)),
    (
        'case15_deadcode.go',
        IssuesTestInfo(n_cc=3, n_maintainability=3, n_func_len=1, n_error_prone=3, n_best_practices=1),
    ),
    ('case16_errcheck.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=1, n_error_prone=11)),
    ('case17_magic_numbers.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=1, n_info=2)),
    ('case18_generics.go', IssuesTestInfo(n_cc=2, n_maintainability=2, n_func_len=2, n_code_style=1, n_info=4)),
]


@pytest.mark.parametrize(('file_name', 'expected_issues_info'), FILE_WITH_ISSUE_INFO_TEST_DATA)
def test_file_with_issues_info(file_name: str, expected_issues_info: IssuesTestInfo):
    inspector = GolangLintInspector()

    path_to_file = GO_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})

    issues_info = gather_issues_test_info(issues)
    assert issues_info == expected_issues_info


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
                origin_class='unused',
                type=IssueType.ERROR_PRONE,
                description="func `hypotenuse` is unused",
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
        'unused',
        'cyclop',
        'lll',
        'funlen',
        'maintidx',
        'gomnd',
        'whitespace',
        'goconst',
        'gosimple-S1000',
    ]

    expected_issue_types = [
        IssueType.ERROR_PRONE,
        IssueType.CYCLOMATIC_COMPLEXITY,
        IssueType.LINE_LEN,
        IssueType.FUNC_LEN,
        IssueType.MAINTAINABILITY,
        IssueType.INFO,
        IssueType.CODE_STYLE,
        IssueType.COMPLEXITY,
        IssueType.BEST_PRACTICES,
    ]

    issue_types = list(map(GolangLintInspector.choose_issue_type, error_codes))
    assert issue_types == expected_issue_types


MEASURE_TEST_DATA = [
    ('cyclop', 13),
    ('funlen', 13),
    ('lll', 121),
    ('maintidx', 79),
]


@pytest.mark.parametrize(('origin_class', 'expected_measure'), MEASURE_TEST_DATA)
def test_measure_parse(origin_class: str, expected_measure: int):
    inspector = GolangLintInspector()

    path_to_file = GOLANG_LINT_FOLDER / 'issues' / f'{origin_class.lower()}.go'
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.measure() == expected_measure


NEW_DESCRIPTION_TEST_DATA = [
    ('cyclop', get_cyclomatic_complexity_tip().format(13)),
    ('funlen', get_func_len_tip().format(13)),
    ('lll', get_line_len_tip().format(121)),
    ('maintidx', get_maintainability_index_tip()),
    ('gomnd', get_magic_number_tip().format(42)),
]


@pytest.mark.parametrize(('origin_class', 'expected_description'), NEW_DESCRIPTION_TEST_DATA)
def test_new_issue_description(origin_class: str, expected_description: str):
    inspector = GolangLintInspector()

    path_to_file = GOLANG_LINT_FOLDER / 'issues' / f'{origin_class.lower()}.go'
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {'n_cpu': 1})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.description == expected_description
