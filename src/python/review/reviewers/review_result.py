from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.python.review.inspectors.issue import BaseIssue
from src.python.review.quality.model import Quality


@dataclass
class FileReviewResult:
    file_path: Path
    issues: List[BaseIssue]
    quality: Quality


@dataclass
class ReviewResult:
    file_review_results: List[FileReviewResult]
    general_quality: Quality
    issue_class_to_penalty_coefficient: Dict[str, int]

    @property
    def all_issues(self) -> List[BaseIssue]:
        issues = []
        for file_review_result in self.file_review_results:
            issues.extend(file_review_result.issues)

        return issues
