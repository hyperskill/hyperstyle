from __future__ import annotations

import json
from typing import NamedTuple

import pytest

from hyperstyle.src.python.review.application_config import ApplicationConfig
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from hyperstyle.src.python.review.quality.model import QualityType
from hyperstyle.src.python.review.reviewers.exceptions import PathNotExistsError
from hyperstyle.src.python.review.reviewers.perform_review import (
    OutputFormat,
    perform_and_print_review,
)
from test.python.inspectors import PYTHON_DATA_FOLDER


class Args(NamedTuple):
    path: str
    allow_duplicates: bool
    disable: list[str]
    format: str
    handler: str


@pytest.fixture
def config() -> ApplicationConfig:
    return ApplicationConfig(
        disabled_inspectors={InspectorType.IJ_PYTHON},
        allow_duplicates=False,
        n_cpu=1,
        inspectors_config={"n_cpu": 1},
        with_all_categories=False,
    )


def test_run_code_review_when_no_issues(capsys, config) -> None:
    file_path = PYTHON_DATA_FOLDER / "case1_simple_valid_program.py"
    exit_code = perform_and_print_review(file_path, OutputFormat.JSON, config)
    assert exit_code == 0

    captured = capsys.readouterr()
    review_result_json = json.loads(captured.out)

    quality = review_result_json["quality"]
    assert quality
    assert quality["code"] == QualityType.EXCELLENT.value
    assert quality["text"]

    assert len(review_result_json["issues"]) == 0


def test_run_code_review_when_issues_found(capsys, config) -> None:
    file_path = PYTHON_DATA_FOLDER / "case0_spaces.py"
    exit_code = perform_and_print_review(file_path, OutputFormat.JSON, config)

    assert exit_code > 0

    captured = capsys.readouterr()
    review_result_json = json.loads(captured.out)

    assert review_result_json["quality"]
    assert review_result_json["quality"]["code"]
    assert review_result_json["quality"]["text"]

    found_issues = review_result_json["issues"]
    assert len(found_issues) > 0

    for issue in found_issues:
        assert issue["code"]
        assert issue["text"]
        assert issue["line"]
        assert issue["line_number"]
        assert issue["column_number"] > 0
        assert issue["category"]


def test_run_code_review_when_unknown_file(config) -> None:
    file_path = PYTHON_DATA_FOLDER / "case_unknown_file.py"
    with pytest.raises(PathNotExistsError):
        _ = perform_and_print_review(file_path, OutputFormat.JSON, config)
