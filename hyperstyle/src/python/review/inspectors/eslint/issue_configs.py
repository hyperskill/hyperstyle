from __future__ import annotations

import re

from hyperstyle.src.python.review.inspectors.common.issue.issue_configs import (
    IssueConfig,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)
from hyperstyle.src.python.review.inspectors.common.issue.tips import get_cyclomatic_complexity_tip

ISSUE_CONFIGS: list[IssueConfig] = [
    MeasurableIssueConfig(
        origin_class="complexity",
        new_description=get_cyclomatic_complexity_tip(),
        parser=IssueDescriptionParser(
            regexp=re.compile(r"complexity of (\d+)"),
            converter={0: int},
        ),
    ),
]
