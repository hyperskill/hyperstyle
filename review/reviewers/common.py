from collections import defaultdict
from typing import List, Optional

from review.application_config import ApplicationConfig
from review.common.language import Language
from review.common.parallel_runner import inspect_in_parallel
from review.inspectors.checkstyle.checkstyle import CheckstyleInspector
from review.inspectors.detekt.detekt import DetektInspector
from review.inspectors.eslint.eslint import ESLintInspector
from review.inspectors.flake8.flake8 import Flake8Inspector
from review.inspectors.issue import BaseIssue
from review.inspectors.pmd.pmd import PMDInspector
from review.inspectors.pyast.python_ast import PythonAstInspector
from review.inspectors.pylint.pylint import PylintInspector
from review.quality.evaluate_quality import evaluate_quality
from review.quality.model import Quality
from review.reviewers.review_result import FileReviewResult, ReviewResult
from review.reviewers.utils.code_statistics import gather_code_statistics
from review.reviewers.utils.issues_filter import (
    filter_duplicate_issues, filter_low_metric_issues
)
from review.reviewers.utils.metadata_exploration import FileMetadata, Metadata

LANGUAGE_TO_INSPECTORS = {
    Language.PYTHON: [
        PylintInspector(),
        Flake8Inspector(),
        PythonAstInspector(),
    ],
    Language.JAVA: [
        CheckstyleInspector(),
        PMDInspector(),
        # SpotbugsInspector(),
        # SpringlintInspector()  # TODO experimental
    ],
    Language.KOTLIN: [
        DetektInspector(),
    ],
    Language.JS: [
        ESLintInspector(),
    ]
}


def perform_language_review(metadata: Metadata,
                            config: ApplicationConfig,
                            language: Language) -> ReviewResult:
    inspectors = LANGUAGE_TO_INSPECTORS[language]

    issues = inspect_in_parallel(metadata.path, config, inspectors)
    if issues:
        issues = filter_low_metric_issues(issues, language)

        if not config.allow_duplicates:
            issues = filter_duplicate_issues(issues)

    if isinstance(metadata, FileMetadata):
        files_metadata = [metadata]
        issues = filter_out_of_range_issues(issues, config.start_line, config.end_line)
    else:
        files_metadata = metadata.language_to_files[language]

    file_path_to_issues = defaultdict(list)
    for issue in issues:
        file_path_to_issues[issue.file_path].append(issue)

    file_review_results = []
    general_quality = Quality([])
    for file_metadata in files_metadata:
        issues = file_path_to_issues[file_metadata.path]
        code_statistics = gather_code_statistics(issues, file_metadata.path)
        code_statistics.total_lines = min(code_statistics.total_lines,
                                          get_range_lines(config.start_line, config.end_line))

        quality = evaluate_quality(code_statistics, language)
        general_quality = general_quality.merge(quality)

        file_review_results.append(FileReviewResult(
            file_metadata.path,
            issues,
            quality
        ))

    return ReviewResult(
        file_review_results,
        general_quality
    )


def filter_out_of_range_issues(issues: List[BaseIssue],
                               start_line: int = 1,
                               end_line: Optional[int] = None) -> List[BaseIssue]:

    if end_line is None:
        end_line = 100_000_000

    suitable_issues = []
    for issue in issues:
        if start_line <= issue.line_no <= end_line:
            suitable_issues.append(issue)

    return suitable_issues


def get_range_lines(start_line: int = 1, end_line: Optional[int] = None) -> int:
    if end_line is None:
        return 100_000_000

    return end_line - start_line + 1
