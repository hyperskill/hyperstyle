import re

from hyperstyle.src.python.review.inspectors.common.tips import (
    get_bool_expr_len_tip,
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_magic_number_tip,
)
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)


ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='MagicNumber',
        new_description=get_magic_number_tip(with_number_field=False),
    ),
    # Function length
    MeasurableIssueConfig(
        origin_class='LongMethod',
        new_description=get_func_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'The function .* is too long \((\d+)\)'),
            converter={0: int},
        ),
    ),
    # Bool expression length
    MeasurableIssueConfig(
        origin_class='ComplexCondition',
        new_description=get_bool_expr_len_tip(unit_name='operands'),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'This condition is too complex \((\d+)\)'),
            converter={0: int},
        ),
    ),
    # Cyclomatic complexity
    MeasurableIssueConfig(
        origin_class='ComplexMethod',
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'The function .* appears to be too complex \((\d+)\)'),
            converter={0: int},
        ),
    ),
]
