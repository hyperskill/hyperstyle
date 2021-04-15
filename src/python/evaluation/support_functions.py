import os
from pathlib import Path
from typing import NoReturn, Union

from openpyxl import load_workbook


def create_folder(directory: Union[str, Path]) -> NoReturn:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        pass


def remove_sheet(path: str, name: str) -> NoReturn:
    file = load_workbook(path)
    try:
        file.remove(file[name])
        file.save(path)
    except KeyError:
        pass
