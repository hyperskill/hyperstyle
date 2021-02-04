import enum
import logging
from functools import partial
from pathlib import Path
from typing import Final

from src.python.review.application_config import ApplicationConfig
from src.python.review.common.language import Language
from src.python.review.reviewers.common import perform_language_review
from src.python.review.reviewers.python import perform_python_review
from src.python.review.reviewers.review_result import ReviewResult
from src.python.review.reviewers.utils.metadata_exploration import explore_file, explore_project
from src.python.review.reviewers.utils.print_review import (
    print_review_result_as_json,
    print_review_result_as_multi_file_json,
    print_review_result_as_text
)

logger: Final = logging.getLogger(__name__)


class UnsupportedLanguage(Exception):
    pass


class PathNotExists(Exception):
    pass


language_to_reviewer = {
    Language.PYTHON: perform_python_review,
    Language.JAVA: partial(perform_language_review, language=Language.JAVA),
    Language.KOTLIN: partial(perform_language_review, language=Language.KOTLIN),
    Language.JS: partial(perform_language_review, language=Language.JS)
}


class OutputFormat(enum.Enum):
    JSON = 'json'
    TEXT = 'text'

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)


def perform_and_print_review(path: Path,
                             output_format: OutputFormat,
                             config: ApplicationConfig) -> int:
    review_result = perform_review(path, config)

    for file_review_result in review_result.file_review_results:
        file_review_result.file_path = file_review_result.file_path.relative_to(path)

    if OutputFormat.JSON == output_format:
        if config.new_format:
            print_review_result_as_multi_file_json(review_result)
        else:
            print_review_result_as_json(review_result)
    else:
        print_review_result_as_text(review_result, path)

    return len(review_result.all_issues)


def perform_review(path: Path, config: ApplicationConfig) -> ReviewResult:
    if not path.exists():
        raise PathNotExists

    if path.is_file():
        metadata = explore_file(path)
        if metadata.language == Language.UNKNOWN:
            logger.error(f'Unsupported language. Extension {metadata.extension} for file {path}')
            raise UnsupportedLanguage(path, metadata.extension)
        languages = [metadata.language]
    else:
        metadata = explore_project(path)
        if metadata.languages == {Language.UNKNOWN}:
            logger.error(f'Unsupported language. Extensions '
                         f'{metadata.extensions} for project {path}')
            raise UnsupportedLanguage(path, metadata.extensions)
        languages = list(metadata.languages.difference({Language.UNKNOWN}))

    # TODO start review for several languages and do something with the results
    reviewer = language_to_reviewer[languages[0]]

    return reviewer(metadata, config)
