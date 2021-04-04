from dataclasses import dataclass
from typing import Optional

from src.python.review.common.language import Language
from src.python.review.inspectors.issue import IssueType
from src.python.review.quality.model import Rule, QualityType


@dataclass
class CohesionRuleConfig:
    cohesion_lack_bad: int
    cohesion_lack_moderate: int


common_cohesion_rule_config = CohesionRuleConfig(
    cohesion_lack_bad=50,
    cohesion_lack_moderate=30,
)

LANGUAGE_TO_COHESION_RULE_CONFIG = {
    Language.JAVA: common_cohesion_rule_config,
    Language.PYTHON: common_cohesion_rule_config,
    Language.KOTLIN: common_cohesion_rule_config,
    Language.JS: common_cohesion_rule_config,
}


class CohesionRule(Rule):
    def __init__(self, config: CohesionRuleConfig):
        self.config = config
        self.rule_type = IssueType.COHESION
        self.cohesion_lack: Optional[int] = None

    def apply(self, cohesion_lack: int):
        self.cohesion_lack = cohesion_lack
        if cohesion_lack > self.config.cohesion_lack_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = cohesion_lack - self.config.cohesion_lack_bad
        elif cohesion_lack > self.config.cohesion_lack_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = cohesion_lack - self.config.cohesion_lack_moderate
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        return QualityType.EXCELLENT

    def merge(self, other: 'CohesionRule') -> 'CohesionRule':
        config = CohesionRuleConfig(
            min(self.config.cohesion_lack_bad, other.config.cohesion_lack_bad),
            min(self.config.cohesion_lack_moderate, other.config.cohesion_lack_moderate),
        )
        result_rule = CohesionRule(config)
        result_rule.apply(max(self.cohesion_lack, other.cohesion_lack))

        return result_rule
