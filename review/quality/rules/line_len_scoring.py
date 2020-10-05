from dataclasses import dataclass

from review.quality.model import QualityType, Rule
from review.inspectors.issue import IssueType
from review.common.language import Language


@dataclass
class LineLengthRuleConfig:
    n_line_len_bad: float
    n_line_len_good: float


common_line_length_rule_config = LineLengthRuleConfig(
    n_line_len_bad=0.05,
    n_line_len_good=0.035
)

LANGUAGE_TO_LINE_LENGTH_RULE_CONFIG = {
    Language.JAVA: common_line_length_rule_config,
    Language.KOTLIN: common_line_length_rule_config,
    Language.PYTHON: common_line_length_rule_config,
    Language.JS: common_line_length_rule_config,
}


class LineLengthRule(Rule):
    def __init__(self, config: LineLengthRuleConfig):
        self.config = config
        self.rule_type = IssueType.LINE_LEN

    def apply(self, n_line_len, n_lines):
        self.ratio = n_line_len / max(n_lines, 1)
        self.n_line_len = n_line_len
        self.n_lines = n_lines

        if self.ratio > self.config.n_line_len_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = n_line_len - self.config.n_line_len_bad
        elif self.ratio > self.config.n_line_len_good:
            self.quality_type = QualityType.GOOD
            self.next_level_delta = n_line_len - self.config.n_line_len_good
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = 0
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'LineLengthRule') -> 'LineLengthRule':
        config = LineLengthRuleConfig(
            min(self.config.n_line_len_bad, other.config.n_line_len_bad),
            min(self.config.n_line_len_good, other.config.n_line_len_good)
        )
        result_rule = LineLengthRule(config)
        result_rule.apply(self.n_line_len + other.n_line_len, self.n_lines + other.n_lines)

        return result_rule
