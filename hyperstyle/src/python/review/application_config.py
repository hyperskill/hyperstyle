from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List, Optional, Set

from hyperstyle.src.python.review.common.file_system import Extension
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType


@dataclass
class ApplicationConfig:
    disabled_inspectors: Set[InspectorType]
    allow_duplicates: bool
    n_cpu: int
    inspectors_config: dict
    with_all_categories: bool
    start_line: int = 1
    end_line: Optional[int] = None
    new_format: bool = False
    history: Optional[str] = None
    group_by_difficulty: bool = False


@unique
class LanguageVersion(Enum):
    JAVA_7 = 'java7'
    JAVA_8 = 'java8'
    JAVA_9 = 'java9'
    JAVA_11 = 'java11'
    JAVA_15 = 'java15'
    JAVA_17 = 'java17'
    PYTHON_3 = 'python3'
    KOTLIN = 'kotlin'
    JS = 'javascript'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls.__members__.values()]

    @classmethod
    def language_to_extension_dict(cls) -> Dict['LanguageVersion', Extension]:
        return {
            cls.JAVA_7: Extension.JAVA,
            cls.JAVA_8: Extension.JAVA,
            cls.JAVA_9: Extension.JAVA,
            cls.JAVA_11: Extension.JAVA,
            cls.JAVA_15: Extension.JAVA,
            cls.JAVA_17: Extension.JAVA,
            cls.PYTHON_3: Extension.PY,
            cls.KOTLIN: Extension.KT,
            cls.JS: Extension.JS,
        }

    def extension_by_language(self) -> Extension:
        return self.language_to_extension_dict()[self]

    def is_java(self) -> bool:
        return (
            self == LanguageVersion.JAVA_7
            or self == LanguageVersion.JAVA_8
            or self == LanguageVersion.JAVA_9
            or self == LanguageVersion.JAVA_11
            or self == LanguageVersion.JAVA_15
            or self == LanguageVersion.JAVA_17
        )

    @classmethod
    def from_value(cls, value: str, default=None):
        try:
            return LanguageVersion(value)
        except ValueError:
            return default
