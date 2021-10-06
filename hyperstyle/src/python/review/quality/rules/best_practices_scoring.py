from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class BestPracticesRuleConfig:
    n_best_practices_moderate: int
    n_best_practices_good: int
    n_files: int


common_best_practices_rule_config = BestPracticesRuleConfig(
    n_best_practices_moderate=4,
    n_best_practices_good=1,
    n_files=1,
)

LANGUAGE_TO_BEST_PRACTICES_RULE_CONFIG = {
    Language.JAVA: common_best_practices_rule_config,
    Language.PYTHON: common_best_practices_rule_config,
    Language.KOTLIN: common_best_practices_rule_config,
    Language.JS: common_best_practices_rule_config,
}


class BestPracticesRule(Rule):
    def __init__(self, config: BestPracticesRuleConfig):
        self.config = config
        self.rule_type = IssueType.BEST_PRACTICES
        self.n_best_practices: Optional[int] = None

    def apply(self, n_best_practices):
        self.n_best_practices = n_best_practices
        ratio = n_best_practices / self.config.n_files

        if ratio > self.config.n_best_practices_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = ratio - self.config.n_best_practices_moderate
        elif ratio > self.config.n_best_practices_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = ratio - self.config.n_best_practices_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        if self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'BestPracticesRule') -> 'BestPracticesRule':
        config = BestPracticesRuleConfig(
            min(self.config.n_best_practices_moderate, other.config.n_best_practices_moderate),
            min(self.config.n_best_practices_good, other.config.n_best_practices_good),
            n_files=self.config.n_files + other.config.n_files,
        )
        result_rule = BestPracticesRule(config)
        result_rule.apply(self.n_best_practices + other.n_best_practices)

        return result_rule
