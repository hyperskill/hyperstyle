from typing import Dict

from src.python.review.inspectors.issue import IssueType

CODE_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'E800': IssueType.BEST_PRACTICES,  # flake8-eradicate

    # flake8-bugbear
    'B001': IssueType.BEST_PRACTICES,  # do not use bare except
    'B005': IssueType.BEST_PRACTICES,  # avoid strip() in multi-char strings
    'B007': IssueType.BEST_PRACTICES,  # unused loop's control variable

    # flake8-return
    'R504': IssueType.BEST_PRACTICES,

    # builtin naming
    'A003': IssueType.BEST_PRACTICES,
}

CODE_PREFIX_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'B': IssueType.ERROR_PRONE,  # flake8-bugbear
    'A': IssueType.ERROR_PRONE,  # flake8-builtins
    'R': IssueType.ERROR_PRONE,  # flake8-return

    'E': IssueType.CODE_STYLE,  # standard flake8
    'W': IssueType.CODE_STYLE,  # standard flake8
    'N': IssueType.CODE_STYLE,  # standard flake8
    'I': IssueType.CODE_STYLE,  # flake8-import-order

    'F': IssueType.BEST_PRACTICES,  # standard flake8
    'C': IssueType.BEST_PRACTICES,  # flake8-comprehensions
    'SC': IssueType.BEST_PRACTICES,  # flake8-spellcheck
}
