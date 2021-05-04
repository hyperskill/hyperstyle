from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.python.review.inspectors.issue import BaseIssue
from src.python.review.quality.model import Quality
from src.python.review.quality.penalty import Punisher


@dataclass
class FileReviewResult:
    file_path: Path
    issues: List[BaseIssue]
    quality: Quality
    punisher: Punisher


@dataclass
class ReviewResult:
    file_review_results: List[FileReviewResult]
    general_quality: Quality
    general_punisher: Punisher

    @property
    def all_issues(self) -> List[BaseIssue]:
        issues = []
        for file_review_result in self.file_review_results:
            issues.extend(file_review_result.issues)

        return issues
