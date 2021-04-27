import json
import linecache
from pathlib import Path

from src.python.review.common.file_system import get_file_line
from src.python.review.reviewers.review_result import ReviewResult
from src.python.review.reviewers.utils.penalty import get_penalty_influence


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

    quality_with_penalty = review_result.general_quality.quality_with_penalty.value
    output_json = {'quality': {
        'code': quality_with_penalty,
        'text': f'Code quality (beta): {quality_with_penalty}',
    }, 'issues': []}

    for issue in issues:
        line_text = get_file_line(issue.file_path, issue.line_no)

        penalty_influence = 0
        quality_without_penalty = review_result.general_quality.quality_type.value
        if quality_with_penalty != quality_without_penalty:
            penalty_influence = get_penalty_influence(
                # issue penalty coefficient
                review_result.issue_class_to_penalty_coefficient.get(issue.origin_class, 0),
                # total penalty coefficient
                review_result.general_quality.penalty_coefficient,
            )

        output_json['issues'].append({
            'code': issue.origin_class,
            'text': issue.description,
            'line': line_text,
            'line_number': issue.line_no,
            'column_number': issue.column_no,
            'category': issue.type.value,
            'penalty_influence': penalty_influence,
        })

    print(json.dumps(output_json))


def print_review_result_as_multi_file_json(review_result: ReviewResult) -> None:
    file_review_result_jsons = []

    review_result.file_review_results.sort(key=lambda result: result.file_path)

    for file_review_result in review_result.file_review_results:
        quality_with_penalty = file_review_result.quality.quality_with_penalty.value
        file_review_result_json = {
            'file_name': str(file_review_result.file_path),
            'quality': {
                'code': quality_with_penalty,
                'text': f'Code quality (beta): {quality_with_penalty}',
            },
            'issues': [],
        }

        file_review_result_jsons.append(file_review_result_json)

        for issue in file_review_result.issues:
            line_text = get_file_line(issue.file_path, issue.line_no)

            penalty_influence = 0
            quality_without_penalty = review_result.general_quality.quality_type.value
            if quality_with_penalty != quality_without_penalty:
                penalty_influence = get_penalty_influence(
                    # issue penalty coefficient
                    review_result.issue_class_to_penalty_coefficient.get(issue.origin_class, 0),
                    # total penalty coefficient
                    file_review_result.quality.penalty_coefficient,
                )

            file_review_result_json['issues'].append({
                'code': issue.origin_class,
                'text': issue.description,
                'line': line_text,
                'line_number': issue.line_no,
                'column_number': issue.column_no,
                'category': issue.type.value,
                'penalty_influence': penalty_influence,
            })

    quality_with_penalty = review_result.general_quality.quality_with_penalty.value

    output_json = {
        'quality': {
            'code': quality_with_penalty,
            'text': f'Code quality (beta): {quality_with_penalty}',
        },
        'file_review_results': file_review_result_jsons,
    }

    print(json.dumps(output_json))
