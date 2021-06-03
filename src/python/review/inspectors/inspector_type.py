from enum import Enum, unique
from typing import List


@unique
class InspectorType(Enum):
    # Python language
    PYLINT = 'PYLINT'
    PYTHON_AST = 'PYTHON_AST'
    FLAKE8 = 'FLAKE8'
    RADON = 'RADON'

    # Java language
    PMD = 'PMD'
    CHECKSTYLE = 'CHECKSTYLE'
    SPOTBUGS = 'SPOTBUGS'
    SPRINGLINT = 'SPRINGLINT'

    # Kotlin language
    DETEKT = 'DETEKT'
    INTELLIJ = 'INTELLIJ'

    # JavaScript language
    ESLINT = 'ESLINT'

    UNDEFINED = 'UNDEFINED'

    @classmethod
    def available_values(cls) -> List[str]:
        return [
            # Python language
            cls.PYLINT.value,
            cls.FLAKE8.value,
            cls.PYTHON_AST.value,
            cls.RADON.value,

            # Java language
            cls.PMD.value,
            cls.CHECKSTYLE.value,

            # Kotlin language
            cls.DETEKT.value,

            # JavaScript language
            cls.ESLINT.value,
        ]
