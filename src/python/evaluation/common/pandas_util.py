import logging
from pathlib import Path
from typing import Set, Union

import pandas as pd
from src.python.evaluation.common.csv_util import write_dataframe_to_csv
from src.python.evaluation.common.util import ColumnName
from src.python.evaluation.common.xlsx_util import create_workbook, remove_sheet, write_dataframe_to_xlsx_sheet
from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import Extension, get_restricted_extension

logger = logging.getLogger(__name__)


def filter_df_by_language(df: pd.DataFrame, languages: Set[LanguageVersion],
                          column: str = ColumnName.LANG.value) -> pd.DataFrame:
    return df.loc[df[column].isin(set(map(lambda l: l.value, languages)))]


def drop_duplicates(df: pd.DataFrame, column: str = ColumnName.CODE.value) -> pd.DataFrame:
    return df.drop_duplicates(column, keep='last')


def get_solutions_df(ext: Extension, file_path: Union[str, Path]) -> pd.DataFrame:
    try:
        if ext == Extension.XLSX:
            lang_code_dataframe = pd.read_excel(file_path)
        else:
            lang_code_dataframe = pd.read_csv(file_path)
    except FileNotFoundError as e:
        logger.error('XLSX-file or CSV-file with the specified name does not exists.')
        raise e

    return lang_code_dataframe


def get_solutions_df_by_file_path(path: Path) -> pd.DataFrame:
    ext = get_restricted_extension(path, [Extension.XLSX, Extension.CSV])
    return get_solutions_df(ext, path)


def write_df_to_file(df: pd.DataFrame, output_file_path: Path, extension: Extension) -> None:
    if extension == Extension.CSV:
        write_dataframe_to_csv(output_file_path, df)
    elif extension == Extension.XLSX:
        create_workbook(output_file_path)
        write_dataframe_to_xlsx_sheet(output_file_path, df, 'inspection_results')
        # remove empty sheet that was initially created with the workbook
        remove_sheet(output_file_path, 'Sheet')
