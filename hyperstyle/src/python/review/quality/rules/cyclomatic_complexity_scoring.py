from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class CyclomaticComplexityRuleConfig:
    cc_value_bad: int
    cc_value_moderate: int


LANGUAGE_TO_CYCLOMATIC_COMPLEXITY_RULE_CONFIG = {
    Language.JAVA: CyclomaticComplexityRuleConfig(
        cc_value_bad=14,
        cc_value_moderate=13,
    ),
    Language.KOTLIN: CyclomaticComplexityRuleConfig(
        cc_value_bad=12,
        cc_value_moderate=11,
    ),
    Language.PYTHON: CyclomaticComplexityRuleConfig(
        cc_value_bad=10,
        cc_value_moderate=9,
    ),
    Language.JS: CyclomaticComplexityRuleConfig(
        cc_value_bad=14,
        cc_value_moderate=13,
    ),
}


class CyclomaticComplexityRule(Rule):
    def __init__(self, config: CyclomaticComplexityRuleConfig):
        self.config = config
        self.rule_type = IssueType.CYCLOMATIC_COMPLEXITY
        self.cc_value: Optional[int] = None

    def apply(self, cc_value):
        self.cc_value = cc_value
        if cc_value > self.config.cc_value_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = cc_value - self.config.cc_value_bad
        elif cc_value > self.config.cc_value_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = cc_value - self.config.cc_value_moderate
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        return QualityType.EXCELLENT

    def merge(self, other: 'CyclomaticComplexityRule') -> 'CyclomaticComplexityRule':
        config = CyclomaticComplexityRuleConfig(
            min(self.config.cc_value_bad, other.config.cc_value_bad),
            min(self.config.cc_value_moderate, other.config.cc_value_moderate),
        )
        result_rule = CyclomaticComplexityRule(config)
        result_rule.apply(max(self.cc_value, other.cc_value))

        return result_rule
