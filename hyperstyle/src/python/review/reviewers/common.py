from collections import defaultdict
from typing import List, Optional

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.common.parallel_runner import inspect_in_parallel
from hyperstyle.src.python.review.inspectors.checkstyle.checkstyle import CheckstyleInspector
from hyperstyle.src.python.review.inspectors.detekt.detekt import DetektInspector
from hyperstyle.src.python.review.inspectors.eslint.eslint import ESLintInspector
from hyperstyle.src.python.review.inspectors.flake8.flake8 import Flake8Inspector
from hyperstyle.src.python.review.inspectors.issue import BaseIssue
from hyperstyle.src.python.review.inspectors.pmd.pmd import PMDInspector
from hyperstyle.src.python.review.inspectors.pyast.python_ast import PythonAstInspector
from hyperstyle.src.python.review.inspectors.pylint.pylint import PylintInspector
from hyperstyle.src.python.review.inspectors.radon.radon import RadonInspector
from hyperstyle.src.python.review.quality.evaluate_quality import evaluate_quality
from hyperstyle.src.python.review.quality.model import Quality
from hyperstyle.src.python.review.quality.penalty import categorize, get_previous_issues_by_language, Punisher
from hyperstyle.src.python.review.reviewers.review_result import FileReviewResult, GeneralReviewResult
from hyperstyle.src.python.review.reviewers.utils.code_statistics import gather_code_statistics
from hyperstyle.src.python.review.reviewers.utils.issues_filter import (
    filter_duplicate_issues,
    filter_low_measure_issues,
    group_issues_by_difficulty,
)
from hyperstyle.src.python.review.reviewers.utils.metadata_exploration import FileMetadata, Metadata

LANGUAGE_TO_INSPECTORS = {
    Language.PYTHON: [
        PylintInspector(),
        Flake8Inspector(),
        PythonAstInspector(),
        RadonInspector(),
    ],
    Language.JAVA: [
        CheckstyleInspector(),
        PMDInspector(),
    ],
    Language.KOTLIN: [
        DetektInspector(),
    ],
    Language.JS: [
        ESLintInspector(),
    ],
}


def perform_language_review(metadata: Metadata, config: ApplicationConfig, language: Language) -> GeneralReviewResult:
    inspectors = LANGUAGE_TO_INSPECTORS[language]

    issues = inspect_in_parallel(metadata.path, config, inspectors)
    if issues:
        issues = filter_low_measure_issues(issues, language)

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

    previous_issues = get_previous_issues_by_language(config.history, language)
    categorize(previous_issues, issues)

    issues_by_difficulty = group_issues_by_difficulty(issues)

    general_punisher_by_difficulty = {
        difficulty: Punisher(issues, previous_issues) for difficulty, issues in issues_by_difficulty.items()
    }

    general_quality_by_difficulty = {
        difficulty: Quality([]) for difficulty in issues_by_difficulty.keys()
    }

    file_review_results = []
    for file_metadata in files_metadata:
        file_issues = file_path_to_issues[file_metadata.path]
        file_issues_by_difficulty = group_issues_by_difficulty(file_issues)

        code_statistics_by_difficulty = {
            difficulty: gather_code_statistics(file_issues, file_metadata.path)
            for difficulty, file_issues in file_issues_by_difficulty.items()
        }

        for code_statistics in code_statistics_by_difficulty.values():
            code_statistics.total_lines = min(code_statistics.total_lines,
                                              get_range_lines(config.start_line, config.end_line))

        punisher_by_difficulty = {
            difficulty: Punisher(file_issues, previous_issues)
            for difficulty, file_issues in file_issues_by_difficulty.items()
        }

        quality_by_difficulty = {
            difficulty: evaluate_quality(code_statistics, language)
            for difficulty, code_statistics in code_statistics_by_difficulty.items()
        }

        for difficulty, quality in quality_by_difficulty.items():
            general_quality_by_difficulty[difficulty] = general_quality_by_difficulty[difficulty].merge(quality)

        file_review_results.append(
            FileReviewResult(quality_by_difficulty, punisher_by_difficulty, file_issues, file_metadata.path),
        )

    return GeneralReviewResult(
        general_quality_by_difficulty,
        general_punisher_by_difficulty,
        issues,
        file_review_results,
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
