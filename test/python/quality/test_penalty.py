from pathlib import Path

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.quality.penalty import categorize, PreviousIssue, Punisher

current_issues = [
    BaseIssue(
        file_path=Path("."),
        line_no=1,
        column_no=1,
        description="Possibly misspelt word",
        origin_class="SC200",
        inspector_type=InspectorType.FLAKE8,
        type=IssueType.BEST_PRACTICES,
    ),
    BaseIssue(
        file_path=Path("."),
        line_no=10,
        column_no=5,
        description="Lambda may not be necessary",
        origin_class="W0108",
        inspector_type=InspectorType.FLAKE8,
        type=IssueType.CODE_STYLE,
    ),
]

punisher = Punisher([], [])


def test_get_penalizing_classes_empty_previous_issues_empty_current_issues():
    actual = punisher._get_penalizing_classes([], [])

    assert actual == set()


def test_get_penalizing_classes_empty_current_issues():
    actual = punisher._get_penalizing_classes(current_issues, [])

    assert actual == set()


def test_get_penalizing_classes_empty_previous_issues():
    previous_issues = [PreviousIssue("WPS301", 50), PreviousIssue("SC200", 10)]

    actual = punisher._get_penalizing_classes([], previous_issues)
    assert actual == set()


def test_get_penalizing_classes_empty_intersection():
    previous_issues = [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)]

    actual = punisher._get_penalizing_classes(current_issues, previous_issues)
    assert actual == set()


def test_get_penalizing_classes_non_empty_intersection_1():
    previous_issues = [PreviousIssue("SC200", 50), PreviousIssue("WPS412", 10)]

    actual = punisher._get_penalizing_classes(current_issues, previous_issues)
    assert actual == {"SC200"}


def test_get_penalizing_classes_non_empty_intersection_2():
    previous_issues = [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)]

    actual = punisher._get_penalizing_classes(current_issues, previous_issues)
    assert actual == {"SC200", "W0108"}


def test_get_penalizing_classes_categorize_different_issues():
    previous_issues = [PreviousIssue("WPS412", 50), PreviousIssue("WPS412", 10)]

    categorize(previous_issues, current_issues)

    for issue in previous_issues:
        assert issue.category is None


def test_get_penalizing_classes_same_issues_1():
    previous_issues = [PreviousIssue("SC200", 50), PreviousIssue("WPS312", 10)]

    categorize(previous_issues, current_issues)

    assert previous_issues[0].category == IssueType.BEST_PRACTICES
    assert previous_issues[1].category is None


def test_get_penalizing_classes_same_issues_2():
    previous_issues = [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)]

    categorize(previous_issues, current_issues)

    assert previous_issues[0].category == IssueType.BEST_PRACTICES
    assert previous_issues[1].category == IssueType.CODE_STYLE


def test_get_issue_influence_on_penalty_repeated_issue():
    punisher._issue_class_to_influence = {"SC200": 0.636, "WPS312": 0.1225}

    actual = punisher.get_issue_influence_on_penalty("SC200")

    assert actual == 63


def test_get_issue_influence_on_penalty_not_repeater_issue():
    punisher._issue_class_to_influence = {"SC200": 0.636, "WPS312": 0.1225}

    actual = punisher.get_issue_influence_on_penalty("Q146")

    assert actual == 0


def test_get_normalized_penalty_coefficient_empty_current_issues():
    punisher._penalty_coefficient = 8

    actual = punisher._get_normalized_penalty_coefficient([])

    assert actual == 0


def test_get_normalized_penalty_coefficient_non_empty_current_issues():
    punisher._penalty_coefficient = 8

    actual = punisher._get_normalized_penalty_coefficient(current_issues)

    assert actual == 0.8
