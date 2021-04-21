from enum import Enum
from typing import List

from src.python.review.application_config import LanguageVersion


class EvaluationProcessNames(Enum):
    CODE = "code"
    LANG = "lang"
    LANGUAGE = "language"
    GRADE = "grade"
    TRACEBACK = "traceback"
    RESULTS = "results"
    RESULTS_EXT = "results.xlsx"

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls.__members__.values()]


script_structure_rule = ("Please, make sure your XLSX-file matches following script standards: \n"
                         "1. Your XLSX-file should have 2 obligatory columns named:"
                         f"'{EvaluationProcessNames.CODE.value}' & '{EvaluationProcessNames.LANG.value}'. \n"
                         f"'{EvaluationProcessNames.CODE.value}' column -- relates to the code-sample. \n"
                         f"'{EvaluationProcessNames.LANG.value}' column -- relates to the language of a "
                         "particular code-sample. \n"
                         "2. Your code samples should belong to the one of the supported languages. \n"
                         "Supported languages are: Java, Kotlin, Python. \n"
                         f"3. Check that '{EvaluationProcessNames.LANG.value}' column cells are filled with "
                         "acceptable language-names: \n"
                         f"Acceptable language-names are: {LanguageVersion.PYTHON_3.value}, "
                         f"{LanguageVersion.JAVA_8.value} ,"
                         f"{LanguageVersion.JAVA_11.value} and {LanguageVersion.KOTLIN.value}.")
