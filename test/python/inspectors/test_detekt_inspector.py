from test.python.inspectors import KOTLIN_DATA_FOLDER
from test.python.inspectors.conftest import use_file_metadata

import pytest
from hyperstyle.src.python.review.common.language import Language
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
