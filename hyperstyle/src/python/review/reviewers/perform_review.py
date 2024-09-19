from __future__ import annotations

import enum
import logging
from functools import partial
from typing import Final, TYPE_CHECKING

from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.issue.issue import IssueType
from hyperstyle.src.python.review.reviewers.common import perform_language_review
from hyperstyle.src.python.review.reviewers.go import perform_go_review
from hyperstyle.src.python.review.reviewers.python import perform_python_review
from hyperstyle.src.python.review.reviewers.utils.metadata_exploration import (
    explore_file,
    explore_in_memory_metadata,
    explore_project,
    Metadata,
)
from hyperstyle.src.python.review.reviewers.utils.print_review import (
    print_review_result_as_json,
    print_review_result_as_multi_file_json,
    print_review_result_as_text,
)

if TYPE_CHECKING:
    from pathlib import Path

    from hyperstyle.src.python.review.application_config import ApplicationConfig
    from hyperstyle.src.python.review.reviewers.review_result import GeneralReviewResult

logger: Final = logging.getLogger(__name__)


class UnsupportedLanguageError(Exception):
    pass


class PathNotExistsError(Exception):
    pass


language_to_reviewer = {
    Language.PYTHON: perform_python_review,
    Language.JAVA: partial(perform_language_review, language=Language.JAVA),
    Language.KOTLIN: partial(perform_language_review, language=Language.KOTLIN),
    Language.JS: partial(perform_language_review, language=Language.JS),
    Language.GO: perform_go_review,
}


class OutputFormat(enum.Enum):
    JSON = "json"
    TEXT = "text"

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for _, member in OutputFormat.__members__.items()]


def perform_and_print_review(path: Path, output_format: OutputFormat, config: ApplicationConfig) -> int:
    review_result = perform_review(path, config)

    for file_review_result in review_result.file_review_results:
        file_review_result.file_path = file_review_result.file_path.relative_to(path)

    if output_format == OutputFormat.JSON:
        if config.new_format:
            print_review_result_as_multi_file_json(review_result, config)
        else:
            print_review_result_as_json(review_result, config)
    else:
        print_review_result_as_text(review_result, path, config)

    # Don't count INFO issues too
    return len(list(filter(lambda issue: issue.type != IssueType.INFO, review_result.issues)))


def perform_review(path: Path, config: ApplicationConfig) -> GeneralReviewResult:
    if not path.exists():
        raise PathNotExistsError

    if path.is_file():
        metadata = explore_file(path)
        if metadata.language == Language.UNKNOWN:
            logger.error(f"Unsupported language. Extension {metadata.extension} for file {path}")
            raise UnsupportedLanguageError(path, metadata.extension)
        languages = [metadata.language]
    else:
        metadata = explore_project(path)
        if metadata.languages == {Language.UNKNOWN}:
            logger.error(f"Unsupported language. Extensions {metadata.extensions} for project {path}")
            raise UnsupportedLanguageError(path, metadata.extensions)
        languages = list(metadata.languages.difference({Language.UNKNOWN}))

    if config.language is not None:
        languages = [config.language]
    languages.sort()

    return _preform_review(metadata, languages, config)


def _preform_review(
    metadata: Metadata, languages: list[Language], config: ApplicationConfig
) -> GeneralReviewResult:
    # TODO: start review for several languages and do something with the results
    reviewer = language_to_reviewer[languages[0]]
    return reviewer(metadata, config)


def preform_review_in_memory(code: str, language: Language, config: ApplicationConfig) -> GeneralReviewResult:
    metadata = explore_in_memory_metadata(code)
    return _preform_review(metadata, [language], config)
