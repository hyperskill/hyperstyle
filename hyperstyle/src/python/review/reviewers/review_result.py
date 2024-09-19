from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from hyperstyle.src.python.review.inspectors.common.issue.issue import BaseIssue, IssueDifficulty
    from hyperstyle.src.python.review.quality.model import Quality
    from hyperstyle.src.python.review.quality.penalty import Punisher


@dataclass
class ReviewResult:
    """ReviewResult contains a list of issues, as well as quality and punisher obtained with these issues."""

    quality_by_difficulty: dict[IssueDifficulty, Quality]
    punisher_by_difficulty: dict[IssueDifficulty, Punisher]
    issues: list[BaseIssue]


@dataclass
class FileReviewResult(ReviewResult):
    """FileReviewResult contains the information needed to output about a particular inspected file."""

    file_path: Path


@dataclass
class GeneralReviewResult(ReviewResult):
    """GeneralReviewResult contains the information needed to output about the entire inspected project."""

    file_review_results: list[FileReviewResult]
