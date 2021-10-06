from test.python.inspectors import PYTHON_DATA_FOLDER
from test.python.inspectors.conftest import use_file_metadata
from textwrap import dedent

import pytest
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.issue import IssueType
from hyperstyle.src.python.review.inspectors.radon.radon import RadonInspector
from hyperstyle.src.python.review.inspectors.tips import get_maintainability_index_tip
from hyperstyle.src.python.review.reviewers.utils.issues_filter import filter_low_measure_issues


FILE_NAMES_AND_N_ISSUES = [
    ("case13_complex_logic.py", 1),
    ("case13_complex_logic_2.py", 1),
    ("case8_good_class.py", 0),
]


@pytest.mark.parametrize(("file_name", "n_issues"), FILE_NAMES_AND_N_ISSUES)
def test_file_with_issues(file_name: str, n_issues: int):
    inspector = RadonInspector()

    path_to_file = PYTHON_DATA_FOLDER / file_name
    with use_file_metadata(path_to_file) as file_metadata:
        issues = inspector.inspect(file_metadata.path, {})
        issues = filter_low_measure_issues(issues, Language.PYTHON)

        assert len(issues) == n_issues


def test_mi_parse():
    file_name = "test.py"
    output = f"""\
        {file_name} - C (4.32)
        {file_name} - B (13.7)
        {file_name} - A (70.0)
    """
    output = dedent(output)

    issues = RadonInspector.mi_parse(output)

    assert all(str(issue.file_path) == file_name for issue in issues)
    assert [issue.line_no for issue in issues] == [1, 1, 1]
    assert [issue.column_no for issue in issues] == [1, 1, 1]
    assert [issue.description for issue in issues] == [get_maintainability_index_tip()] * 3
    assert [issue.type for issue in issues] == [
        IssueType.MAINTAINABILITY,
        IssueType.MAINTAINABILITY,
        IssueType.MAINTAINABILITY,
    ]
    assert [issue.maintainability_lack for issue in issues] == [95, 86, 30]
