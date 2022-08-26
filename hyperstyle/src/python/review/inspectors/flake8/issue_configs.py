import re

from hyperstyle.src.python.review.inspectors.common.tips import (
    get_augmented_assign_pattern_tip,
    get_cohesion_tip,
    get_cyclomatic_complexity_tip,
    get_line_len_tip,
    get_magic_number_tip,
)
from hyperstyle.src.python.review.inspectors.common.utils import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)

ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='WPS432',
        new_description=get_magic_number_tip(),
        parser=IssueDescriptionParser(re.compile(r'^Found magic number: (.+)$')),
    ),
    IssueConfig(
        origin_class='WPS350',
        new_description=get_augmented_assign_pattern_tip(),
    ),
    IssueConfig(
        origin_class='B007',
        new_description=(
            "Loop control variable '{0}' not used within the loop body. "
            "If this is intended, replace it with an underscore."
        ),
        parser=IssueDescriptionParser(re.compile(r"Loop control variable '(.+)' not used within the loop body")),
    ),
    # Cyclomatic Complexity
    MeasurableIssueConfig(
        origin_class='C901',
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"'.+' is too complex \((\d+)\)"),
            converter={0: int},
        ),
    ),
    # Cohesion
    MeasurableIssueConfig(
        origin_class='H601',
        new_description=get_cohesion_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"class has low \((\d*\.?\d*)%\) cohesion"),
            converter={0: lambda match: convert_percentage_of_value_to_lack_of_value(float(match))},
        ),
    ),
    # Line len
    MeasurableIssueConfig(
        origin_class='E501',
        new_description=get_line_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"line too long \((\d+) > \d+ characters\)"),
            converter={0: int},
        ),
    ),
]
