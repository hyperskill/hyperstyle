from enum import Enum, unique
from pathlib import Path
from typing import List


@unique
class Language(Enum):
    JAVA = 'JAVA'
    PYTHON = 'PYTHON'
    KOTLIN = 'KOTLIN'
    JS = 'JAVASCRIPT'
    UNKNOWN = 'UNKNOWN'


EXTENSION_TO_LANGUAGE = {
    '.java': Language.JAVA,
    '.py': Language.PYTHON,
    '.kt': Language.KOTLIN,
    '.kts': Language.KOTLIN,
    '.js': Language.JS,
}


def guess_file_language(file_path: Path) -> Language:
    return EXTENSION_TO_LANGUAGE.get(file_path.suffix, Language.UNKNOWN)


def filter_paths(file_paths: List[Path], language: Language) -> List[Path]:
    result = []
    for path in file_paths:
        if guess_file_language(path) == language:
            result.append(path)
    return result
