from enum import Enum, unique
from typing import List


@unique
class InspectorType(Enum):
    # Python language
    PYLINT = 'PYLINT'
    PYTHON_AST = 'PYTHON_AST'
    FLAKE8 = 'FLAKE8'
    RADON = 'RADON'
    IJ_PYTHON = 'IJ_PYTHON'

    # Java language
    PMD = 'PMD'
    CHECKSTYLE = 'CHECKSTYLE'

    # Kotlin language
    DETEKT = 'DETEKT'
    IJ_KOTLIN = 'IJ_KOTLIN'

    # JavaScript language
    ESLINT = 'ESLINT'

    # Go language
    GOLANG_LINT = 'GOLANG_LINT'

    UNDEFINED = 'UNDEFINED'
    QODANA = 'QODANA'
    # TODO: it is used on production for java inspections, remove in the future releases
    IJ_OLD = 'INTELLIJ'

    @classmethod
    def available_values(cls) -> List[str]:
        return [
            # Python language
            cls.PYLINT.value,
            cls.FLAKE8.value,
            cls.PYTHON_AST.value,
            cls.RADON.value,
            cls.IJ_PYTHON.value,

            # Java language
            cls.PMD.value,
            cls.CHECKSTYLE.value,

            # Kotlin language
            cls.DETEKT.value,
            cls.IJ_KOTLIN.value,

            # JavaScript language
            cls.ESLINT.value,

            # Go language
            cls.GOLANG_LINT.value,

            cls.IJ_OLD.value,
        ]
