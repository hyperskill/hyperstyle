import logging.config
from pathlib import Path
from typing import NoReturn, Union

import pandas as pd
from openpyxl import load_workbook

logger = logging.getLogger(__name__)


def remove_sheet(workbook_path: Union[str, Path], sheet_name: str, not_exist_ok=True) -> NoReturn:
    try:
        workbook = load_workbook(workbook_path)
        workbook.remove(workbook[sheet_name])
        workbook.save(workbook_path)
    except KeyError:
        # if not_exist_ok=True – do not raise KeyError if sheet does not exist
        if not_exist_ok:
            pass
        else:
            logger.exception(f'Sheet with specified name: {sheet_name} does not exist.')


def write_dataframe_to_xlsx_sheet(xlsx_file_path: Union[str, Path], context_dataframe: pd.DataFrame,
                                  sheet_name: str, engine: str, mode='a', index=False):

    with pd.ExcelWriter(xlsx_file_path, engine=engine, mode=mode) as writer:
        context_dataframe.to_excel(writer, sheet_name=sheet_name, index=index)
