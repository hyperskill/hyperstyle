import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueType
from hyperstyle.src.python.review.quality.model import QualityType


@dataclass(frozen=True, eq=True)
class PenaltyIssue(BaseIssue):
    influence_on_penalty: int


# TODO: need testing
ISSUE_TYPE_TO_PENALTY_COEFFICIENT = {
    IssueType.COHESION: 0.6,
    IssueType.COUPLING: 0.6,
    IssueType.FUNC_LEN: 0.6,
    IssueType.LINE_LEN: 1,
    IssueType.ARCHITECTURE: 1,  # TODO: Change the coefficient when the tool can find this type of issues
    IssueType.BEST_PRACTICES: 0.9,
    IssueType.BOOL_EXPR_LEN: 0.6,
    IssueType.CHILDREN_NUMBER: 0.2,
    IssueType.CLASS_RESPONSE: 0.2,
    IssueType.CODE_STYLE: 1,
    IssueType.COMPLEXITY: 0.5,
    IssueType.CYCLOMATIC_COMPLEXITY: 0.7,
    IssueType.ERROR_PRONE: 0.6,
    IssueType.INHERITANCE_DEPTH: 0.2,
    IssueType.MAINTAINABILITY: 0.3,
    IssueType.METHOD_NUMBER: 0.2,
    IssueType.WEIGHTED_METHOD: 0.2,
    IssueType.UNDEFINED: 0,
    IssueType.INFO: 0,
}


@dataclass
class PenaltyConfig:
    one_level_quality_reduction: float
    two_level_quality_reduction: float
    three_level_quality_reduction: float


# TODO: need testing
common_penalty_rule = PenaltyConfig(
    one_level_quality_reduction=0.5,
    two_level_quality_reduction=0.7,
    three_level_quality_reduction=0.9,
)


@dataclass
class PreviousIssue:
    origin_class: str
    number: int
    category: IssueType = None


def get_previous_issues_by_language(lang_to_history: Optional[str], language: Language) -> List[PreviousIssue]:
    """
    Reads a json string and returns a list of previously made issues for the specified language.
    """
    if lang_to_history is None:
        return []

    language_to_history = json.loads(lang_to_history)
    history = language_to_history.get(language.value.lower(), [])

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


class Punisher:
    """
    Punisher with the list of previous issues and current issues allows you to use the 'get_quality_with_penalty'
    function to get quality including the penalty for previous issues and use the 'get_issue_influence_on_penalty'
    function to get the influence of an issues on reducing the quality score.
    """

    _penalty_coefficient: float
    _normalized_penalty_coefficient: float
    _issue_class_to_influence: Dict[str, float]

    def __init__(self, current_issues: List[BaseIssue], previous_issues: List[PreviousIssue]):
        self._penalty_coefficient = self._get_penalty_coefficient(current_issues, previous_issues)
        self._normalized_penalty_coefficient = self._get_normalized_penalty_coefficient(current_issues)
        self._issue_class_to_influence = self._get_issue_class_to_influence(current_issues, previous_issues)

    def get_quality_with_penalty(self, quality_without_penalty: QualityType) -> QualityType:
        """
        Depending on the penalty coefficient, reduces the quality type.
        """
        numbered_quality_type = quality_without_penalty.to_number()
        numbered_quality_type -= self._get_penalty_score()

        quality = QualityType.EXCELLENT

        if numbered_quality_type <= 0:
            quality = QualityType.BAD
        elif numbered_quality_type == 1:
            quality = QualityType.MODERATE
        elif numbered_quality_type == 2:
            quality = QualityType.GOOD

        return quality

    def get_issue_influence_on_penalty(self, issue_class: str) -> int:
        """
        Calculates the influence of the issue on the penalty.

        Returns a number in the range from 0 to 100.
        """

        return int(self._issue_class_to_influence.get(issue_class, 0) * 100)

    def _get_penalty_score(self) -> int:
        """
        Calculates the penalty score with the penalty coefficient

        Returns a number equal to 0, 1, 2 or 3, which describes how many levels the grade should be lowered.
        """

        penalty_score = 3

        if self._normalized_penalty_coefficient < common_penalty_rule.one_level_quality_reduction:
            penalty_score = 0
        elif self._normalized_penalty_coefficient < common_penalty_rule.two_level_quality_reduction:
            penalty_score = 1
        elif self._normalized_penalty_coefficient < common_penalty_rule.three_level_quality_reduction:
            penalty_score = 2

        return penalty_score

    def _get_penalty_coefficient(self, current_issues: List[BaseIssue], previous_issues: List[PreviousIssue]) -> float:
        """
        To calculate the penalty coefficient we use those issues that occurred earlier and repeated again.
        Such issues will be called penalizing issues. For each penalizing issue, we calculate a number equal to
        the number of times this issue was repeated earlier multiplied by the coefficient of the category to
        which the issue belongs. These numbers are added up to get the penalty coefficient.
        """

        penalizing_classes = self._get_penalizing_classes(current_issues, previous_issues)
        penalizing_issues = list(filter(lambda issue: issue.origin_class in penalizing_classes, previous_issues))

        coefficient = 0
        for issue in penalizing_issues:
            coefficient += ISSUE_TYPE_TO_PENALTY_COEFFICIENT.get(issue.category, 1) * issue.number

        return coefficient

    def _get_normalized_penalty_coefficient(self, current_issues: List[BaseIssue]) -> float:
        """
        The penalty coefficient is normalized by the formula: k / (k + n),
        where k is the penalty coefficient, n is the number of current issues.
        """

        coefficient = 0
        if current_issues:
            coefficient = self._penalty_coefficient / (self._penalty_coefficient + len(current_issues))

        return coefficient

    def _get_issue_class_to_influence(self,
                                      current_issues: List[BaseIssue],
                                      previous_issues: List[PreviousIssue]) -> Dict[str, float]:
        """
        For each issue to be penalized, the corresponding influence on penalty is calculated.

        To do this, for each issue we count its penalty coefficient, normalize it,
        and divide the resulting number by the total normalized penalty coefficient.
        """

        penalizing_classes = self._get_penalizing_classes(current_issues, previous_issues)
        penalizing_issues = list(filter(lambda issue: issue.origin_class in penalizing_classes, previous_issues))

        result = {}
        for issue in penalizing_issues:
            issue_coefficient = ISSUE_TYPE_TO_PENALTY_COEFFICIENT.get(issue.category, 1) * issue.number
            normalized_issue_coefficient = issue_coefficient / (self._penalty_coefficient + len(current_issues))
            influence = normalized_issue_coefficient / self._normalized_penalty_coefficient

            result[issue.origin_class] = influence

        return result

    @staticmethod
    def _get_penalizing_classes(current_issues: List[BaseIssue], previous_issues: List[PreviousIssue]) -> Set[str]:
        """
        Returns issues that should be penalized.
        We penalize for those issues that were there before, but repeated again.
        """
        current_classes = set(map(lambda issue: issue.origin_class, current_issues))
        previous_classes = set(map(lambda issue: issue.origin_class, previous_issues))

        return previous_classes.intersection(current_classes)
