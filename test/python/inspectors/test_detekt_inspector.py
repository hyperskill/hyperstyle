from test.python.inspectors import DETEKT_DATA_FOLDER, KOTLIN_DATA_FOLDER
from test.python.inspectors.conftest import use_file_metadata

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.common.tips import (
    get_bool_expr_len_tip,
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_magic_number_tip,
)
from hyperstyle.src.python.review.inspectors.detekt.detekt import DetektInspector
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues

FILE_NAMES_AND_N_ISSUES = [
    ('case0_good_program.kt', 0),
    ('case1_coffee_machine.kt', 0),
    ('case2_valid_program.kt', 0),
    ('case3_todo.kt', 0),
    ('case4_semicolons.kt', 6),
    ('case5_imports.kt', 6),
    ('case6_missing_spaces.kt', 6),
    ('case8_needless_blank_line.kt', 3),
    ('case9_braces.kt', 8),
    ('case11_bad_ident.kt', 3),
    ('case13_good_filename.kt', 0),
    ('case14_keyword_spacing.kt', 12),
    ('case15_empty_class_func.kt', 2),
    ('case16_redundant_unit.kt', 1),
    ('case18_redundant_braces.kt', 6),
    ('case20_cyclomatic_complexity.kt', 0),
    ('case21_cyclomatic_complexity_bad.kt', 2),
    ('case22_too_many_arguments.kt', 1),
    ('case23_bad_range_performance.kt', 7),
    ('case24_duplicate_when_bug.kt', 1),
    ('case25_unreachable_code.kt', 4),
    ('case26_var_could_be_val.kt', 1),
]


@pytest.mark.parametrize(('file_name', 'n_issues'), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = DetektInspector()

    path_to_file = KOTLIN_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})
        issues = filter_low_measure_issues(issues, Language.KOTLIN)

    assert len(issues) == n_issues


MEASURE_TEST_DATA = [
    ('LongMethod', 15),
    ('ComplexCondition', 4),
    ('ComplexMethod', 17),
]


@pytest.mark.parametrize(('origin_class', 'expected_measure'), MEASURE_TEST_DATA)
def test_measure_parse(origin_class: str, expected_measure: int):
    inspector = DetektInspector()

    path_to_file = DETEKT_DATA_FOLDER / 'issues' / f'{origin_class}.kt'
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.measure() == expected_measure


NEW_DESCRIPTION_TEST_DATA = [
    ('LongMethod', get_func_len_tip().format(15)),
    ('ComplexCondition', get_bool_expr_len_tip(unit_name='operands').format(4)),
    ('ComplexMethod', get_cyclomatic_complexity_tip().format(17)),
    ('MagicNumber', get_magic_number_tip(with_number_field=False)),
]


@pytest.mark.parametrize(('origin_class', 'expected_description'), NEW_DESCRIPTION_TEST_DATA)
def test_new_issue_description(origin_class: str, expected_description: str):
    inspector = DetektInspector()

    path_to_file = DETEKT_DATA_FOLDER / 'issues' / f'{origin_class}.kt'
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})

    issue = list(filter(lambda elem: elem.origin_class == origin_class, issues))[0]

    assert issue.description == expected_description
