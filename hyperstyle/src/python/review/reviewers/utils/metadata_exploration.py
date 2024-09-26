from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from hyperstyle.src.python.review.common.file_system import get_all_file_system_items, get_extension_from_file
from hyperstyle.src.python.review.common.language import guess_file_language, Language

if TYPE_CHECKING:
    from pathlib import Path


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
    inner_files: list[FileMetadata]

    @property
    def languages(self) -> set[Language]:
        return {file_metadata.language for file_metadata in self.inner_files}

    @property
    def size_bytes(self) -> int:
        return sum(file_metadata.size_bytes for file_metadata in self.inner_files)

    @property
    def extension_to_files(self) -> dict[str, list[FileMetadata]]:
        extension_to_files = defaultdict(list)
        for file in self.inner_files:
            extension_to_files[get_extension_from_file(file.path)].append(file)
        return extension_to_files

    @property
    def language_to_files(self) -> dict[Language, list[Path]]:
        language_to_files = defaultdict(list)
        for file in self.inner_files:
            language_to_files[file.language].append(file.path)
        return language_to_files

    @property
    def extensions(self) -> set[str]:
        return set(self.extension_to_files)


@dataclass
class InMemoryMetadata:
    code: str


Metadata = FileMetadata | ProjectMetadata | InMemoryMetadata


def explore_file(path: Path) -> FileMetadata:
    if not path.exists() or not path.is_file():
        msg = f"The file {path} does not exist or is not a file"
        raise ValueError(msg)

    stat = path.stat()
    language = guess_file_language(path)
    return FileMetadata(path, language, stat.st_size)


def explore_project(path: Path) -> ProjectMetadata:
    if not path.exists() or not path.is_dir():
        msg = f"The file {path} does not exist or is not a directory"
        raise ValueError(msg)

    inner_files = [explore_file(file_path) for file_path in get_all_file_system_items(path)]

    return ProjectMetadata(path, inner_files)


def explore_in_memory_metadata(code: str) -> InMemoryMetadata:
    return InMemoryMetadata(code)
