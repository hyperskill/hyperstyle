import re

from hyperstyle.src.python.review.inspectors.common.tips import (
    get_bool_expr_len_tip,
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
    get_magic_number_tip,
)
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)

ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='MagicNumberCheck',
        new_description=get_magic_number_tip(),
        parser=IssueDescriptionParser(re.compile(r"'(.+)' is a magic number")),
    ),
    # Cyclomatic complexity
    MeasurableIssueConfig(
        origin_class='CyclomaticComplexityCheck',
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'Cyclomatic Complexity is (\d+)'),
            converter={0: int},
        ),
    ),
    # Function length
    MeasurableIssueConfig(
        origin_class='JavaNCSSCheck',
        new_description=get_func_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'NCSS for this method is (\d+)'),
            converter={0: int},
        ),
    ),
    # Bool expression length
    MeasurableIssueConfig(
        origin_class='BooleanExpressionComplexityCheck',
        new_description=get_bool_expr_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'Boolean expression complexity is (\d+)'),
            converter={0: int},
        ),
    ),
    # Line length
    MeasurableIssueConfig(
        origin_class='LineLengthCheck',
        new_description=get_line_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'Line is longer than \d+ characters \(found (\d+)\)'),
            converter={0: int},
        ),
    ),
]
