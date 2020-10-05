from dataclasses import dataclass
from pathlib import Path
from typing import List

from review.inspectors.issue import BaseIssue
from review.quality.model import Quality


@dataclass
class FileReviewResult:
    file_path: Path
    issues: List[BaseIssue]
    quality: Quality


@dataclass
class ReviewResult:
    file_review_results: List[FileReviewResult]
    general_quality: Quality

    @property
    def all_issues(self) -> List[BaseIssue]:
        issues = []
        for file_review_result in self.file_review_results:
            issues.extend(file_review_result.issues)

        return issues
