from test.python.inspectors import ESLINT_DATA_FOLDER, JS_DATA_FOLDER
from test.python.inspectors.conftest import use_file_metadata

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.tips import get_cyclomatic_complexity_tip
from hyperstyle.src.python.review.inspectors.eslint.eslint import ESLintInspector
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues

FILE_NAMES_AND_N_ISSUES = [
    ('case0_no_issues.js', 0),
    ('case1_with_issues.js', 7),
    ('case2_semi_node_and_unused.js', 5),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = ESLintInspector()

    path_to_file = JS_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})
        issues = filter_low_measure_issues(issues, Language.JS)

    assert len(issues) == n_issues


MEASURE_TEST_DATA = [
    ('complexity', 13),
]


@pytest.mark.parametrize(('origin_class', 'expected_measure'), MEASURE_TEST_DATA)
def test_measure_parse(origin_class: str, expected_measure: int):
    inspector = ESLintInspector()

    path_to_file = ESLINT_DATA_FOLDER / 'issues' / f"{origin_class.replace('-', '_')}.js"
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.measure() == expected_measure


NEW_DESCRIPTION_TEST_DATA = [
    ('complexity', get_cyclomatic_complexity_tip().format(13)),
]


@pytest.mark.parametrize(('origin_class', 'expected_description'), NEW_DESCRIPTION_TEST_DATA)
def test_new_issue_description(origin_class: str, expected_description: str):
    inspector = ESLintInspector()

    path_to_file = ESLINT_DATA_FOLDER / 'issues' / f"{origin_class.replace('-', '_')}.js"
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.description == expected_description
