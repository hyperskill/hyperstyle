import enum
import logging
from functools import partial
from pathlib import Path
from typing import Final, List

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.reviewers.common import perform_language_review
from hyperstyle.src.python.review.reviewers.python import perform_python_review
from hyperstyle.src.python.review.reviewers.review_result import GeneralReviewResult
from hyperstyle.src.python.review.reviewers.utils.metadata_exploration import explore_file, explore_project
from hyperstyle.src.python.review.reviewers.utils.print_review import (
    print_review_result_as_json,
    print_review_result_as_multi_file_json,
    print_review_result_as_text,
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
    Language.JS: partial(perform_language_review, language=Language.JS),
}


class OutputFormat(enum.Enum):
    JSON = 'json'
    TEXT = 'text'

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for _, member in OutputFormat.__members__.items()]


def perform_and_print_review(path: Path,
                             output_format: OutputFormat,
                             config: ApplicationConfig) -> int:
    review_result = perform_review(path, config)

    for file_review_result in review_result.file_review_results:
        file_review_result.file_path = file_review_result.file_path.relative_to(path)

    if OutputFormat.JSON == output_format:
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
            logger.error(f'Unsupported language. Extensions {metadata.extensions} for project {path}')
            raise UnsupportedLanguage(path, metadata.extensions)
        languages = list(metadata.languages.difference({Language.UNKNOWN}))

    # TODO start review for several languages and do something with the results
    reviewer = language_to_reviewer[languages[0]]

    return reviewer(metadata, config)
