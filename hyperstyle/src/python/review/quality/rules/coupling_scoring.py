from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class CouplingRuleConfig:
    coupling_bad: int
    coupling_moderate: int


common_coupling_rule_config = CouplingRuleConfig(
    coupling_bad=30,
    coupling_moderate=20,
)

LANGUAGE_TO_COUPLING_RULE_CONFIG = {
    Language.JAVA: common_coupling_rule_config,
    Language.PYTHON: common_coupling_rule_config,
    Language.KOTLIN: common_coupling_rule_config,
    Language.JS: common_coupling_rule_config,
}


class CouplingRule(Rule):
    def __init__(self, config: CouplingRuleConfig):
        self.config = config
        self.rule_type = IssueType.COUPLING
        self.coupling: Optional[int] = None

    def apply(self, coupling):
        self.coupling = coupling
        if coupling > self.config.coupling_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = coupling - self.config.coupling_bad
        elif coupling > self.config.coupling_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = coupling - self.config.coupling_moderate
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = coupling
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        return QualityType.EXCELLENT

    def merge(self, other: 'CouplingRule') -> 'CouplingRule':
        config = CouplingRuleConfig(
            min(self.config.coupling_bad, other.config.coupling_bad),
            min(self.config.coupling_moderate, other.config.coupling_moderate),
        )
        result_rule = CouplingRule(config)
        result_rule.apply(max(self.coupling, other.coupling))

        return result_rule
