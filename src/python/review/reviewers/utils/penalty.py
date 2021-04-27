import dataclasses
import json
from typing import Dict, List, Optional, Set

from src.python.review.common.language import Language
from src.python.review.inspectors.issue import BaseIssue, IssueType

ISSUE_TYPE_TO_PENALTY_COEFFICIENT = {
    IssueType.COHESION: 1,
    IssueType.COUPLING: 1,
    IssueType.FUNC_LEN: 1,
    IssueType.LINE_LEN: 1,
    IssueType.ARCHITECTURE: 1,
    IssueType.BEST_PRACTICES: 1,
    IssueType.BOOL_EXPR_LEN: 1,
    IssueType.CHILDREN_NUMBER: 1,
    IssueType.CLASS_RESPONSE: 1,
    IssueType.CODE_STYLE: 1,
    IssueType.COMPLEXITY: 1,
    IssueType.CYCLOMATIC_COMPLEXITY: 1,
    IssueType.ERROR_PRONE: 1,
    IssueType.INHERITANCE_DEPTH: 1,
    IssueType.MAINTAINABILITY: 1,
    IssueType.METHOD_NUMBER: 1,
    IssueType.WEIGHTED_METHOD: 1,
}


@dataclasses.dataclass
class PenaltyConfig:
    one_level_penalty: int
    two_level_penalty: int
    three_level_penalty: int


common_penalty_rule = PenaltyConfig(
    one_level_penalty=10,
    two_level_penalty=20,
    three_level_penalty=30,
)


@dataclasses.dataclass
class PreviousIssue:
    origin_class: str
    quantity: int
    category: IssueType = None


def get_previous_issues_by_language(lang_to_history: Optional[str], language: Language) -> List[PreviousIssue]:
    """
    Reads a json string and returns a list of previously made issues for the specified language.
    """
    if lang_to_history is None:
        return []

    language_to_history = json.loads(lang_to_history)
    history = language_to_history[language.value.lower()]

    previous_issues = []
    for issue_data in history:
        previous_issues.append(PreviousIssue(**issue_data))
    return previous_issues


def categorize(previous_issues: List[PreviousIssue], current_issues: List[BaseIssue]):
    """
    For each previously made issue determines its category, with the help of current issues.
    """
    origin_class_to_category = {}
    for issue in current_issues:
        origin_class_to_category[issue.origin_class] = issue.type

    for issue in previous_issues:
        issue.category = origin_class_to_category.get(issue.origin_class, None)


def get_issue_class_to_penalty(issues: List[PreviousIssue]) -> Dict[str, int]:
    """
    For each issue, the corresponding penalty coefficient is calculated.
    """
    return {
        issue.origin_class: ISSUE_TYPE_TO_PENALTY_COEFFICIENT.get(issue.category, 1) * issue.quantity
        for issue in issues
    }


def get_penalizing_classes(current_issues: List[BaseIssue], previous_issues: List[PreviousIssue]) -> Set[str]:
    """
    Returns issues that should be penalized.
    """
    current_classes = set(map(lambda issue: issue.origin_class, current_issues))
    previous_classes = set(map(lambda issue: issue.origin_class, previous_issues))

    return previous_classes.intersection(current_classes)


def get_penalty_coefficient(current_issues: List[BaseIssue], previous_issues: List[PreviousIssue]) -> int:
    """
    Calculates the final penalty coefficient.
    """

    penalizing_classes = get_penalizing_classes(current_issues, previous_issues)
    penalizing_issues = list(filter(lambda issue: issue.origin_class in penalizing_classes, previous_issues))

    penalty_coefficient = 0
    for issue in penalizing_issues:
        penalty_coefficient += issue.quantity * ISSUE_TYPE_TO_PENALTY_COEFFICIENT[issue.category]

    return penalty_coefficient


def get_penalty_influence(issue_penalty_coefficient: int, total_penalty_coefficient: int) -> int:
    """
    Calculates the influence of the issue on the penalty.

    Returns a number in the range from 0 to 100.
    """

    return int(issue_penalty_coefficient / total_penalty_coefficient * 100)


def get_penalty(penalty_coefficient: int) -> int:
    """
    Calculates the penalty with the penalty coefficient

    Returns a number equal to 0, 1, 2 or 3, which describes how many levels the grade should be lowered.
    """

    if penalty_coefficient < common_penalty_rule.one_level_penalty:
        return 0
    elif penalty_coefficient < common_penalty_rule.two_level_penalty:
        return 1
    elif penalty_coefficient < common_penalty_rule.three_level_penalty:
        return 2
    else:
        return 3
