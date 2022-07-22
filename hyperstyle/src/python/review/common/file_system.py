import linecache
import logging
import os
import tempfile
from contextlib import contextmanager
from enum import Enum, unique
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


@unique
class FileSystemItem(Enum):
    PATH = 0
    SUBDIR = 1
    FILE = 2


@unique
class Encoding(Enum):
    ISO_ENCODING = 'ISO-8859-1'
    UTF_ENCODING = 'utf-8'


# Make sure all extensions (except an empty one) have a dot
@unique
class Extension(Enum):
    EMPTY = ''
    PY = '.py'
    JAVA = '.java'
    KT = '.kt'
    JS = '.js'
    KTS = '.kts'

    # Not empty extensions are returned with a dot, for example, '.txt'
    # If file has no extensions, an empty one ('') is returned
    @classmethod
    def from_file(cls, file: Union[Path, str]) -> Optional['Extension']:
        try:
            return Extension(get_extension_from_file(file))
        except ValueError:
            return None


def get_extension_from_file(file: Union[Path, str]) -> str:
    return os.path.splitext(file)[1]


ItemCondition = Callable[[str], bool]


def all_items_condition(name: str) -> bool:
    return True


# To get all files or subdirs (depends on the last parameter) from root that match item_condition
# Note that all subdirs or files already contain the full path for them
def get_all_file_system_items(
        root: Path,
        item_condition: ItemCondition = all_items_condition,
        item_type: FileSystemItem = FileSystemItem.FILE,
        without_subdirs: bool = False,
) -> List[Path]:
    if not root.is_dir():
        raise ValueError(f'The {root} is not a directory')

    items = []
    for fs_tuple in os.walk(root):
        for item in fs_tuple[item_type.value]:
            if item_condition(item):
                items.append(Path(os.path.join(fs_tuple[FileSystemItem.PATH.value], item)))

        if without_subdirs:
            break

    return items


# TODO: Need testing
@contextmanager
def new_temp_dir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def new_temp_file(suffix: Extension = Extension.EMPTY) -> Tuple[str, str]:
    yield tempfile.mkstemp(suffix=suffix.value)


def get_file_line(path: Path, line_number: int):
    return linecache.getline(
        str(path),
        line_number,
    ).strip()


def get_content_from_file(file_path: Path, encoding: str = Encoding.ISO_ENCODING.value,
                          to_strip_nl: bool = True) -> str:
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
        return content if not to_strip_nl else content.rstrip('\n')


# Before using it, check that there are no line breaks in the string
def __is_line_empty(line: str) -> bool:
    return len(line.strip()) == 0


def __is_comment(line: str) -> bool:
    return line.strip().startswith(('#', '//'))


def get_total_code_lines_from_file(path: Path) -> int:
    code = get_content_from_file(path, to_strip_nl=False)
    return get_total_code_lines_from_code(code)


def get_total_code_lines_from_code(code: str) -> int:
    lines = code.splitlines()
    return len(list(filter(lambda line: not __is_line_empty(line) and not __is_comment(line), lines)))


def check_set_up_env_variable(variable_name: str) -> bool:
    if variable_name not in os.environ:
        logger.warning(f'{variable_name} was not set up!')
        return False
    return True
