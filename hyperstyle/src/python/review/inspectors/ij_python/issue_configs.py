from __future__ import annotations

from hyperstyle.src.python.review.inspectors.common.issue.issue_configs import IssueConfig

ISSUE_CONFIGS: list[IssueConfig] = [
    IssueConfig(
        origin_class="E128",
        new_description="Incorrect indent",
    ),
]
