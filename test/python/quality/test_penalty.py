from pathlib import Path
from typing import List, Set

import pytest

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.quality.penalty import categorize, PreviousIssue, Punisher

punisher = Punisher([], [])

CURRENT_ISSUES = [
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

PREVIOUS_ISSUES_CURRENT_ISSUES_EXPECTED_CLASSES = [
    ([], [], set()),
    ([], CURRENT_ISSUES, set()),
    ([PreviousIssue("WPS301", 50), PreviousIssue("SC200", 10)], [], set()),
    ([PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], CURRENT_ISSUES, set()),
    ([PreviousIssue("SC200", 50), PreviousIssue("WPS412", 10)], CURRENT_ISSUES, {"SC200"}),
    ([PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], CURRENT_ISSUES, {"SC200", "W0108"}),
]


@pytest.mark.parametrize(('previous_issues', 'current_issues', 'expected_penalizing_classes'),
                         PREVIOUS_ISSUES_CURRENT_ISSUES_EXPECTED_CLASSES)
def test_get_penalizing_classes(previous_issues: List[PreviousIssue],
                                current_issues: List[BaseIssue],
                                expected_penalizing_classes: Set[str]):
    actual = punisher._get_penalizing_classes(current_issues, previous_issues)

    assert actual == expected_penalizing_classes


PREVIOUS_ISSUES_CURRENT_ISSUES_EXPECTED_CATEGORIES = [
    ([], [], []),
    ([], CURRENT_ISSUES, []),
    ([PreviousIssue("WPS412", 50), PreviousIssue("WPS412", 10)], [], [None, None]),
    ([PreviousIssue("WPS412", 50), PreviousIssue("WPS412", 10)], CURRENT_ISSUES, [None, None]),
    ([PreviousIssue("SC200", 50), PreviousIssue("WPS312", 10)], CURRENT_ISSUES, [IssueType.BEST_PRACTICES, None]),
    ([PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], CURRENT_ISSUES,
     [IssueType.BEST_PRACTICES, IssueType.CODE_STYLE]),
]


@pytest.mark.parametrize(('previous_issues', 'current_issues', 'expected_categories'),
                         PREVIOUS_ISSUES_CURRENT_ISSUES_EXPECTED_CATEGORIES)
def test_categorize(previous_issues: List[PreviousIssue],
                    current_issues: List[BaseIssue],
                    expected_categories: List[IssueType]):
    categorize(previous_issues, current_issues)

    for issue, expected_category in zip(previous_issues, expected_categories):
        assert issue.category == expected_category


ISSUE_CLASS_EXPECTED_INFLUENCE = [
    ("SC200", 63),
    ("Q146", 0)
]


@pytest.mark.parametrize(('issue_class', 'expected_influence'), ISSUE_CLASS_EXPECTED_INFLUENCE)
def test_get_issue_influence_on_penalty(issue_class: str, expected_influence: int):
    punisher._issue_class_to_influence = {"SC200": 0.636, "WPS312": 0.1225}

    actual = punisher.get_issue_influence_on_penalty(issue_class)

    assert actual == expected_influence


PENALTY_COEFFICIENT_CURRENT_ISSUES_NORMALIZED_PENALTY_COEFFICIENT = [
    (8, [], 0),
    (8, CURRENT_ISSUES, 0.8)
]


@pytest.mark.parametrize(('penalty_coefficient', 'current_issues', 'normalized_penalty_coefficient'),
                         PENALTY_COEFFICIENT_CURRENT_ISSUES_NORMALIZED_PENALTY_COEFFICIENT)
def test_get_normalized_penalty_coefficient(penalty_coefficient: float,
                                            current_issues: List[BaseIssue],
                                            normalized_penalty_coefficient):
    punisher._penalty_coefficient = 8

    actual = punisher._get_normalized_penalty_coefficient(current_issues)

    assert actual == normalized_penalty_coefficient
