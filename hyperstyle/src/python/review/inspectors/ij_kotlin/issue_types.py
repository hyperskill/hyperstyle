from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hyperstyle.src.python.review.inspectors.common.issue.issue import IssueType

IJ_INSPECTION_TO_ISSUE_TYPE: dict[str, IssueType] = {}

IJ_MESSAGE_TO_ISSUE_TYPE: dict[str, dict[str, IssueType]] = {}
