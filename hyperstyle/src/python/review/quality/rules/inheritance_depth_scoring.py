from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class InheritanceDepthRuleConfig:
    depth_bad: int


common_inheritance_depth_rule_config = InheritanceDepthRuleConfig(
    depth_bad=3,
)

LANGUAGE_TO_INHERITANCE_DEPTH_RULE_CONFIG = {
    Language.JAVA: common_inheritance_depth_rule_config,
    Language.PYTHON: common_inheritance_depth_rule_config,
    Language.KOTLIN: common_inheritance_depth_rule_config,
    Language.JS: common_inheritance_depth_rule_config,
}


class InheritanceDepthRule(Rule):
    def __init__(self, config: InheritanceDepthRuleConfig):
        self.config = config
        self.rule_type = IssueType.INHERITANCE_DEPTH
        self.depth: Optional[int] = None

    def apply(self, depth):
        self.depth = depth
        if depth > self.config.depth_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = depth - self.config.depth_bad
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = depth
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        return QualityType.EXCELLENT

    def merge(self, other: 'InheritanceDepthRule') -> 'InheritanceDepthRule':
        config = InheritanceDepthRuleConfig(min(self.config.depth_bad,
                                                other.config.depth_bad))
        result_rule = InheritanceDepthRule(config)
        result_rule.apply(max(self.depth, other.depth))

        return result_rule
