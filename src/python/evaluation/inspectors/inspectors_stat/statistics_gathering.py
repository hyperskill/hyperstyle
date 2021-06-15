import argparse
from typing import Callable, Dict, List, Set, Tuple

from src.python.evaluation.inspectors.inspectors_stat.issues.flake8_all_issues import (
    ALL_BUGBEAR_ISSUES, ALL_BUILTINS_ISSUES, ALL_COMPREHENSIONS_ISSUES, ALL_FORMAT_STRING_ISSUES,
    ALL_IMPORT_ORDER_ISSUES, ALL_RETURN_ISSUES, ALL_SPELLCHECK_ISSUES, ALL_STANDARD_ISSUES, ALL_WPS_ISSUES,
    FLAKE8_DISABLED_ISSUES
)
from src.python.evaluation.inspectors.inspectors_stat.issues.other_issues import PYTHON_AST_ISSUES, PYTHON_RADON_ISSUES
from src.python.evaluation.inspectors.inspectors_stat.issues.pylint_all_issues import ALL_ISSUES, PYLINT_DISABLED_ISSUES
from src.python.review.common.language import Language
from src.python.review.inspectors.checkstyle.checkstyle import CheckstyleInspector
from src.python.review.inspectors.checkstyle.issue_types import CHECK_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.detekt.detekt import DetektInspector
from src.python.review.inspectors.detekt.issue_types import DETECT_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.eslint.eslint import ESLintInspector
from src.python.review.inspectors.eslint.issue_types import ESLINT_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.flake8.flake8 import Flake8Inspector
from src.python.review.inspectors.issue import (
    get_default_issue_stat, get_main_category_by_issue_type, IssuesStat, IssueType
)
from src.python.review.inspectors.pmd.issue_types import PMD_RULE_TO_ISSUE_TYPE
from src.python.review.inspectors.pmd.pmd import PMDInspector
from src.python.review.inspectors.pyast.python_ast import PythonAstInspector
from src.python.review.inspectors.pylint.pylint import PylintInspector
from src.python.review.inspectors.radon.radon import RadonInspector


def __get_flake8_issue_keys() -> Set[str]:
    issues_dicts = [ALL_STANDARD_ISSUES, ALL_BUGBEAR_ISSUES, ALL_BUILTINS_ISSUES, ALL_RETURN_ISSUES,
                    ALL_FORMAT_STRING_ISSUES, ALL_IMPORT_ORDER_ISSUES, ALL_COMPREHENSIONS_ISSUES,
                    ALL_SPELLCHECK_ISSUES, ALL_WPS_ISSUES]
    all_issues = set().union(*map(lambda d: d.keys(), issues_dicts))
    return set(all_issues - set(FLAKE8_DISABLED_ISSUES))


def __match_issue_keys_to_issue_type(issue_keys: Set[str], matcher: Callable) -> Dict[str, IssueType]:
    matched_issues = {}
    for key in issue_keys:
        matched_issues[key] = matcher(key)
    return matched_issues


# Count for each main category the frequency of issues for this category
def __gather_issues_stat(issue_types: List[IssueType]) -> IssuesStat:
    main_category_to_issue_type = get_default_issue_stat()
    for issue_type in issue_types:
        main_category_to_issue_type[get_main_category_by_issue_type(issue_type)] += 1
    return main_category_to_issue_type


def __merge_issues_stats(*args: IssuesStat) -> IssuesStat:
    assert len(args) >= 1, 'Please, use at least one argument'
    final_stat = {}
    for key in args[0].keys():
        final_stat[key] = sum(d[key] for d in args)
    return final_stat


def __collect_language_stat(*args: Set[Tuple[Set[str], Callable]]) -> IssuesStat:
    all_issue_types = []
    for issues, matcher in args:
        all_issue_types.append(__match_issue_keys_to_issue_type(issues, matcher).values())
    return __merge_issues_stats(*map(lambda stat: __gather_issues_stat(stat), all_issue_types))


def collect_stat_by_language(language: Language) -> IssuesStat:
    if language == Language.PYTHON:
        python_inspection_to_matcher = [
            (set(set(ALL_ISSUES.keys()) - set(PYLINT_DISABLED_ISSUES)), PylintInspector.choose_issue_type),
            (__get_flake8_issue_keys(), Flake8Inspector.choose_issue_type),
            (set(PYTHON_RADON_ISSUES.keys()), RadonInspector.choose_issue_type),
            (set(PYTHON_AST_ISSUES.keys()), PythonAstInspector.choose_issue_type),
        ]
        return __collect_language_stat(*python_inspection_to_matcher)
    elif language == Language.JAVA:
        java_inspection_to_matcher = [
            (set(PMD_RULE_TO_ISSUE_TYPE.keys()), PMDInspector.choose_issue_type),
            (set(CHECK_CLASS_NAME_TO_ISSUE_TYPE.keys() - set(CheckstyleInspector.skipped_issues)),
             CheckstyleInspector.choose_issue_type),
        ]
        return __collect_language_stat(*java_inspection_to_matcher)
    elif language == Language.KOTLIN:
        kotlin_inspection_to_matcher = [
            (set(DETECT_CLASS_NAME_TO_ISSUE_TYPE.keys()), DetektInspector.choose_issue_type),
        ]
        return __collect_language_stat(*kotlin_inspection_to_matcher)
    elif language == Language.JS:
        js_inspection_to_matcher = [
            (set(ESLINT_CLASS_NAME_TO_ISSUE_TYPE.keys()), ESLintInspector.choose_issue_type),
        ]
        return __collect_language_stat(*js_inspection_to_matcher)

    raise NotImplementedError(f'Language {language} is not supported yet!')


def print_stat(language: Language, stat: IssuesStat) -> None:
    print(f'Collected statistics for {language.value.lower()} language:')
    for issue_type, freq in stat.items():
        print(f'{issue_type}: {freq} times;')
    print(f'Note: {IssueType.UNDEFINED} means a category that is not categorized among the four main categories. '
          f'Most likely it is {IssueType.INFO} category')


def __parse_language(language: str) -> Language:
    try:
        return Language(language.upper())
    except KeyError:
        raise KeyError(f'Incorrect language key: {language}. Please, try again!')


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    languages = ', '.join(map(lambda l: l.lower(), Language.values()))

    parser.add_argument('language',
                        type=__parse_language,
                        help=f'The language for which statistics will be printed. Available values are: {languages}')


def main() -> None:
    parser = argparse.ArgumentParser()
    configure_arguments(parser)
    args = parser.parse_args()

    language = args.language
    stat = collect_stat_by_language(language)
    print_stat(language, stat)


if __name__ == '__main__':
    main()
