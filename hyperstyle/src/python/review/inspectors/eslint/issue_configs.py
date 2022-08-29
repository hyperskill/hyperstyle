import re

from hyperstyle.src.python.review.inspectors.common.tips import get_cyclomatic_complexity_tip
from hyperstyle.src.python.review.inspectors.issue_configs import IssueDescriptionParser, MeasurableIssueConfig

ISSUE_CONFIGS = [
    MeasurableIssueConfig(
        origin_class='complexity',
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r'complexity of (\d+)'),
            converter={0: int},
        ),
    ),
]
