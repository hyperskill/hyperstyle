import linecache
import os
import pickle
import re
import shutil
import tempfile
from contextlib import contextmanager
from enum import Enum, unique
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Union

import yaml


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
    XLSX = '.xlsx'
    CSV = '.csv'
    PICKLE = '.pickle'
    JSON = '.json'

    # Image extensions
    PNG = '.png'
    JPG = '.jpg'
    JPEG = '.jpeg'
    WEBP = '.webp'
    SVG = '.svg'
    PDF = '.pdf'
    EPS = '.eps'

    # Not empty extensions are returned with a dot, for example, '.txt'
    # If file has no extensions, an empty one ('') is returned
    @classmethod
    def get_extension_from_file(cls, file: str) -> 'Extension':
        return Extension(os.path.splitext(file)[1])

    @classmethod
    def get_image_extensions(cls) -> List['Extension']:
        return [
            Extension.PNG,
            Extension.JPG,
            Extension.JPEG,
            Extension.WEBP,
            Extension.SVG,
            Extension.PDF,
            Extension.EPS,
        ]


ItemCondition = Callable[[str], bool]


def all_items_condition(name: str) -> bool:
    return True


def extension_file_condition(extension: Extension) -> ItemCondition:
    def has_this_extension(name: str) -> bool:
        return get_extension_from_file(name) == extension

    return has_this_extension


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


def match_condition(regex: str) -> ItemCondition:
    def does_name_match(name: str) -> bool:
        return re.fullmatch(regex, name) is not None
    return does_name_match


def serialize_data_and_write_to_file(path: Path, data: Any) -> None:
    os.makedirs(get_parent_folder(path), exist_ok=True)
    with open(path, 'wb') as f:
        p = pickle.Pickler(f)
        p.dump(data)


def deserialize_data_from_file(path: Path) -> Any:
    with open(path, 'rb') as f:
        u = pickle.Unpickler(f)
        return u.load()


def parse_yaml(path: Union[Path, str]) -> Any:
    with open(path) as file:
        return yaml.safe_load(file)


# For getting name of the last folder or file
# For example, returns 'folder' for both 'path/data/folder' and 'path/data/folder/'
def get_name_from_path(path: Union[Path, str], with_extension: bool = True) -> str:
    head, tail = os.path.split(path)
    # Tail can be empty if '/' is at the end of the path
    file_name = tail or os.path.basename(head)
    if not with_extension:
        file_name = os.path.splitext(file_name)[0]
    elif get_extension_from_file(Path(file_name)) == Extension.EMPTY:
        raise ValueError('Cannot get file name with extension, because the passed path does not contain it')
    return file_name


def pair_in_and_out_files(in_files: List[Path], out_files: List[Path]) -> List[Tuple[Path, Path]]:
    pairs = []
    for in_file in in_files:
        out_file = Path(re.sub(r'in(?=[^in]*$)', 'out', str(in_file)))
        if out_file not in out_files:
            raise ValueError(f'List of out files does not contain a file for {in_file}')
        pairs.append((in_file, out_file))
    return pairs


# TODO: Need testing
@contextmanager
def new_temp_dir() -> Path:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def new_temp_file(suffix: Extension = Extension.EMPTY) -> Tuple[str, str]:
    yield tempfile.mkstemp(suffix=suffix.value)


# File should contain the full path and its extension.
# Create all parents if necessary
def create_file(file_path: Union[str, Path], content: str):
    file_path = Path(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w+') as f:
        f.writelines(content)
        yield Path(file_path)


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


# Not empty extensions are returned with a dot, for example, '.txt'
# If file has no extensions, an empty one ('') is returned
def get_extension_from_file(file: Union[Path, str]) -> Extension:
    return Extension(os.path.splitext(file)[1])


def get_restricted_extension(file_path: Optional[Union[str, Path]] = None,
                             available_values: List[Extension] = None) -> Extension:
    if file_path is None:
        return Extension.EMPTY
    ext = Extension.get_extension_from_file(file_path)
    if available_values is not None and ext not in available_values:
        raise ValueError(f'Invalid extension. '
                         f'Available values are: {list(map(lambda e: e.value, available_values))}.')
    return ext


def remove_slash(path: str) -> str:
    return path.rstrip('/')


def remove_directory(directory: Union[str, Path]) -> None:
    if os.path.isdir(directory):
        shutil.rmtree(directory, ignore_errors=True)


def add_slash(path: str) -> str:
    if not path.endswith('/'):
        path += '/'
    return path


def get_parent_folder(path: Union[Path, str], to_add_slash: bool = False) -> Path:
    path = remove_slash(str(path))
    parent_folder = '/'.join(path.split('/')[:-1])
    if to_add_slash:
        parent_folder = add_slash(parent_folder)
    return Path(parent_folder)


def copy_directory(source: Union[str, Path], destination: Union[str, Path], dirs_exist_ok: bool = True):
    shutil.copytree(source, destination, dirs_exist_ok=dirs_exist_ok)


def copy_file(source: Union[str, Path], destination: Union[str, Path]):
    shutil.copy(source, destination)
