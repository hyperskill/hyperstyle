from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class MaintainabilityRuleConfig:
    maintainability_lack_good: int
    maintainability_lack_moderate: int
    maintainability_lack_bad: int


# TODO: Need testing
# In Radon, the maintainability index is ranked as follows:
# 20-100: Very high
# 10-19: Medium
# 0-9: Extremely low
# Therefore, maintainability_lack_bad = 90, and maintainability_lack_moderate = 80.
common_maintainability_rule_config = MaintainabilityRuleConfig(
    maintainability_lack_good=50,
    maintainability_lack_moderate=80,
    maintainability_lack_bad=90,
)

LANGUAGE_TO_MAINTAINABILITY_RULE_CONFIG = {
    Language.JAVA: common_maintainability_rule_config,
    Language.PYTHON: common_maintainability_rule_config,
    Language.KOTLIN: common_maintainability_rule_config,
    Language.JS: common_maintainability_rule_config,
}


class MaintainabilityRule(Rule):
    def __init__(self, config: MaintainabilityRuleConfig):
        self.config = config
        self.rule_type = IssueType.MAINTAINABILITY
        self.maintainability_lack: Optional[int] = None

    def apply(self, maintainability_lack):
        self.maintainability_lack = maintainability_lack
        if maintainability_lack > self.config.maintainability_lack_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = maintainability_lack - self.config.maintainability_lack_bad
        elif maintainability_lack > self.config.maintainability_lack_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = maintainability_lack - self.config.maintainability_lack_moderate
        elif maintainability_lack > self.config.maintainability_lack_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = maintainability_lack - self.config.maintainability_lack_good
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

    def merge(self, other: 'MaintainabilityRule') -> 'MaintainabilityRule':
        config = MaintainabilityRuleConfig(
            min(self.config.maintainability_lack_bad, other.config.maintainability_lack_bad),
            min(self.config.maintainability_lack_moderate, other.config.maintainability_lack_moderate),
            min(self.config.maintainability_lack_good, other.config.maintainability_lack_good),
        )
        result_rule = MaintainabilityRule(config)
        result_rule.apply(max(self.maintainability_lack, other.maintainability_lack))

        return result_rule
