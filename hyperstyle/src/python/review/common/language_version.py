from enum import unique, Enum
from typing import List, Dict

from hyperstyle.src.python.review.common.file_system import Extension


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
    GO = 'go'

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
            cls.GO: Extension.GO,
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
