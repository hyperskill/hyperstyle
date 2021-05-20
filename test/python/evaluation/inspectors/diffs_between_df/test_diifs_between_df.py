from pathlib import Path
from test.python.evaluation import INSPECTORS_DIR_PATH

import pytest
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.common.util import ColumnName, EvaluationArgument
from src.python.evaluation.inspectors.diffs_between_df import find_diffs
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType

RESOURCES_PATH = INSPECTORS_DIR_PATH / 'diffs_between_df'

EMPTY_DIFFS = {
    ColumnName.GRADE.value: [],
    EvaluationArgument.TRACEBACK.value: {},
}

INCORRECT_GRADE_DIFFS = {
    ColumnName.GRADE.value: [1, 2],
    EvaluationArgument.TRACEBACK.value: {},
}

ISSUES = {
    BaseIssue(
        origin_class='C0305',
        description='Trailing newlines',
        line_no=15,
        column_no=1,
        type=IssueType('CODE_STYLE'),

        file_path=Path(),
        inspector_type=InspectorType.UNDEFINED,
    ), BaseIssue(
        origin_class='E211',
        description='whitespace before \'(\'',
        line_no=1,
        column_no=6,
        type=IssueType('CODE_STYLE'),

        file_path=Path(),
        inspector_type=InspectorType.UNDEFINED,
    ),
}

ISSUES_DIFFS = {
    ColumnName.GRADE.value: [],
    EvaluationArgument.TRACEBACK.value: {
        1: ISSUES,
    },
}

MIXED_DIFFS = {
    ColumnName.GRADE.value: [2, 3],
    EvaluationArgument.TRACEBACK.value: {
        1: ISSUES,
    },
}

TEST_DATA = [
    ('old_1.csv', 'new_1.csv', EMPTY_DIFFS),
    ('old_2.csv', 'new_2.csv', INCORRECT_GRADE_DIFFS),
    ('old_3.csv', 'new_3.csv', ISSUES_DIFFS),
    ('old_4.csv', 'new_4.csv', MIXED_DIFFS),
]


@pytest.mark.parametrize(('old_file', 'new_file', 'diffs'), TEST_DATA)
def test(old_file: Path, new_file: Path, diffs: dict):
    old_df = get_solutions_df_by_file_path(RESOURCES_PATH / old_file)
    new_df = get_solutions_df_by_file_path(RESOURCES_PATH / new_file)
    actual_diffs = find_diffs(old_df, new_df)
    assert actual_diffs == diffs
