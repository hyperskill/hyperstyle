from typing import Dict

from hyperstyle.src.python.review.inspectors.issue import IssueType

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

    # flake8-broken-line
    'N400': IssueType.CODE_STYLE,

    # flake8-commas
    'C812': IssueType.CODE_STYLE,
    'C813': IssueType.CODE_STYLE,
    'C815': IssueType.CODE_STYLE,
    'C816': IssueType.CODE_STYLE,
    'C818': IssueType.CODE_STYLE,
    'C819': IssueType.CODE_STYLE,

    # The categorization for WPS was created using the following document: https://bit.ly/3yms06n

    # WPS: Naming
    'WPS117': IssueType.CODE_STYLE,  # Forbid naming variables self, cls, or mcs.
    'WPS125': IssueType.ERROR_PRONE,  # Forbid variable or module names which shadow builtin names.

    # WPS: Consistency
    'WPS300': IssueType.CODE_STYLE,  # Forbid imports relative to the current folder.
    'WPS301': IssueType.CODE_STYLE,  # Forbid imports like import os.path.
    'WPS304': IssueType.CODE_STYLE,  # Forbid partial floats like .05 or 23..
    'WPS310': IssueType.BEST_PRACTICES,  # Forbid uppercase X, O, B, and E in numbers.
    'WPS313': IssueType.CODE_STYLE,  # Enforce separation of parenthesis from keywords with spaces.
    'WPS317': IssueType.CODE_STYLE,  # Forbid incorrect indentation for parameters.
    'WPS318': IssueType.CODE_STYLE,  # Forbid extra indentation.
    'WPS319': IssueType.CODE_STYLE,  # Forbid brackets in the wrong position.
    'WPS320': IssueType.CODE_STYLE,  # Forbid multi-line function type annotations.
    'WPS321': IssueType.CODE_STYLE,  # Forbid uppercase string modifiers.
    'WPS324': IssueType.ERROR_PRONE,  # If any return has a value, all return nodes should have a value.
    'WPS325': IssueType.ERROR_PRONE,  # If any yield has a value, all yield nodes should have a value.
    'WPS326': IssueType.ERROR_PRONE,  # Forbid implicit string concatenation.
    'WPS329': IssueType.ERROR_PRONE,  # Forbid meaningless except cases.
    'WPS330': IssueType.ERROR_PRONE,  # Forbid unnecessary operators in your code.
    'WPS338': IssueType.BEST_PRACTICES,  # Forbid incorrect order of methods inside a class.
    'WPS339': IssueType.CODE_STYLE,  # Forbid meaningless zeros.
    'WPS340': IssueType.CODE_STYLE,  # Forbid extra + signs in the exponent.
    'WPS341': IssueType.CODE_STYLE,  # Forbid lowercase letters as hex numbers.
    'WPS343': IssueType.CODE_STYLE,  # Forbid uppercase complex number suffix.
    'WPS344': IssueType.ERROR_PRONE,  # Forbid explicit division (or modulo) by zero.
    'WPS347': IssueType.ERROR_PRONE,  # Forbid imports that may cause confusion outside of the module.
    'WPS348': IssueType.CODE_STYLE,  # Forbid starting lines with a dot.
    'WPS350': IssueType.CODE_STYLE,  # Enforce using augmented assign pattern.
    'WPS355': IssueType.CODE_STYLE,  # Forbid useless blank lines before and after brackets.
    'WPS361': IssueType.CODE_STYLE,  # Forbids inconsistent newlines in comprehensions.

    # WPS: Best practices
    'WPS405': IssueType.ERROR_PRONE,  # Forbid anything other than ast.Name to define loop variables.
    'WPS406': IssueType.ERROR_PRONE,  # Forbid anything other than ast.Name to define contexts.
    'WPS408': IssueType.ERROR_PRONE,  # Forbid using the same logical conditions in one expression.
    'WPS414': IssueType.ERROR_PRONE,  # Forbid tuple unpacking with side-effects.
    'WPS415': IssueType.ERROR_PRONE,  # Forbid the same exception class in multiple except blocks.
    'WPS416': IssueType.ERROR_PRONE,  # Forbid yield keyword inside comprehensions.
    'WPS417': IssueType.ERROR_PRONE,  # Forbid duplicate items in hashes.
    'WPS418': IssueType.ERROR_PRONE,  # Forbid exceptions inherited from BaseException.
    'WPS419': IssueType.ERROR_PRONE,  # Forbid multiple returning paths with try / except case.
    'WPS424': IssueType.ERROR_PRONE,  # Forbid BaseException exception.
    'WPS426': IssueType.ERROR_PRONE,  # Forbid lambda inside loops.
    'WPS428': IssueType.ERROR_PRONE,  # Forbid statements that do nothing.
    'WPS432': IssueType.INFO,  # Forbid magic numbers.
    'WPS433': IssueType.CODE_STYLE,  # Forbid imports nested in functions.
    'WPS439': IssueType.ERROR_PRONE,  # Forbid Unicode escape sequences in binary strings.
    'WPS440': IssueType.ERROR_PRONE,  # Forbid overlapping local and block variables.
    'WPS441': IssueType.ERROR_PRONE,  # Forbid control variables after the block body.
    'WPS442': IssueType.ERROR_PRONE,  # Forbid shadowing variables from outer scopes.
    'WPS443': IssueType.ERROR_PRONE,  # Forbid explicit unhashable types of asset items and dict keys.
    'WPS445': IssueType.ERROR_PRONE,  # Forbid incorrectly named keywords in starred dicts.
    'WPS448': IssueType.ERROR_PRONE,  # Forbid incorrect order of except.
    'WPS449': IssueType.ERROR_PRONE,  # Forbid float keys.
    'WPS456': IssueType.ERROR_PRONE,  # Forbids using float("NaN") construct to generate NaN.
    'WPS457': IssueType.ERROR_PRONE,  # Forbids use of infinite while True: loops.
    'WPS458': IssueType.ERROR_PRONE,  # Forbids to import from already imported modules.

    # WPS: Refactoring
    'WPS524': IssueType.ERROR_PRONE,  # Forbid misrefactored self assignment.

    # WPS: OOP
    'WPS601': IssueType.ERROR_PRONE,  # Forbid shadowing class level attributes with instance level attributes.
    'WPS613': IssueType.ERROR_PRONE,  # Forbid super() with incorrect method or property access.
    'WPS614': IssueType.ERROR_PRONE,  # Forbids descriptors in regular functions.
}

CODE_PREFIX_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'B': IssueType.ERROR_PRONE,  # flake8-bugbear
    'A': IssueType.ERROR_PRONE,  # flake8-builtins
    'R': IssueType.ERROR_PRONE,  # flake8-return
    'P': IssueType.ERROR_PRONE,  # flake8-format-string

    'E': IssueType.CODE_STYLE,  # standard flake8
    'W': IssueType.CODE_STYLE,  # standard flake8
    'N': IssueType.CODE_STYLE,  # standard flake8
    'I': IssueType.CODE_STYLE,  # flake8-import-order

    'F': IssueType.BEST_PRACTICES,  # standard flake8
    'C': IssueType.BEST_PRACTICES,  # flake8-comprehensions
    'SC': IssueType.INFO,  # flake8-spellcheck

    'WPS1': IssueType.CODE_STYLE,  # WPS type: Naming
    'WPS2': IssueType.COMPLEXITY,  # WPS type: Complexity
    'WPS3': IssueType.BEST_PRACTICES,  # WPS type: Consistency
    'WPS4': IssueType.BEST_PRACTICES,  # WPS type: Best practices
    'WPS5': IssueType.BEST_PRACTICES,  # WPS type: Refactoring
    'WPS6': IssueType.BEST_PRACTICES,  # WPS type: OOP
}
