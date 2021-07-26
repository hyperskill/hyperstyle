import argparse
import json
import sys
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from pandarallel import pandarallel
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path, write_df_to_file
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.evaluation_run_tool import get_language_version
from src.python.evaluation.statistics.common.raw_issue_encoder_decoder import RawIssueDecoder
from src.python.evaluation.statistics.get_raw_issues import RAW_ISSUES
from src.python.review.common.file_system import Extension, get_parent_folder, get_total_code_lines_from_code
from src.python.review.common.language import Language
from src.python.review.inspectors.issue import BaseIssue, ISSUE_TYPE_TO_CLASS, IssueType, Measurable
from src.python.review.reviewers.utils.code_statistics import get_code_style_lines

ID = ColumnName.ID.value
LANG = ColumnName.LANG.value
CODE = ColumnName.CODE.value

CODE_STYLE_LINES = f'{IssueType.CODE_STYLE.value}_lines'
LINE_LEN_NUMBER = f'{IssueType.LINE_LEN.value}_number'
TOTAL_LINES = 'total_lines'
VALUE = 'value'

DEFAULT_OUTPUT_FOLDER_NAME = 'raw_issues_statistics'
MAIN_STATS_DF_NAME = 'main_stats'
OTHER_STATS_DF_NAME = 'other_stats'


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'solutions_with_raw_issues',
        type=lambda value: Path(value).absolute(),
        help=f'Local XLSX-file or CSV-file path. Your file must include column-names: '
             f'"{CODE}", "{LANG}", and "{RAW_ISSUES}"',
    )

    parser.add_argument(
        '-o', '--output',
        type=lambda value: Path(value).absolute(),
        help='Path where datasets with statistics will be saved. '
             'If not specified, datasets will be saved next to the original one.',
    )


def _convert_language_code_to_language(language_code: str) -> str:
    try:
        language_version = get_language_version(language_code)
    except KeyError:
        return language_code

    language = Language.from_language_version(language_version)

    if language == Language.UNKNOWN:
        return language_code

    return language.value


def _extract_stats_from_issues(row: pd.Series) -> pd.Series:
    try:
        issues: List[BaseIssue] = json.loads(row[RAW_ISSUES], cls=RawIssueDecoder)
    except (JSONDecodeError, TypeError):
        issues: List[BaseIssue] = []

    counter = Counter([issue.type for issue in issues])

    for issue_type, issue_class in ISSUE_TYPE_TO_CLASS.items():
        if issubclass(issue_class, Measurable):
            row[issue_type.value] = [issue.measure() for issue in issues if isinstance(issue, issue_class)]
        else:
            row[issue_type.value] = counter[issue_type]

    row[CODE_STYLE_LINES] = get_code_style_lines(issues)
    row[LINE_LEN_NUMBER] = counter[IssueType.LINE_LEN]
    row[TOTAL_LINES] = get_total_code_lines_from_code(row[CODE])

    row[LANG] = _convert_language_code_to_language(row[LANG])

    return row


def _is_python(language_code: str) -> bool:
    try:
        return Language(language_code) == Language.PYTHON
    except ValueError:
        return False


def _get_stats_by_lang(df_with_stats: pd.DataFrame) -> Dict[str, Tuple[pd.DataFrame, pd.DataFrame]]:
    result = {}

    df_grouped_by_lang = df_with_stats.groupby(LANG)
    for lang in df_grouped_by_lang.groups:
        lang_group = df_grouped_by_lang.get_group(lang)

        columns_with_stats = []

        # ---- Frequency statistics ----
        for issue_type, issue_class in ISSUE_TYPE_TO_CLASS.items():
            column = lang_group[issue_type.value]
            if issubclass(issue_class, Measurable):
                column = column.explode()
            columns_with_stats.append(column.value_counts())

        columns_with_stats.append(lang_group[TOTAL_LINES].value_counts())

        freq_stats = pd.concat(columns_with_stats, axis=1).fillna(0)

        # Fill in the intermediate values that are not occurred with zeros
        min_value, max_value = freq_stats.index.min(), freq_stats.index.max()
        freq_stats = freq_stats.reindex(range(min_value, max_value + 1), fill_value=0).astype(int)

        # Put the values in a separate column
        freq_stats.index.name = VALUE
        freq_stats.reset_index(inplace=True)

        columns_with_stats.clear()

        # ---- Ratio statistics ----

        # Calculate line len ratio according to LineLengthRule
        line_len_ratio_column = lang_group[LINE_LEN_NUMBER] / lang_group[TOTAL_LINES].apply(lambda elem: max(1, elem))
        line_len_ratio_column.name = IssueType.LINE_LEN.value
        columns_with_stats.append(line_len_ratio_column)

        # Calculate code style ratio according to CodeStyleRule
        if _is_python(str(lang)):
            code_style_ratio_column = lang_group[CODE_STYLE_LINES] / lang_group[TOTAL_LINES].apply(
                lambda total_lines: max(1, total_lines),
            )
        else:
            code_style_ratio_column = lang_group[CODE_STYLE_LINES] / lang_group[TOTAL_LINES].apply(
                lambda total_lines: max(1, total_lines - 4),
            )

        code_style_ratio_column.name = IssueType.CODE_STYLE.value
        columns_with_stats.append(code_style_ratio_column)

        ratio_stats = pd.concat(columns_with_stats, axis=1)

        result[str(lang)] = (freq_stats, ratio_stats)

    return result


def inspect_solutions(solutions_with_raw_issues: pd.DataFrame) -> Dict[str, Tuple[pd.DataFrame, pd.DataFrame]]:
    pandarallel.initialize()

    solutions_with_raw_issues = solutions_with_raw_issues.parallel_apply(_extract_stats_from_issues, axis=1)

    return _get_stats_by_lang(solutions_with_raw_issues)


def _get_output_folder(solutions_file_path: Path, output_folder: Optional[Path]):
    if output_folder is not None:
        return output_folder

    return get_parent_folder(solutions_file_path) / DEFAULT_OUTPUT_FOLDER_NAME


def _save_stats(
    stats_by_lang: Dict[str, Tuple[pd.DataFrame, pd.DataFrame]],
    solutions_file_path: Path,
    output_path: Optional[Path],
) -> None:
    output_folder = _get_output_folder(solutions_file_path, output_path)
    output_extension = Extension.get_extension_from_file(str(solutions_file_path))

    for lang, (main_stats, other_stats) in stats_by_lang.items():
        lang_folder = output_folder / lang
        lang_folder.mkdir(parents=True, exist_ok=True)
        write_df_to_file(main_stats, lang_folder / f'{MAIN_STATS_DF_NAME}{output_extension.value}', output_extension)
        write_df_to_file(other_stats, lang_folder / f'{OTHER_STATS_DF_NAME}{output_extension.value}', output_extension)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_with_raw_issues = get_solutions_df_by_file_path(args.solutions_with_raw_issues)

    stats_by_lang = inspect_solutions(solutions_with_raw_issues)

    _save_stats(stats_by_lang, args.solutions_with_raw_issues, args.output)
