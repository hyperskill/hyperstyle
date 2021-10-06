from dataclasses import dataclass
from typing import Optional

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.quality.model import QualityType, Rule


@dataclass
class ErrorProneRuleConfig:
    n_error_prone_bad: int


# TODO: It is necessary to add subcategories where the following boundaries can be used:
#       GOOD: 0
#       MODERATE: 1
#       BAD: 2
common_error_prone_rule_config = ErrorProneRuleConfig(
    n_error_prone_bad=0,
)

LANGUAGE_TO_ERROR_PRONE_RULE_CONFIG = {
    Language.JAVA: common_error_prone_rule_config,
    Language.KOTLIN: common_error_prone_rule_config,
    Language.PYTHON: common_error_prone_rule_config,
    Language.JS: common_error_prone_rule_config,
}


class ErrorProneRule(Rule):
    def __init__(self, config: ErrorProneRuleConfig):
        self.config = config
        self.rule_type = IssueType.ERROR_PRONE
        self.n_error_prone: Optional[int] = None

    def apply(self, n_error_prone):
        self.n_error_prone = n_error_prone
        if n_error_prone > self.config.n_error_prone_bad:
            self.quality_type = QualityType.BAD
            self.next_level_delta = n_error_prone - self.config.n_error_prone_bad
        else:
            self.quality_type = QualityType.EXCELLENT
            self.next_level_delta = n_error_prone
        self.next_level_type = self.__get_next_quality_type()

    def __get_next_quality_type(self) -> QualityType:
        return QualityType.EXCELLENT

    def merge(self, other: 'ErrorProneRule') -> 'ErrorProneRule':
        config = ErrorProneRuleConfig(min(self.config.n_error_prone_bad,
                                          other.config.n_error_prone_bad))
        result_rule = ErrorProneRule(config)
        result_rule.apply(self.n_error_prone + other.n_error_prone)

        return result_rule
