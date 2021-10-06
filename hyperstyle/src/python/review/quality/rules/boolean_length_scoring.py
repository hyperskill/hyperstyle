from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class BooleanExpressionRuleConfig:
    bool_expr_len_bad: int
    bool_expr_len_moderate: int
    bool_expr_len_good: int


common_boolean_expression_rule_config = BooleanExpressionRuleConfig(
    bool_expr_len_bad=6,
    bool_expr_len_moderate=5,
    bool_expr_len_good=3,
)

kotlin_boolean_expression_rule_config = BooleanExpressionRuleConfig(
    bool_expr_len_bad=9,
    bool_expr_len_moderate=7,
    bool_expr_len_good=5,
)

LANGUAGE_TO_BOOLEAN_EXPRESSION_RULE_CONFIG = {
    Language.JAVA: common_boolean_expression_rule_config,
    Language.KOTLIN: kotlin_boolean_expression_rule_config,
    Language.PYTHON: common_boolean_expression_rule_config,
    Language.JS: common_boolean_expression_rule_config,
}


class BooleanExpressionRule(Rule):
    def __init__(self, config: BooleanExpressionRuleConfig):
        self.config = config
        self.rule_type = IssueType.BOOL_EXPR_LEN
        self.bool_expr_len: Optional[int] = None

    def apply(self, bool_expr_len):
        self.bool_expr_len = bool_expr_len
        if bool_expr_len > self.config.bool_expr_len_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = bool_expr_len - self.config.bool_expr_len_bad
        elif bool_expr_len > self.config.bool_expr_len_moderate:
            self.quality_type = QualityType.MODERATE
            self.next_level_delta = bool_expr_len - self.config.bool_expr_len_moderate
        elif bool_expr_len > self.config.bool_expr_len_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = bool_expr_len - self.config.bool_expr_len_good
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

    def merge(self, other: 'BooleanExpressionRule') -> 'BooleanExpressionRule':
        config = BooleanExpressionRuleConfig(
            min(self.config.bool_expr_len_bad, other.config.bool_expr_len_bad),
            min(self.config.bool_expr_len_moderate, other.config.bool_expr_len_moderate),
            min(self.config.bool_expr_len_good, other.config.bool_expr_len_good),
        )
        result_rule = BooleanExpressionRule(config)
        result_rule.apply(max(self.bool_expr_len, other.bool_expr_len))

        return result_rule
