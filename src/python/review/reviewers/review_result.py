from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.python.review.inspectors.issue import BaseIssue
from src.python.review.quality.model import Quality
from src.python.review.quality.penalty import Punisher


@dataclass
class ReviewResult:
    """
    ReviewResult contains a list of issues, as well as quality and punisher obtained with these issues.
    """
    quality: Quality
    punisher: Punisher
    issues: List[BaseIssue]


@dataclass
class FileReviewResult(ReviewResult):
    """
    FileReviewResult contains the information needed to output about a particular inspected file.
    """
    file_path: Path


@dataclass
class GeneralReviewResult(ReviewResult):
    """
    GeneralReviewResult contains the information needed to output about the entire inspected project.
    """
    file_review_results: List[FileReviewResult]
