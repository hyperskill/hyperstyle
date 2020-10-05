from typing import Dict

from review.inspectors.issue import IssueType

# C convention related checks
# R refactoring related checks
# W warnings for stylistic issues, or minor programming issues
# E errors, for probable bugs in the code

CODE_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'W0101': IssueType.ERROR_PRONE,  # unreachable code
    'W0102': IssueType.ERROR_PRONE,  # dangerous default value
    'W0104': IssueType.ERROR_PRONE,  # statement doesn't have any effect
    'W0109': IssueType.ERROR_PRONE,  # duplicate key in dictionary
    'W0221': IssueType.ERROR_PRONE,  # arguments number differs from method
    'W0222': IssueType.ERROR_PRONE,  # different signature
    'W0223': IssueType.ERROR_PRONE,  # abstract method is not overridden
    'W0231': IssueType.ERROR_PRONE,  # super init not called
    'W0311': IssueType.CODE_STYLE,  # bad indentation
    'W0312': IssueType.CODE_STYLE,  # mixed indentation
    'W0631': IssueType.ERROR_PRONE,  # using an undefined loop variable
    'W0622': IssueType.ERROR_PRONE,  # redefining built-in
    'W1648': IssueType.ERROR_PRONE,  # a module is no longer exists
}

CATEGORY_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'C': IssueType.CODE_STYLE,
    'R': IssueType.BEST_PRACTICES,
    'W': IssueType.BEST_PRACTICES,
    'E': IssueType.ERROR_PRONE,
}
