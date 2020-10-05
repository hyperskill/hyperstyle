from pathlib import Path

from review.inspectors.inspector_type import InspectorType
from review.inspectors.issue import CodeIssue, IssueType
from review.reviewers.utils.issues_filter import filter_duplicate_issues


def test_filter_duplicate_issues_when_single_inspector() -> None:
    issues = [
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.FLAKE8,
                  type=IssueType.CODE_STYLE,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  inspector_type=InspectorType.FLAKE8,
                  type=IssueType.CODE_STYLE,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  inspector_type=InspectorType.FLAKE8,
                  type=IssueType.CODE_STYLE,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  type=IssueType.CODE_STYLE,
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class=''),
    ]

    filtered_issues = filter_duplicate_issues(issues)

    assert set(filtered_issues) == set(issues)


def test_filter_duplicate_issues_when_several_inspectors() -> None:
    issues = [
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.PYLINT,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.INTELLIJ,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  type=IssueType.CODE_STYLE,
                  inspector_type=InspectorType.PYLINT,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  type=IssueType.BEST_PRACTICES,
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=11,
                  description='',
                  type=IssueType.ERROR_PRONE,
                  inspector_type=InspectorType.INTELLIJ,
                  column_no=1,
                  origin_class=''),
    ]

    filtered_issues = filter_duplicate_issues(issues)

    assert set(filtered_issues) == {issues[0],
                                    issues[3],
                                    issues[4],
                                    issues[5]}


def test_filter_duplicate_issues_when_several_issues_in_line_no() -> None:
    issues = [
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  type=IssueType.CODE_STYLE,
                  inspector_type=InspectorType.PYLINT,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  type=IssueType.CODE_STYLE,
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  type=IssueType.CODE_STYLE,
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class=''),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.FLAKE8,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.INTELLIJ,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
        CodeIssue(file_path=Path('code.py'),
                  line_no=10,
                  description='',
                  inspector_type=InspectorType.INTELLIJ,
                  column_no=1,
                  origin_class='',
                  type=IssueType.COMPLEXITY),
    ]

    filtered_issues = filter_duplicate_issues(issues)

    assert set(filtered_issues) == {issues[1],
                                    issues[2],
                                    issues[4],
                                    issues[5]}
