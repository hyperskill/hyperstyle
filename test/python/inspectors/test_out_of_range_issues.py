from pathlib import Path

from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, CodeIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.reviewers.common import filter_out_of_range_issues

DEFAULT_PATH = Path('test_out_of_range_issues.py')


def create_code_issue_by_line(line_no: int) -> BaseIssue:
    return CodeIssue(
        file_path=DEFAULT_PATH,
        line_no=line_no,
        description='',
        inspector_type=InspectorType.FLAKE8,
        type=IssueType.CODE_STYLE,
        column_no=1,
        origin_class='',
        difficulty=IssueDifficulty.EASY,
    )


def test_out_of_range_issues_when_no_issues() -> None:
    issues = []

    assert filter_out_of_range_issues(issues) == []
    assert filter_out_of_range_issues(issues, start_line=2) == []
    assert filter_out_of_range_issues(issues, end_line=4) == []
    assert filter_out_of_range_issues(issues, start_line=2, end_line=4) == []


def test_out_of_range_issues_when_some_out_of_range_issues() -> None:
    issues = []
    for line_no in range(1, 6):  # 1, 2, 3, 4, 5
        issues.append(create_code_issue_by_line(line_no))

    assert filter_out_of_range_issues(issues) == issues
    assert filter_out_of_range_issues(issues, start_line=2) == issues[1:5]
    assert filter_out_of_range_issues(issues, end_line=4) == issues[:4]
    assert filter_out_of_range_issues(issues, start_line=2, end_line=4) == issues[1:4]
    assert filter_out_of_range_issues(issues, start_line=4, end_line=8) == [issues[3],
                                                                            issues[4]]
    assert filter_out_of_range_issues(issues, start_line=6, end_line=10) == []


def test_out_of_range_issues_when_the_same_borders() -> None:
    first_line_issues = [
        create_code_issue_by_line(1),
        create_code_issue_by_line(1),
        create_code_issue_by_line(1),
    ]

    assert filter_out_of_range_issues(first_line_issues,
                                      start_line=1, end_line=1) == first_line_issues

    assert filter_out_of_range_issues(first_line_issues,
                                      start_line=2, end_line=2) == []
