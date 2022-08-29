import re

from hyperstyle.src.python.review.inspectors.common.tips import (
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
    get_magic_number_tip,
    get_maintainability_index_tip,
)
from hyperstyle.src.python.review.inspectors.common.utils import convert_percentage_of_value_to_lack_of_value
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)

ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='gomnd',
        new_description=get_magic_number_tip(),
        parser=IssueDescriptionParser(re.compile('^mnd: Magic number: (.*), in .* detected$')),
    ),
    MeasurableIssueConfig(
        origin_class='cyclop',
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'^calculated cyclomatic complexity for function .* is (\d+), max is -1$'),
            converter={0: int},
        ),
    ),
    MeasurableIssueConfig(
        origin_class='funlen',
        new_description=get_func_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"^Function '.*' is too long \((\d+) > 1\)$"),
            converter={0: int},
        ),
    ),
    MeasurableIssueConfig(
        origin_class='lll',
        new_description=get_line_len_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'^line is (\d+) characters$'),
            converter={0: int},
        ),
    ),
    MeasurableIssueConfig(
        origin_class='maintidx',
        new_description=get_maintainability_index_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(
                r'^Function name: .*, Cyclomatic Complexity: .*, Halstead Volume: .*, Maintainability Index: (.+)$',
            ),
            converter={0: lambda group: convert_percentage_of_value_to_lack_of_value(float(group))},
        ),
    ),
]
