from enum import Enum, unique
from typing import List


@unique
class InspectorType(Enum):
    # Python language
    PYLINT = 'PYLINT'
    PYTHON_AST = 'PYTHON_AST'
    FLAKE8 = 'FLAKE8'

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

    @classmethod
    def available_values(cls) -> List[str]:
        return [
            # Python language
            InspectorType.PYLINT.value,
            InspectorType.FLAKE8.value,
            InspectorType.PYTHON_AST.value,

            # Java language
            InspectorType.PMD.value,
            InspectorType.CHECKSTYLE.value,

            # Kotlin language
            InspectorType.DETEKT.value,

            # JavaScript language
            InspectorType.ESLINT.value,
        ]
