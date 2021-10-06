from typing import Dict

from hyperstyle.src.python.review.inspectors.issue import IssueType

ESLINT_CLASS_NAME_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # Possible errors (according to Eslint doc)
    'for-direction': IssueType.ERROR_PRONE,
    'getter-return': IssueType.ERROR_PRONE,
    'no-async-promise-executor': IssueType.ERROR_PRONE,
    'no-compare-neg-zero': IssueType.ERROR_PRONE,
    'no-cond-assign': IssueType.ERROR_PRONE,
    'no-constant-condition': IssueType.BEST_PRACTICES,
    'no-control-regex': IssueType.ERROR_PRONE,
    'no-dupe-args': IssueType.ERROR_PRONE,
    'no-dupe-else-if': IssueType.ERROR_PRONE,
    'no-dupe-keys': IssueType.ERROR_PRONE,
    'no-duplicate-case': IssueType.ERROR_PRONE,

    'no-empty': IssueType.BEST_PRACTICES,
    'no-empty-character-class': IssueType.BEST_PRACTICES,
    'no-ex-assign': IssueType.BEST_PRACTICES,
    'no-extra-semi': IssueType.BEST_PRACTICES,

    'no-func-assign': IssueType.ERROR_PRONE,
    'no-import-assign': IssueType.ERROR_PRONE,

    'no-inner-declarations': IssueType.BEST_PRACTICES,
    'no-invalid-regexp': IssueType.ERROR_PRONE,
    'no-irregular-whitespace': IssueType.CODE_STYLE,
    'no-obj-calls': IssueType.BEST_PRACTICES,
    'no-prototype-builtins': IssueType.BEST_PRACTICES,
    'no-regex-spaces': IssueType.BEST_PRACTICES,
    'no-unexpected-multiline': IssueType.CODE_STYLE,
    'no-unreachable': IssueType.ERROR_PRONE,
    'use-isnan': IssueType.ERROR_PRONE,

    # Best practices (according to Eslint doc)
    'complexity': IssueType.CYCLOMATIC_COMPLEXITY,
    'curly': IssueType.CODE_STYLE,
    'consistent-return': IssueType.BEST_PRACTICES,
    'default-case': IssueType.BEST_PRACTICES,
    'eqeqeq': IssueType.BEST_PRACTICES,
    'no-case-declarations': IssueType.BEST_PRACTICES,
    'no-empty-function': IssueType.BEST_PRACTICES,
    'no-fallthrough': IssueType.BEST_PRACTICES,
    'no-global-assign': IssueType.BEST_PRACTICES,
    'no-multi-spaces': IssueType.CODE_STYLE,
    'no-octal': IssueType.BEST_PRACTICES,
    'no-redeclare': IssueType.BEST_PRACTICES,
    'no-self-assign': IssueType.BEST_PRACTICES,
    'no-unused-labels': IssueType.BEST_PRACTICES,
    'no-useless-catch': IssueType.BEST_PRACTICES,
    'no-useless-escape': IssueType.BEST_PRACTICES,
    'no-with': IssueType.BEST_PRACTICES,
    'yoda': IssueType.BEST_PRACTICES,

    # Variables, style issues, ECMA SCRIPT 6 (according to Eslint doc)
    'no-delete-var': IssueType.BEST_PRACTICES,
    'no-shadow-restricted-names': IssueType.BEST_PRACTICES,
    'no-undef': IssueType.BEST_PRACTICES,
    'no-unused-vars': IssueType.CODE_STYLE,
    'brace-style': IssueType.CODE_STYLE,
    'camelcase': IssueType.CODE_STYLE,
    'comma-style': IssueType.CODE_STYLE,
    'comma-spacing': IssueType.CODE_STYLE,
    'semi': IssueType.CODE_STYLE,
    'no-multiple-empty-lines': IssueType.CODE_STYLE,
    'space-infix-ops': IssueType.CODE_STYLE,
    'object-curly-newline': IssueType.CODE_STYLE,
    'no-trailing-spaces': IssueType.CODE_STYLE,
    'no-whitespace-before-property': IssueType.CODE_STYLE,
    'max-len': IssueType.CODE_STYLE,

    # ECMA SCRIPT 6
    'constructor-super': IssueType.BEST_PRACTICES,
    'no-class-assign': IssueType.BEST_PRACTICES,
    'no-const-assign': IssueType.BEST_PRACTICES,
    'no-dupe-class-members': IssueType.BEST_PRACTICES,
    'no-new-symbol': IssueType.BEST_PRACTICES,
    'no-this-before-super': IssueType.BEST_PRACTICES,
    'require-yield': IssueType.BEST_PRACTICES,
    'no-var': IssueType.CODE_STYLE,
}
