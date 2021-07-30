import argparse
import json
import logging
import sys
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List, Optional

sys.path.append('')
sys.path.append('../../..')

import pandas as pd
from pandarallel import pandarallel
from src.python.evaluation.common.pandas_util import get_solutions_df_by_file_path, write_df_to_file
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.issues_statistics.common.raw_issue_encoder_decoder import RawIssueDecoder
from src.python.evaluation.issues_statistics.get_raw_issues import RAW_ISSUES
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import Extension, get_parent_folder, get_total_code_lines_from_code
from src.python.review.common.language import Language
from src.python.review.inspectors.issue import BaseIssue, ISSUE_TYPE_TO_CLASS, IssueType, Measurable
from src.python.review.quality.rules.code_style_scoring import CodeStyleRule
from src.python.review.quality.rules.line_len_scoring import LineLengthRule
from src.python.review.reviewers.utils.code_statistics import get_code_style_lines

ID = ColumnName.ID.value
LANG = ColumnName.LANG.value
CODE = ColumnName.CODE.value

CODE_STYLE_LINES = f'{IssueType.CODE_STYLE.value}_lines'
CODE_STYLE_RATIO = f'{IssueType.CODE_STYLE.value}_ratio'
LINE_LEN_NUMBER = f'{IssueType.LINE_LEN.value}_number'
LINE_LEN_RATIO = f'{IssueType.LINE_LEN.value}_ratio'
TOTAL_LINES = 'total_lines'
VALUE = 'value'

OUTPUT_DF_NAME = 'stats'
DEFAULT_OUTPUT_FOLDER_NAME = 'raw_issues_statistics'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'solutions_with_raw_issues',
        type=lambda value: Path(value).absolute(),
        help=f'Local XLSX-file or CSV-file path. Your file must include column-names: '
             f'"{ID}", "{CODE}", "{LANG}", and "{RAW_ISSUES}".',
    )

    parser.add_argument(
        '-o', '--output',
        type=lambda value: Path(value).absolute(),
        help='Path to the folder where datasets with statistics will be saved. '
             'If not specified, the datasets will be saved in the folder next to the original one.',
    )


def _convert_language_code_to_language(fragment_id: str, language_code: str) -> str:
    language_version = LanguageVersion.from_value(language_code)

    if language_version is None:
        logger.warning(f'{fragment_id}: it was not possible to determine the language version from "{language_code}".')
        return language_code

    language = Language.from_language_version(language_version)

    if language == Language.UNKNOWN:
        logger.warning(f'{fragment_id}: it was not possible to determine the language from "{language_version}".')
        return language_code

    return language.value


def _extract_stats_from_issues(row: pd.Series) -> pd.Series:
    logger.info(f'{row[ID]}: extracting stats.')

    if row.isnull().values.any():
        logger.warning(f'{row[ID]}: the row contains Null. ')

    try:
        issues: List[BaseIssue] = json.loads(row[RAW_ISSUES], cls=RawIssueDecoder)
    except (JSONDecodeError, TypeError):
        logger.warning(f'{row[ID]}: failed to decode issues.')
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

    row[LANG] = _convert_language_code_to_language(row[ID], row[LANG])

    logger.info(f'{row[ID]}: extraction of statistics is complete.')

    return row


def _convert_ratio_to_int(ratio: float):
    """
    Round the ratio to 2 decimal places, multiply by 100, and take the integer part.
    """
    return int((round(ratio, 2) * 100))


def _group_stats_by_lang(df_with_stats: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    logger.info('The grouping of statistics by language has started.')

    result = {}

    df_grouped_by_lang = df_with_stats.groupby(LANG)
    for lang in df_grouped_by_lang.groups:
        logger.info(f'"{lang}" statistics grouping started.')

        lang_group = df_grouped_by_lang.get_group(lang)

        columns_with_stats = []

        for issue_type, issue_class in ISSUE_TYPE_TO_CLASS.items():
            column = lang_group[issue_type.value]
            if issubclass(issue_class, Measurable):
                column = column.explode()
            columns_with_stats.append(column.value_counts())

        columns_with_stats.append(lang_group[TOTAL_LINES].value_counts())

        line_len_ratio_column = lang_group.apply(
            lambda row: LineLengthRule.get_ratio(row[LINE_LEN_NUMBER], row[TOTAL_LINES]),
            axis=1,
        )
        line_len_ratio_column = line_len_ratio_column.apply(_convert_ratio_to_int)
        line_len_ratio_column.name = LINE_LEN_RATIO
        columns_with_stats.append(line_len_ratio_column.value_counts())

        code_style_ratio_column = lang_group.apply(
            lambda row: CodeStyleRule.get_ratio(
                row[CODE_STYLE_LINES], row[TOTAL_LINES], Language.from_value(str(lang), default=Language.UNKNOWN),
            ),
            axis=1,
        )
        code_style_ratio_column = code_style_ratio_column.apply(_convert_ratio_to_int)
        code_style_ratio_column.name = CODE_STYLE_RATIO
        columns_with_stats.append(code_style_ratio_column.value_counts())

        stats = pd.concat(columns_with_stats, axis=1).fillna(0).astype(int)

        # Put values in a separate column
        stats.index.name = VALUE
        stats.reset_index(inplace=True)

        result[str(lang)] = stats
        logger.info(f'"{lang}" statistics grouping finished.')

    logger.info('The grouping of statistics by language has finished.')

    return result


def inspect_raw_issues(solutions_with_raw_issues: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    pandarallel.initialize()

    solutions_with_raw_issues = solutions_with_raw_issues.parallel_apply(_extract_stats_from_issues, axis=1)

    return _group_stats_by_lang(solutions_with_raw_issues)


def _get_output_folder(solutions_file_path: Path, output_folder: Optional[Path]):
    if output_folder is not None:
        return output_folder

    return get_parent_folder(solutions_file_path) / DEFAULT_OUTPUT_FOLDER_NAME


def _save_stats(stats_by_lang: Dict[str, pd.DataFrame], solutions_file_path: Path, output_path: Optional[Path]) -> None:
    output_folder = _get_output_folder(solutions_file_path, output_path)
    output_extension = Extension.get_extension_from_file(str(solutions_file_path))

    logger.info(f'Saving statistics to a folder: {output_folder}.')

    for lang, stats in stats_by_lang.items():
        lang_folder = output_folder / lang
        lang_folder.mkdir(parents=True, exist_ok=True)
        write_df_to_file(stats, lang_folder / f'{OUTPUT_DF_NAME}{output_extension.value}', output_extension)

    logger.info('Saving statistics is complete.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    solutions_with_raw_issues = get_solutions_df_by_file_path(args.solutions_with_raw_issues)

    stats_by_lang = inspect_raw_issues(solutions_with_raw_issues)

    _save_stats(stats_by_lang, args.solutions_with_raw_issues, args.output)
