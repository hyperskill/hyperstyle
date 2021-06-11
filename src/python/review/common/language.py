from enum import Enum, unique
from pathlib import Path
from typing import List

from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import Extension, get_extension_from_file


@unique
class Language(Enum):
    JAVA = 'JAVA'
    PYTHON = 'PYTHON'
    KOTLIN = 'KOTLIN'
    JS = 'JAVASCRIPT'
    UNKNOWN = 'UNKNOWN'

    @staticmethod
    def from_language_version(language_version: LanguageVersion) -> 'Language':
        version_to_lang = {
            LanguageVersion.PYTHON_3: Language.PYTHON,
            LanguageVersion.JAVA_7: Language.JAVA,
            LanguageVersion.JAVA_8: Language.JAVA,
            LanguageVersion.JAVA_9: Language.JAVA,
            LanguageVersion.JAVA_11: Language.JAVA,
            LanguageVersion.KOTLIN: Language.KOTLIN,
        }

        return version_to_lang.get(language_version, Language.UNKNOWN)


EXTENSION_TO_LANGUAGE = {
    Extension.JAVA: Language.JAVA,
    Extension.PY: Language.PYTHON,
    Extension.KT: Language.KOTLIN,
    Extension.KTS: Language.KOTLIN,
    Extension.JS: Language.JS,
}


def guess_file_language(file_path: Path) -> Language:
    return EXTENSION_TO_LANGUAGE.get(get_extension_from_file(file_path), Language.UNKNOWN)


def filter_paths_by_language(file_paths: List[Path], language: Language) -> List[Path]:
    result = []
    for path in file_paths:
        if guess_file_language(path) == language:
            result.append(path)
    return result
