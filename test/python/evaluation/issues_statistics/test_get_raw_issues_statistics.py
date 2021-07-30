from pathlib import Path
from test.python.common_util import equal_df
from test.python.evaluation.issues_statistics import (
    GET_RAW_ISSUES_STATISTICS_TARGET_FILES_FOLDER,
    GET_RAW_ISSUES_STATISTICS_TEST_FILES_FOLDER,
)
from typing import Optional

import pandas as pd
import pytest
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path
from src.python.evaluation.issues_statistics.get_raw_issues_statistics import (
    _convert_language_code_to_language,
    _get_output_folder,
    DEFAULT_OUTPUT_FOLDER_NAME,
    inspect_raw_issues,
)
from src.python.review.common.language import Language

DF_PARENT_FOLDER_NAME = 'parent_folder'
DF_NAME = 'input_df'
DF_PATH = Path(DF_PARENT_FOLDER_NAME) / DF_NAME
DEFAULT_OUTPUT_PATH = Path(DF_PARENT_FOLDER_NAME) / DEFAULT_OUTPUT_FOLDER_NAME

NEW_FOLDER = 'new_folder'

GET_OUTPUT_FOLDER_PATH_TEST_DATA = [
    (DF_PATH, None, DEFAULT_OUTPUT_PATH),
    (DF_PATH, Path(NEW_FOLDER), Path(NEW_FOLDER)),
]


@pytest.mark.parametrize(
    ('solutions_file_path', 'output_folder', 'expected_output_folder'),
    GET_OUTPUT_FOLDER_PATH_TEST_DATA,
)
def test_get_output_folder(solutions_file_path: Path, output_folder: Optional[Path], expected_output_folder: Path):
    actual_output_folder = _get_output_folder(solutions_file_path, output_folder)
    assert actual_output_folder == expected_output_folder


CONVERT_LANGUAGE_CODE_TO_LANGUAGE_TEST_DATA = [
    ('java7', 'JAVA'),
    ('java8', 'JAVA'),
    ('java9', 'JAVA'),
    ('java11', 'JAVA'),
    ('java15', 'JAVA'),
    ('python3', 'PYTHON'),
    ('kotlin', 'KOTLIN'),
    ('javascript', 'JAVASCRIPT'),
    ('some_weird_lang', 'some_weird_lang'),
]


@pytest.mark.parametrize(('language_code', 'expected_language'), CONVERT_LANGUAGE_CODE_TO_LANGUAGE_TEST_DATA)
def test_convert_language_code_to_language(language_code: str, expected_language: str):
    actual_language = _convert_language_code_to_language(fragment_id='0', language_code=language_code)
    assert actual_language == expected_language


INSPECT_SOLUTIONS_TEST_DATA = [
    (
        'test_df_with_null.csv',
        'target_df_with_null.csv',
        Language.PYTHON.value,
    ),
    (
        'test_df_with_empty_raw_issues.csv',
        'target_df_with_empty_raw_issues.csv',
        Language.KOTLIN.value,
    ),
    (
        'test_df_with_incorrect_language.csv',
        'target_df_with_incorrect_language.csv',
        'some_weird_lang',
    ),
    (
        'test_df_single_lang.csv',
        'target_df_single_lang.csv',
        Language.JAVA.value,
    ),
    (
        'test_df_multi_lang.csv',
        'target_df_multi_lang_java.csv',
        Language.JAVA.value,
    ),
    (
        'test_df_multi_lang.csv',
        'target_df_multi_lang_js.csv',
        Language.JS.value,
    ),
    (
        'test_df_multi_lang.csv',
        'target_df_multi_lang_python.csv',
        Language.PYTHON.value,
    ),
]


@pytest.mark.parametrize(('test_file', 'target_file', 'lang'), INSPECT_SOLUTIONS_TEST_DATA)
def test_inspect_solutions(test_file: str, target_file: str, lang: str):
    test_df = get_solutions_df_by_file_path(GET_RAW_ISSUES_STATISTICS_TEST_FILES_FOLDER / test_file)
    stats = inspect_raw_issues(test_df)

    freq_stats = pd.read_csv(GET_RAW_ISSUES_STATISTICS_TARGET_FILES_FOLDER / target_file)

    assert equal_df(stats[lang], freq_stats)
