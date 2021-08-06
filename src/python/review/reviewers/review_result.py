from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.python.review.inspectors.issue import BaseIssue, IssueDifficulty
from src.python.review.quality.model import Quality
from src.python.review.quality.penalty import Punisher


@dataclass
class ReviewResult:
    quality_by_difficulty: Dict[IssueDifficulty, Quality]
    punisher_by_difficulty: Dict[IssueDifficulty, Punisher]
    issues: List[BaseIssue]


@dataclass
class FileReviewResult(ReviewResult):
    file_path: Path


@dataclass
class GeneralReviewResult(ReviewResult):
    file_review_results: List[FileReviewResult]
