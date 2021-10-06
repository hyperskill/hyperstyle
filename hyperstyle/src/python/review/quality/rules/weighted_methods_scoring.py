from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class WeightedMethodsRuleConfig:
    weighted_methods_bad: int
    weighted_methods_moderate: int
    weighted_methods_good: int


common_weighted_methods_rule_config = WeightedMethodsRuleConfig(
    weighted_methods_bad=105,
    weighted_methods_moderate=85,
    weighted_methods_good=70,
)

LANGUAGE_TO_WEIGHTED_METHODS_RULE_CONFIG = {
    Language.JAVA: common_weighted_methods_rule_config,
    Language.PYTHON: common_weighted_methods_rule_config,
    Language.KOTLIN: common_weighted_methods_rule_config,
    Language.JS: common_weighted_methods_rule_config,
}


class WeightedMethodsRule(Rule):
    def __init__(self, config: WeightedMethodsRuleConfig):
        self.config = config
        self.rule_type = IssueType.WEIGHTED_METHOD
        self.weighted_methods: Optional[int] = None

    def apply(self, weighted_methods):
        self.weighted_methods = weighted_methods
        if weighted_methods > self.config.weighted_methods_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = weighted_methods - self.config.weighted_methods_bad
        elif weighted_methods > self.config.weighted_methods_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = weighted_methods - self.config.weighted_methods_moderate
        elif weighted_methods > self.config.weighted_methods_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = weighted_methods - self.config.weighted_methods_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = weighted_methods
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'WeightedMethodsRule') -> 'WeightedMethodsRule':
        config = WeightedMethodsRuleConfig(
            min(self.config.weighted_methods_bad, other.config.weighted_methods_bad),
            min(self.config.weighted_methods_moderate, other.config.weighted_methods_moderate),
            min(self.config.weighted_methods_good, other.config.weighted_methods_good),
        )
        result_rule = WeightedMethodsRule(config)
        result_rule.apply(max(self.weighted_methods, other.weighted_methods))

        return result_rule
