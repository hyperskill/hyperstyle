import linecache
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Union


# TODO: Need testing
def get_all_file_paths_in_dir(dir_path: Path) -> List[Path]:
    if not dir_path.is_dir():
        raise ValueError

    file_paths = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_paths.append(Path(root) / file)

    return file_paths


# TODO: Need testing
def get_all_subdirs(dir_path: Path) -> List[Path]:
    subdirs = {dir_path}
    for file_path in get_all_file_paths_in_dir(dir_path):
        subdirs.add(file_path.parent)

    return list(subdirs)


# TODO: Need testing
@contextmanager
def new_temp_dir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def write(path: Union[str, Path], text: str):
    """
    Write text to file. Create all parents if necessary
    :param path:
    :param text:
    :return:
    """
    path = Path(path)

    os.makedirs(path.parent, exist_ok=True)
    with open(str(path), 'w') as file:
        file.write(text)


def get_file_line(path: Path, line_number: int):
    return linecache.getline(
        str(path),
        line_number
    ).strip()
