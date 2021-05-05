import json
import linecache
from pathlib import Path
from typing import Any, Dict

from src.python.review.common.file_system import get_file_line
from src.python.review.inspectors.issue import BaseIssue
from src.python.review.reviewers.review_result import ReviewResult


def print_review_result_as_text(review_result: ReviewResult,
                                path: Path) -> None:
    heading = f'\nReview of {str(path)} ({len(review_result.all_issues)} violations)'
    print(heading)

    if len(review_result.all_issues) == 0:
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

                print(f'{issue.line_no} : '
                      f'{issue.column_no} : '
                      f'{issue.type.value} : '
                      f'{issue.inspector_type.value} : '
                      f'{issue.origin_class} : '
                      f'{issue.description} : '
                      f'{line_text}: '
                      f'{issue.file_path}')
            print('-' * len(heading))
            print(file_review_result.quality)

    print('*' * len(heading))
    print('General quality:')
    print(review_result.general_quality, end='')


def print_review_result_as_json(review_result: ReviewResult) -> None:
    issues = review_result.all_issues

    issues.sort(key=lambda issue: issue.line_no)

    quality_without_penalty = review_result.general_quality.quality_type
    quality_with_penalty = review_result.general_punisher.get_quality_with_penalty(quality_without_penalty)
    output_json = {'quality': {
        'code': quality_with_penalty.value,
        'text': f'Code quality (beta): {quality_with_penalty.value}',
    }, 'issues': []}

    for issue in issues:
        influence_on_penalty = 0
        if quality_with_penalty != quality_without_penalty:
            influence_on_penalty = review_result.general_punisher.get_issue_influence_on_penalty(issue.origin_class)

        output_json['issues'].append(convert_issue_to_json(issue, influence_on_penalty))

    print(json.dumps(output_json))


def print_review_result_as_multi_file_json(review_result: ReviewResult) -> None:
    file_review_result_jsons = []

    review_result.file_review_results.sort(key=lambda result: result.file_path)

    for file_review_result in review_result.file_review_results:
        quality_without_penalty = file_review_result.quality.quality_type
        quality_with_penalty = file_review_result.punisher.get_quality_with_penalty(quality_without_penalty)
        file_review_result_json = {
            'file_name': str(file_review_result.file_path),
            'quality': {
                'code': quality_with_penalty.value,
                'text': f'Code quality (beta): {quality_with_penalty.value}',
            },
            'issues': [],
        }

        file_review_result_jsons.append(file_review_result_json)

        for issue in file_review_result.issues:
            influence_on_penalty = 0
            if quality_with_penalty != quality_without_penalty:
                influence_on_penalty = file_review_result.punisher.get_issue_influence_on_penalty(issue.origin_class)

            file_review_result_json['issues'].append(convert_issue_to_json(issue, influence_on_penalty))

    quality_without_penalty = review_result.general_quality.quality_type
    quality_with_penalty = review_result.general_punisher.get_quality_with_penalty(quality_without_penalty)

    output_json = {
        'quality': {
            'code': quality_with_penalty.value,
            'text': f'Code quality (beta): {quality_with_penalty.value}',
        },
        'file_review_results': file_review_result_jsons,
    }

    print(json.dumps(output_json))


def convert_issue_to_json(issue: BaseIssue, influence_on_penalty: int) -> Dict[str, Any]:
    line_text = get_file_line(issue.file_path, issue.line_no)

    return {
        'code': issue.origin_class,
        'text': issue.description,
        'line': line_text,
        'line_number': issue.line_no,
        'column_number': issue.column_no,
        'category': issue.type.value,
        'influence_on_penalty': influence_on_penalty,
    }
