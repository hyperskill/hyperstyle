from enum import Enum, unique


@unique
class InspectorType(Enum):
    PYLINT = 'PYLINT'
    FLAKE8 = 'FLAKE8'
    PYTHON_AST = 'PYTHON_AST'
    CHECKSTYLE = 'CHECKSTYLE'
    PMD = 'PMD'
    SPOTBUGS = 'SPOTBUGS'
    DETEKT = 'DETEKT'
    INTELLIJ = 'INTELLIJ'
    SPRINGLINT = 'SPRINGLINT'
    ESLINT = 'ESLINT'
