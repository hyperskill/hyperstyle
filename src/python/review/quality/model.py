import abc
import textwrap
from enum import Enum, unique
from functools import total_ordering
from typing import List

from src.python.review.inspectors.issue import IssueType
from src.python.review.reviewers.utils.penalty import get_penalty_score


@total_ordering
@unique
class QualityType(Enum):
    BAD = 'BAD'
    MODERATE = 'MODERATE'
    GOOD = 'GOOD'
    EXCELLENT = 'EXCELLENT'

    def to_number(self) -> int:
        type_to_number = {
            QualityType.BAD: 0,
            QualityType.MODERATE: 1,
            QualityType.GOOD: 2,
            QualityType.EXCELLENT: 3,
        }

        return type_to_number[self]

    def __le__(self, other: 'QualityType') -> bool:
        return self.to_number() < other.to_number()


class Rule(abc.ABC):
    rule_type: IssueType
    quality_type: QualityType
    next_level_type: QualityType
    next_level_delta: int
    value: int

    @abc.abstractmethod
    def apply(self, value):
        pass


class Quality:
    def __init__(self, rules: List[Rule], penalty_coefficient: int = 0):
        self.rules = rules
        self.penalty_coefficient = penalty_coefficient

    @property
    def quality_type(self) -> QualityType:
        return min(map(lambda rule: rule.quality_type, self.rules), default=QualityType.EXCELLENT)

    @property
    def quality_with_penalty(self) -> QualityType:
        numbered_quality_type = self.quality_type.to_number()
        numbered_quality_type -= get_penalty_score(self.penalty_coefficient)

        if numbered_quality_type <= 0:
            return QualityType.BAD
        elif numbered_quality_type == 1:
            return QualityType.MODERATE
        elif numbered_quality_type == 2:
            return QualityType.GOOD
        else:
            return QualityType.EXCELLENT

    @property
    def next_quality_type(self) -> QualityType:
        return min(map(lambda rule: rule.next_level_type, self.rules), default=QualityType.EXCELLENT)

    # TODO: why rule.quality_type == quality_type for next level????
    @property
    def next_level_requirements(self) -> List[Rule]:
        quality_type = self.quality_type
        return [rule for rule in self.rules if rule.quality_type == quality_type]

    def merge(self, other: 'Quality') -> 'Quality':
        self_type_to_rule = {type(rule): rule for rule in self.rules}
        other_type_to_rule = {type(rule): rule for rule in other.rules}
        common_rule_types = set(self_type_to_rule).intersection(other_type_to_rule)

        result_rules = []
        for rule_type in common_rule_types:
            self_rule = self_type_to_rule[rule_type]
            other_rule = other_type_to_rule[rule_type]
            result_rules.append(self_rule.merge(other_rule))

        for rule_type in set(self_type_to_rule).difference(common_rule_types):
            result_rules.append(self_type_to_rule[rule_type])

        for rule_type in set(other_type_to_rule).difference(common_rule_types):
            result_rules.append(other_type_to_rule[rule_type])

        return Quality(result_rules, self.penalty_coefficient)

    def __str__(self):
        message_head_part = f'Code quality (beta): {self.quality_type.value}\n'
        message_next_level_part = ''
        message_deltas_part = ''

        if self.quality_type != QualityType.EXCELLENT:
            message_next_level_part = f"""\
                Next level: {self.next_quality_type.value}
                Next level requirements:
            """
            message_next_level_part = textwrap.dedent(message_next_level_part)

            for rule in self.next_level_requirements:
                message_deltas_part += f'{rule.rule_type.value}: {rule.next_level_delta}\n'

        return message_head_part + message_next_level_part + message_deltas_part
