from pathlib import Path
from typing import List, Set

import pytest
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.quality.penalty import categorize, PreviousIssue, Punisher

punisher = Punisher([], [])

CURRENT_ISSUES = [
    BaseIssue(
        file_path=Path(""),
        line_no=1,
        column_no=1,
        description="Possibly misspelt word",
        origin_class="SC200",
        inspector_type=InspectorType.FLAKE8,
        type=IssueType.BEST_PRACTICES,
        difficulty=IssueDifficulty.MEDIUM,
    ),
    BaseIssue(
        file_path=Path(""),
        line_no=10,
        column_no=5,
        description="Lambda may not be necessary",
        origin_class="W0108",
        inspector_type=InspectorType.FLAKE8,
        type=IssueType.CODE_STYLE,
        difficulty=IssueDifficulty.EASY,
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
    ([PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], [], [None, None]),
    ([PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], CURRENT_ISSUES, [None, None]),
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
    ("Q146", 0),
]


@pytest.mark.parametrize(('issue_class', 'expected_influence'), ISSUE_CLASS_EXPECTED_INFLUENCE)
def test_get_issue_influence_on_penalty(issue_class: str, expected_influence: int):
    punisher._issue_class_to_influence = {"SC200": 0.636, "WPS312": 0.1225}

    actual = punisher.get_issue_influence_on_penalty(issue_class)

    assert actual == expected_influence


PENALTY_COEFFICIENT_CURRENT_ISSUES_NORMALIZED_PENALTY_COEFFICIENT = [
    (8, [], 0),
    (8, CURRENT_ISSUES, 0.8),
]


@pytest.mark.parametrize(('penalty_coefficient', 'current_issues', 'normalized_penalty_coefficient'),
                         PENALTY_COEFFICIENT_CURRENT_ISSUES_NORMALIZED_PENALTY_COEFFICIENT)
def test_get_normalized_penalty_coefficient(penalty_coefficient: float,
                                            current_issues: List[BaseIssue],
                                            normalized_penalty_coefficient):
    punisher._penalty_coefficient = penalty_coefficient

    actual = punisher._get_normalized_penalty_coefficient(current_issues)

    assert actual == normalized_penalty_coefficient


CURRENT_ISSUES_PREVIOUS_ISSUES_EXPECTED_COEFFICIENT = [
    ([], [], 0),
    (CURRENT_ISSUES, [], 0),
    ([], [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 0),
    (CURRENT_ISSUES, [PreviousIssue("WPS301", 50), PreviousIssue("WPS123", 10)], 0),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("WPS123", 10)], 45),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], 45 + 10),
]


@pytest.mark.parametrize(('current_issues', 'previous_issues', 'expected_coefficient'),
                         CURRENT_ISSUES_PREVIOUS_ISSUES_EXPECTED_COEFFICIENT)
def test_get_penalty_coefficient(current_issues: List[BaseIssue],
                                 previous_issues: List[PreviousIssue],
                                 expected_coefficient: float):
    categorize(previous_issues, current_issues)
    actual = punisher._get_penalty_coefficient(current_issues, previous_issues)

    assert actual == expected_coefficient


CURRENT_ISSUES_PREVIOUS_ISSUES_ISSUE_CLASS_EXPECTED_INFLUENCE = [
    ([], [], 'WPS312', 0),
    (CURRENT_ISSUES, [], 'WPS312', 0),
    (CURRENT_ISSUES, [], 'SC200', 0),
    ([], [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 'WPS312', 0),
    ([], [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 'WPS301', 0),
    (CURRENT_ISSUES, [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 'WPS312', 0),
    (CURRENT_ISSUES, [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 'WPS301', 0),
    (CURRENT_ISSUES, [PreviousIssue("WPS301", 50), PreviousIssue("WPS412", 10)], 'SC200', 0),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("WPS412", 10)], 'WPS301', 0),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("WPS412", 10)], 'SC200', 100),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("WPS412", 10)], 'WPS412', 0),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], 'WPS301', 0),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], 'SC200', 81),
    (CURRENT_ISSUES, [PreviousIssue("SC200", 50), PreviousIssue("W0108", 10)], 'W0108', 18),
]


@pytest.mark.parametrize(('current_issues', 'previous_issues', 'issue_class', 'expected_influence'),
                         CURRENT_ISSUES_PREVIOUS_ISSUES_ISSUE_CLASS_EXPECTED_INFLUENCE)
def test_get_issue_class_to_influence(current_issues: List[BaseIssue],
                                      previous_issues: List[PreviousIssue],
                                      issue_class: str,
                                      expected_influence: int):
    categorize(previous_issues, current_issues)
    punisher = Punisher(current_issues, previous_issues)
    actual = punisher.get_issue_influence_on_penalty(issue_class)

    assert actual == expected_influence
