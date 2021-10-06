from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class ComplexityRuleConfig:
    complexity_good: int
    complexity_moderate: int
    complexity_bad: int


common_complexity_rule_config = ComplexityRuleConfig(
    complexity_good=1,
    complexity_moderate=3,
    complexity_bad=6,
)

LANGUAGE_TO_COMPLEXITY_RULE_CONFIG = {
    Language.JAVA: common_complexity_rule_config,
    Language.PYTHON: common_complexity_rule_config,
    Language.KOTLIN: common_complexity_rule_config,
    Language.JS: common_complexity_rule_config,
}


class ComplexityRule(Rule):
    def __init__(self, config: ComplexityRuleConfig):
        self.config = config
        self.rule_type = IssueType.COMPLEXITY
        self.complexity: Optional[int] = None

    def apply(self, complexity):
        self.complexity = complexity
        if complexity > self.config.complexity_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = complexity - self.config.complexity_bad
        elif complexity > self.config.complexity_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = complexity - self.config.complexity_moderate
        elif complexity > self.config.complexity_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = complexity - self.config.complexity_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        elif self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'ComplexityRule') -> 'ComplexityRule':
        config = ComplexityRuleConfig(
            min(self.config.complexity_bad, other.config.complexity_bad),
            min(self.config.complexity_moderate, other.config.complexity_moderate),
            min(self.config.complexity_good, other.config.complexity_good),
        )
        result_rule = ComplexityRule(config)
        result_rule.apply(max(self.complexity, other.complexity))

        return result_rule
