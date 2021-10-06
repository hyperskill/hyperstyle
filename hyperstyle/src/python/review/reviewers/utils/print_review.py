import json
import linecache
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, List, Union

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.common.file_system import get_file_line
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.quality.model import QualityType
from hyperstyle.src.python.review.quality.penalty import PenaltyIssue
from hyperstyle.src.python.review.reviewers.review_result import FileReviewResult, GeneralReviewResult, ReviewResult


def print_review_result_as_text(review_result: GeneralReviewResult, path: Path, config: ApplicationConfig) -> None:
    heading = f'\nReview of {str(path)} ({len(review_result.issues)} violations)'
    print(heading)

    if len(review_result.issues) == 0:
        print('There is no issues found')
    else:
        for file_review_result in review_result.file_review_results:
            print('*' * len(heading))
            print(f'File {file_review_result.file_path}')
            print('-' * len(heading))
            print('Line № : Column № : Type : Inspector : Origin : Description : Line : Path')

            sorted_issues = sorted(file_review_result.issues, key=lambda issue: issue.line_no)
            for issue in sorted_issues:
                line_text = linecache.getline(
                    str(issue.file_path),
                    issue.line_no,
                ).strip()

                issue_type = issue.type
                if not config.with_all_categories:
                    issue_type = issue_type.to_main_type()

                print(f'{issue.line_no} : '
                      f'{issue.column_no} : '
                      f'{issue_type.value} : '
                      f'{issue.inspector_type.value} : '
                      f'{issue.origin_class} : '
                      f'{issue.description} : '
                      f'{line_text}: '
                      f'{issue.file_path}')
            print('-' * len(heading))
            print(file_review_result.quality_by_difficulty[IssueDifficulty.HARD])

    print('*' * len(heading))
    print('General quality:')
    print(review_result.quality_by_difficulty[IssueDifficulty.HARD], end='')


def _get_quality_without_penalty(review_result: ReviewResult) -> Dict[IssueDifficulty, QualityType]:
    return {difficulty: quality.quality_type for difficulty, quality in review_result.quality_by_difficulty.items()}


def _get_quality_with_penalty(review_result: ReviewResult) -> Dict[IssueDifficulty, QualityType]:
    quality_without_penalty = _get_quality_without_penalty(review_result)

    return {
        difficulty: punisher.get_quality_with_penalty(quality_without_penalty[difficulty])
        for difficulty, punisher in review_result.punisher_by_difficulty.items()
    }


def get_quality_json_dict(quality: Dict[IssueDifficulty, QualityType], config: ApplicationConfig) -> Dict:
    quality_json_dict = {
        difficulty.value: {
            OutputJsonFields.CODE.value: quality.value,
            OutputJsonFields.TEXT.value: f'Code quality (beta): {quality.value}',
        }
        for difficulty, quality in quality.items()
    }

    if config.group_by_difficulty:
        return quality_json_dict

    return quality_json_dict[IssueDifficulty.HARD.value]


def get_influence_on_penalty_json_dict(
    origin_class: str,
    review_result: ReviewResult,
    config: ApplicationConfig,
) -> Union[Dict[IssueDifficulty, int], int]:
    quality_without_penalty = _get_quality_without_penalty(review_result)
    quality_with_penalty = _get_quality_with_penalty(review_result)

    influence_on_penalty_json_dict = {
        difficulty.value: punisher.get_issue_influence_on_penalty(origin_class)
        if quality_with_penalty[difficulty] != quality_without_penalty[difficulty]
        else 0
        for difficulty, punisher in review_result.punisher_by_difficulty.items()
    }

    if config.group_by_difficulty:
        return influence_on_penalty_json_dict

    return influence_on_penalty_json_dict[IssueDifficulty.HARD.value]


def convert_review_result_to_json_dict(review_result: ReviewResult, config: ApplicationConfig) -> Dict:
    issues = review_result.issues
    issues.sort(key=lambda issue: issue.line_no)

    quality_with_penalty = _get_quality_with_penalty(review_result)

    output_json = {}

    if isinstance(review_result, FileReviewResult):
        output_json[OutputJsonFields.FILE_NAME.value] = str(review_result.file_path)

    output_json[OutputJsonFields.QUALITY.value] = get_quality_json_dict(quality_with_penalty, config)
    output_json[OutputJsonFields.ISSUES.value] = []

    for issue in issues:
        json_issue = convert_issue_to_json(issue, config)

        json_issue[OutputJsonFields.INFLUENCE_ON_PENALTY.value] = get_influence_on_penalty_json_dict(
            issue.origin_class,
            review_result,
            config,
        )

        output_json[OutputJsonFields.ISSUES.value].append(json_issue)

    return output_json


def print_review_result_as_json(review_result: GeneralReviewResult, config: ApplicationConfig) -> None:
    print(json.dumps(convert_review_result_to_json_dict(review_result, config)))


def print_review_result_as_multi_file_json(review_result: GeneralReviewResult, config: ApplicationConfig) -> None:
    review_result.file_review_results.sort(key=lambda result: result.file_path)

    file_review_result_jsons = []
    for file_review_result in review_result.file_review_results:
        file_review_result_jsons.append(convert_review_result_to_json_dict(file_review_result, config))

    quality_with_penalty = _get_quality_with_penalty(review_result)

    output_json = {
        OutputJsonFields.QUALITY.value: get_quality_json_dict(quality_with_penalty, config),
        OutputJsonFields.FILE_REVIEW_RESULTS.value: file_review_result_jsons,
    }

    print(json.dumps(output_json))


@unique
class OutputJsonFields(Enum):
    QUALITY = 'quality'
    ISSUES = 'issues'
    FILE_REVIEW_RESULTS = 'file_review_results'
    FILE_NAME = 'file_name'

    CODE = 'code'
    TEXT = 'text'
    LINE = 'line'
    LINE_NUMBER = 'line_number'
    COLUMN_NUMBER = 'column_number'
    CATEGORY = 'category'
    INFLUENCE_ON_PENALTY = 'influence_on_penalty'
    DIFFICULTY = 'difficulty'


def convert_issue_to_json(issue: BaseIssue, config: ApplicationConfig) -> Dict[str, Any]:
    line_text = get_file_line(issue.file_path, issue.line_no)

    issue_type = issue.type
    if not config.with_all_categories:
        issue_type = issue_type.to_main_type()

    return {
        OutputJsonFields.CODE.value: issue.origin_class,
        OutputJsonFields.TEXT.value: issue.description,
        OutputJsonFields.LINE.value: line_text,
        OutputJsonFields.LINE_NUMBER.value: issue.line_no,
        OutputJsonFields.COLUMN_NUMBER.value: issue.column_no,
        OutputJsonFields.CATEGORY.value: issue_type.value,
        OutputJsonFields.DIFFICULTY.value: issue.difficulty.value,
    }


# It works only for old json format
def convert_json_to_issues(issues_json: List[dict]) -> List[PenaltyIssue]:
    issues = []
    for issue in issues_json:
        issues.append(
            PenaltyIssue(
                origin_class=issue[OutputJsonFields.CODE.value],
                description=issue[OutputJsonFields.TEXT.value],
                line_no=int(issue[OutputJsonFields.LINE_NUMBER.value]),
                column_no=int(issue[OutputJsonFields.COLUMN_NUMBER.value]),
                type=IssueType(issue[OutputJsonFields.CATEGORY.value]),

                file_path=Path(),
                inspector_type=InspectorType.UNDEFINED,
                influence_on_penalty=issue.get(OutputJsonFields.INFLUENCE_ON_PENALTY.value, 0),
                difficulty=IssueDifficulty(issue.get(OutputJsonFields.DIFFICULTY.value, IssueDifficulty.HARD.value)),
            ),
        )
    return issues
