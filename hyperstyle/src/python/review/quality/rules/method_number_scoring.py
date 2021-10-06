from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class MethodNumberRuleConfig:
    method_number_bad: int
    method_number_moderate: int
    method_number_good: int


common_method_number_rule_config = MethodNumberRuleConfig(
    method_number_bad=32,
    method_number_moderate=24,
    method_number_good=20,
)

LANGUAGE_TO_METHOD_NUMBER_RULE_CONFIG = {
    Language.JAVA: common_method_number_rule_config,
    Language.PYTHON: common_method_number_rule_config,
    Language.KOTLIN: common_method_number_rule_config,
    Language.JS: common_method_number_rule_config,
}


class MethodNumberRule(Rule):
    def __init__(self, config: MethodNumberRuleConfig):
        self.config = config
        self.rule_type = IssueType.METHOD_NUMBER
        self.method_number: Optional[int] = None

    def apply(self, method_number):
        self.method_number = method_number
        if method_number > self.config.method_number_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = method_number - self.config.method_number_bad
        elif method_number > self.config.method_number_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = method_number - self.config.method_number_moderate
        elif method_number > self.config.method_number_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = method_number - self.config.method_number_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = method_number
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        if self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'MethodNumberRule') -> 'MethodNumberRule':
        config = MethodNumberRuleConfig(
            min(self.config.method_number_bad, other.config.method_number_bad),
            min(self.config.method_number_moderate, other.config.method_number_moderate),
            min(self.config.method_number_good, other.config.method_number_good),
        )
        result_rule = MethodNumberRule(config)
        result_rule.apply(max(self.method_number, other.method_number))

        return result_rule
