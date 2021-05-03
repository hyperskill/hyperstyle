from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional, Set

from src.python.review.common.file_system import Extension
from src.python.review.inspectors.inspector_type import InspectorType


@dataclass
class ApplicationConfig:
    disabled_inspectors: Set[InspectorType]
    allow_duplicates: bool
    n_cpu: int
    inspectors_config: dict
    start_line: int = 1
    end_line: Optional[int] = None
    new_format: bool = False
    history: str = None


@unique
class LanguageVersion(Enum):
    JAVA_7 = 'java7'
    JAVA_8 = 'java8'
    JAVA_9 = 'java9'
    JAVA_11 = 'java11'
    PYTHON_3 = 'python3'
    KOTLIN = 'kotlin'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls.__members__.values()]

    @classmethod
    def language_to_extension_dict(cls) -> dict:
        return {cls.PYTHON_3.value: Extension.PY.value,
                cls.JAVA_7.value: Extension.JAVA.value,
                cls.JAVA_8.value: Extension.JAVA.value,
                cls.JAVA_9.value: Extension.JAVA.value,
                cls.JAVA_11.value: Extension.JAVA.value,
                cls.KOTLIN.value: Extension.KT.value}

    @classmethod
    def language_by_extension(cls, lang: str) -> str:
        return cls.language_to_extension_dict()[lang]
