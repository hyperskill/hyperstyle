import linecache
import os
import tempfile
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import List, Union, Callable


class FileSystemItem(Enum):
    PATH = 0
    SUBDIR = 1
    FILE = 2


class Encoding(Enum):
    ISO_ENCODING = 'ISO-8859-1'
    UTF_ENCODING = 'utf-8'


# Make sure all extensions (except an empty one) have a dot
class Extension(Enum):
    EMPTY = ''
    PY = '.py'
    JAVA = '.java'
    KT = '.kt'
    JS = '.js'
    KTS = '.kts'


ItemCondition = Callable[[str], bool]


def all_items_condition(name: str) -> bool:
    return True


# To get all files or subdirs (depends on the last parameter) from root that match item_condition
# Note that all subdirs or files already contain the full path for them
def get_all_file_system_items(root: Path, item_condition: ItemCondition = all_items_condition,
                              item_type: FileSystemItem = FileSystemItem.FILE) -> List[Path]:
    if not root.is_dir():
        raise ValueError(f'The {root} is not a directory')

    items = []
    for fs_tuple in os.walk(root):
        for item in fs_tuple[item_type.value]:
            if item_condition(item):
                items.append(Path(os.path.join(fs_tuple[FileSystemItem.PATH.value], item)))
    return items


# TODO: Need testing
@contextmanager
def new_temp_dir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


# File should contain the full path and its extension.
# Create all parents if necessary
def create_file(file_path: Union[str, Path], content: str):
    file_path = Path(file_path)

    create_directory(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(content)


def create_directory(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)


def get_file_line(path: Path, line_number: int):
    return linecache.getline(
        str(path),
        line_number
    ).strip()


def get_content_from_file(file_path: Path, encoding: str = Encoding.ISO_ENCODING.value,
                          to_strip_nl: bool = True) -> str:
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
        return content if not to_strip_nl else content.rstrip('\n')


# Not empty extensions are returned with a dot, for example, '.txt'
# If file has no extensions, an empty one ('') is returned
def get_extension_from_file(file: Path) -> Extension:
    return Extension(os.path.splitext(file)[1])
