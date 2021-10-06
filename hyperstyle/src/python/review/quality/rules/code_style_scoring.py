from dataclasses import dataclass

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class CodeStyleRuleConfig:
    n_code_style_bad: float
    n_code_style_moderate: float
    n_code_style_good: float
    n_code_style_lines_bad: int
    language: Language


java_code_style_rule_config = CodeStyleRuleConfig(
    n_code_style_bad=0.23,
    n_code_style_moderate=0.17,
    n_code_style_good=0,
    n_code_style_lines_bad=10,
    language=Language.JAVA,
)

python_code_style_rule_config = CodeStyleRuleConfig(
    n_code_style_bad=0.35,
    n_code_style_moderate=0.17,
    n_code_style_good=0,
    n_code_style_lines_bad=5,
    language=Language.PYTHON,
)

kotlin_code_style_rule_config = CodeStyleRuleConfig(
    n_code_style_bad=0.16,
    n_code_style_moderate=0.07,
    n_code_style_good=0,
    n_code_style_lines_bad=10,
    language=Language.KOTLIN,
)

js_code_style_rule_config = CodeStyleRuleConfig(
    n_code_style_bad=0.23,
    n_code_style_moderate=0.17,
    n_code_style_good=0,
    n_code_style_lines_bad=10,
    language=Language.JAVA,
)

LANGUAGE_TO_CODE_STYLE_RULE_CONFIG = {
    Language.JAVA: java_code_style_rule_config,
    Language.KOTLIN: kotlin_code_style_rule_config,
    Language.PYTHON: python_code_style_rule_config,
    Language.JS: js_code_style_rule_config,
}


class CodeStyleRule(Rule):
    def __init__(self, config: CodeStyleRuleConfig):
        self.config = config
        self.rule_type = IssueType.CODE_STYLE
        self.total_lines = 0
        self.n_code_style_lines = 0
        self.ratio = 0
        self.quality_type = None
        self.next_level_delta = 0

    # TODO: refactor
    def apply(self, n_code_style_lines, n_code_style, total_lines):
        self.total_lines = total_lines
        self.n_code_style_lines = n_code_style_lines
        self.n_code_style = n_code_style

        self.update_quality(n_code_style_lines, n_code_style)
        self.ratio = self.get_ratio(n_code_style_lines, total_lines, self.config.language)

        if self.ratio > self.config.n_code_style_bad:
            self.save_quality(QualityType.BAD)
        elif self.ratio > self.config.n_code_style_moderate:
            self.save_quality(QualityType.MODERATE)
        elif self.ratio > self.config.n_code_style_good:
            self.save_quality(QualityType.GOOD)
        else:
            self.save_quality(QualityType.EXCELLENT)

        if n_code_style_lines > self.config.n_code_style_lines_bad:
            self.quality_type = QualityType.BAD

    @staticmethod
    def get_ratio(n_code_style_lines: int, total_lines: int, language: Language) -> float:
        if language == Language.PYTHON:
            return n_code_style_lines / max(1, total_lines)
        else:
            return n_code_style_lines / max(1, total_lines - 4)

    def update_quality(self, n_code_style_lines: int, n_code_style: int):
        if self.config.language == Language.PYTHON:
            if n_code_style == 1:
                self.save_quality(QualityType.MODERATE)
        else:
            if n_code_style_lines == 1:
                self.save_quality(QualityType.GOOD)
            elif n_code_style_lines == 2:
                self.save_quality(QualityType.MODERATE)

    def __get_next_quality_type(self) -> QualityType:
        if self.quality_type == QualityType.BAD:
            return QualityType.MODERATE
        if self.quality_type == QualityType.MODERATE:
            return QualityType.GOOD
        return QualityType.EXCELLENT

    def merge(self, other: 'CodeStyleRule') -> 'CodeStyleRule':
        if self.quality_type > other.quality_type:
            return other
        else:
            return self

    def save_quality(self, quality_type):
        if not self.quality_type:
            self.quality_type = quality_type
        self.quality_type = max(self.quality_type, quality_type)
        self.next_level_type = self.__get_next_quality_type()
