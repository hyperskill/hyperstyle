from enum import Enum, unique
from typing import Set

from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import Extension


@unique
class ColumnName(Enum):
    CODE = 'code'
    LANG = 'lang'
    LANGUAGE = 'language'
    GRADE = 'grade'
    ID = 'id'
    COLUMN = 'column'
    ROW = 'row'
    OLD = 'old'
    NEW = 'new'
    IS_PUBLIC = 'is_public'
    DECREASED_GRADE = 'decreased_grade'
    PENALTY = 'penalty'
    USER = 'user'
    HISTORY = 'history'
    TIME = 'time'
    TRACEBACK = 'traceback'


@unique
class EvaluationArgument(Enum):
    TRACEBACK = 'traceback'
    RESULT_FILE_NAME = 'evaluation_results'
    RESULT_FILE_NAME_XLSX = f'{RESULT_FILE_NAME}{Extension.XLSX.value}'
    RESULT_FILE_NAME_CSV = f'{RESULT_FILE_NAME}{Extension.CSV.value}'


script_structure_rule = ('Please, make sure your XLSX-file matches following script standards: \n'
                         '1. Your XLSX-file or CSV-file should have 2 obligatory columns named:'
                         f'"{ColumnName.CODE.value}" & "{ColumnName.LANG.value}". \n'
                         f'"{ColumnName.CODE.value}" column -- relates to the code-sample. \n'
                         f'"{ColumnName.LANG.value}" column -- relates to the language of a '
                         'particular code-sample. \n'
                         '2. Your code samples should belong to the one of the supported languages. \n'
                         'Supported languages are: Java, Kotlin, Python. \n'
                         f'3. Check that "{ColumnName.LANG.value}" column cells are filled with '
                         'acceptable language-names: \n'
                         f'Acceptable language-names are: {LanguageVersion.PYTHON_3.value}, '
                         f'{LanguageVersion.JAVA_8.value} ,'
                         f'{LanguageVersion.JAVA_11.value} and {LanguageVersion.KOTLIN.value}.')


# Split string by separator
def parse_set_arg(str_arg: str, separator: str = ',') -> Set[str]:
    return set(str_arg.split(separator))
