from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class ResponseRuleConfig:
    response_moderate: int
    response_good: int


common_response_rule_config = ResponseRuleConfig(
    response_moderate=69,
    response_good=59,
)

LANGUAGE_TO_RESPONSE_RULE_CONFIG = {
    Language.JAVA: common_response_rule_config,
    Language.PYTHON: common_response_rule_config,
    Language.KOTLIN: common_response_rule_config,
    Language.JS: common_response_rule_config,
}


class ResponseRule(Rule):
    def __init__(self, config: ResponseRuleConfig):
        self.config = config
        self.rule_type = IssueType.CLASS_RESPONSE
        self.response: Optional[int] = None

    def apply(self, response):
        self.response = response
        if response > self.config.response_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = response - self.config.response_moderate
        elif response > self.config.response_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = response - self.config.response_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = response
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'ResponseRule') -> 'ResponseRule':
        config = ResponseRuleConfig(
            min(self.config.response_moderate, other.config.response_moderate),
            min(self.config.response_good, other.config.response_good),
        )
        result_rule = ResponseRule(config)
        result_rule.apply(max(self.response, other.response))

        return result_rule
