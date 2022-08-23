import re

from hyperstyle.src.python.review.inspectors.common import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)
from hyperstyle.src.python.review.inspectors.tips import (
    get_augmented_assign_pattern_tip,
    get_cohesion_tip,
    get_cyclomatic_complexity_tip,
    get_line_len_tip,
    get_magic_number_tip,
)

ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='WPS432',
        new_description=get_magic_number_tip(with_number_field=True),
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
        parser=IssueDescriptionParser(re.compile(r"'.+' is too complex \((\d+)\)"), int),
    ),
    # Cohesion
    MeasurableIssueConfig(
        origin_class='H601',
        new_description=get_cohesion_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"class has low \((\d*\.?\d*)%\) cohesion"),
            converter=lambda match: convert_percentage_of_value_to_lack_of_value(float(match)),
        ),
    ),
    # Line len
    MeasurableIssueConfig(
        origin_class='E501',
        new_description=get_line_len_tip(),
        parser=IssueDescriptionParser(re.compile(r"line too long \((\d+) > \d+ characters\)"), int),
    ),
]
