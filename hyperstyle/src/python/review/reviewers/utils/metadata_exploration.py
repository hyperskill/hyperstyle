import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Union

from hyperstyle.src.python.review.common.file_system import get_all_file_system_items, get_extension_from_file
from hyperstyle.src.python.review.common.language import guess_file_language, Language


@dataclass
class FileMetadata:
    path: Path
    language: Language
    size_bytes: int

    @property
    def extension(self) -> str:
        return get_extension_from_file(self.path)


@dataclass
class ProjectMetadata:
    path: Path
    inner_files: List[FileMetadata]

    @property
    def languages(self) -> Set[Language]:
        languages = set()
        for file_metadata in self.inner_files:
            languages.add(file_metadata.language)
        return languages

    @property
    def size_bytes(self) -> int:
        return sum(map(lambda file_metadata: file_metadata.size_bytes, self.inner_files))

    @property
    def extension_to_files(self) -> Dict[str, List[FileMetadata]]:
        extension_to_files = defaultdict(list)
        for file in self.inner_files:
            extension_to_files[get_extension_from_file(file.path)].append(file)
        return extension_to_files

    @property
    def language_to_files(self) -> Dict[Language, List[FileMetadata]]:
        language_to_files = defaultdict(list)
        for file in self.inner_files:
            language_to_files[file.language].append(file)
        return language_to_files

    @property
    def extensions(self) -> Set[str]:
        return set(self.extension_to_files)


Metadata = Union[FileMetadata, ProjectMetadata]


def explore_file(path: Path) -> FileMetadata:
    if not path.exists() or not path.is_file():
        raise ValueError(f'The file {path} does not exist or is not a file')

    stat = os.stat(path)
    language = guess_file_language(path)
    return FileMetadata(path, language, stat.st_size)


def explore_project(path: Path) -> ProjectMetadata:
    if not path.exists() or not path.is_dir():
        raise ValueError(f'The file {path} does not exist or is not a directory')

    inner_files = []
    for file_path in get_all_file_system_items(path):
        inner_files.append(explore_file(file_path))

    return ProjectMetadata(path, inner_files)
