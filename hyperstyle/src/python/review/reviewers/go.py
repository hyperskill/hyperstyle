from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.reviewers.common import perform_language_review
from hyperstyle.src.python.review.reviewers.review_result import GeneralReviewResult
from hyperstyle.src.python.review.reviewers.utils.metadata_exploration import Metadata, ProjectMetadata


def perform_go_review(metadata: Metadata, config: ApplicationConfig) -> GeneralReviewResult:
    # The project must contain a go.mod file. If it's missing, then create it.
    if isinstance(metadata, ProjectMetadata):
        mod_file_path = metadata.path / 'go.mod'
        if not mod_file_path.exists():
            mod_file_path.write_text('module main')

    return perform_language_review(metadata, config, Language.GO)
