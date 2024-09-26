from __future__ import annotations

from dataclasses import dataclass

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.issue.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class FunctionLengthRuleConfig:
    func_len_bad: int


LANGUAGE_TO_FUNCTION_LENGTH_RULE_CONFIG = {
    Language.JAVA: FunctionLengthRuleConfig(
        func_len_bad=69,
    ),
    Language.KOTLIN: FunctionLengthRuleConfig(
        func_len_bad=69,
    ),
    Language.PYTHON: FunctionLengthRuleConfig(
        func_len_bad=49,
    ),
    Language.JS: FunctionLengthRuleConfig(
        func_len_bad=69,
    ),
    # Using java config
    Language.GO: FunctionLengthRuleConfig(
        func_len_bad=69,
    ),
}


class FunctionLengthRule(Rule):
    def __init__(self, config: FunctionLengthRuleConfig) -> None:
        self.config = config
        self.rule_type = IssueType.FUNC_LEN
        self.func_len: int | None = None

    def apply(self, func_len: int) -> None:
        self.func_len = func_len
        if func_len > self.config.func_len_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = func_len - self.config.func_len_bad
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        return QualityType.EXCELLENT

    def merge(self, other: Rule) -> FunctionLengthRule:
        assert isinstance(other, FunctionLengthRule)
        config = FunctionLengthRuleConfig(
            min(self.config.func_len_bad, other.config.func_len_bad),
        )
        result_rule = FunctionLengthRule(config)
        assert self.func_len is not None
        assert other.func_len is not None
        result_rule.apply(max(self.func_len, other.func_len))

        return result_rule
