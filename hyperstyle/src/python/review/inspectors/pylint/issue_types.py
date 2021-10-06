from typing import Dict

from hyperstyle.src.python.review.inspectors.issue import IssueType

CODE_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # Basic checker
    'W0129': IssueType.ERROR_PRONE,  # Assert statement has a string literal as its first argument
    'W0127': IssueType.ERROR_PRONE,  # Assigning the same variable to itself
    'W0143': IssueType.ERROR_PRONE,  # Comparing against a callable
    'W0102': IssueType.ERROR_PRONE,  # Dangerous default value as argument
    'W0109': IssueType.ERROR_PRONE,  # Duplicate key in dictionary
    'W0106': IssueType.ERROR_PRONE,  # Expression is assigned to nothing
    'W0128': IssueType.ERROR_PRONE,  # Redeclared variable in assignment
    'W0104': IssueType.ERROR_PRONE,  # Statement seems to have no effect
    'W0105': IssueType.ERROR_PRONE,  # String statement has no effect
    'W0107': IssueType.BEST_PRACTICES,  # Unnecessary pass statement
    'W0101': IssueType.ERROR_PRONE,  # Unreachable code
    'W0125': IssueType.ERROR_PRONE,  # Using a conditional statement with a constant value
    'W0126': IssueType.ERROR_PRONE,  # Using a conditional statement with wrong function due to missing parentheses
    'R0124': IssueType.ERROR_PRONE,  # Redundant comparison
    'C0121': IssueType.BEST_PRACTICES,  # Expression is compared to singleton values like True, False or None
    'C0112': IssueType.BEST_PRACTICES,  # Empty docstring
    'C0123': IssueType.BEST_PRACTICES,  # Use isinstance() rather than type() for a type check

    # Classes checker
    'E0213': IssueType.CODE_STYLE,  # Method should have "self" as first argument
    'W0221': IssueType.ERROR_PRONE,  # Method has diff. number of args than in the interface or in an overridden method
    'W0237': IssueType.ERROR_PRONE,  # Method parameter has diff. name than in the interface or in an overridden method
    'W0223': IssueType.ERROR_PRONE,  # Method is abstract in class but is not overridden
    'W0236': IssueType.ERROR_PRONE,  # Method was overridden in a way that does not match its base class
    'W0222': IssueType.ERROR_PRONE,  # Signature differs from method
    'W0231': IssueType.ERROR_PRONE,  # __init__ method from base class is not called
    'C0205': IssueType.ERROR_PRONE,  # Class __slots__ should be a non-string iterable

    # Design checker
    'R0901': IssueType.COMPLEXITY,  # Too many ancestors
    'R0913': IssueType.COMPLEXITY,  # Too many arguments
    'R0916': IssueType.COMPLEXITY,  # Too many boolean expressions
    'R0912': IssueType.COMPLEXITY,  # Too many branches
    'R0902': IssueType.COMPLEXITY,  # Too many instance attributes
    'R0914': IssueType.COMPLEXITY,  # Too many locals
    'R0904': IssueType.COMPLEXITY,  # Too many public methods
    'R0911': IssueType.COMPLEXITY,  # Too many return statements
    'R0915': IssueType.COMPLEXITY,  # Too many statements

    # Exceptions checker
    'W0705': IssueType.ERROR_PRONE,  # Catching previously caught exception type
    'W0706': IssueType.ERROR_PRONE,  # The except handler raises immediately

    # Format checker
    'W0311': IssueType.CODE_STYLE,  # Bad indentation
    'W0301': IssueType.CODE_STYLE,  # Unnecessary semicolon
    'C0302': IssueType.COMPLEXITY,  # Too many lines in module

    # Imports checker
    'R0401': IssueType.ERROR_PRONE,  # Cyclic import
    'C0415': IssueType.BEST_PRACTICES,  # Import outside toplevel

    # Python3 checker
    'W1659': IssueType.ERROR_PRONE,  # Accessing a removed xreadlines attribute
    'W1623': IssueType.ERROR_PRONE,  # Assigning to a class's __metaclass__ attribute
    'W1622': IssueType.ERROR_PRONE,  # Called a next() method on an object
    'W1620': IssueType.ERROR_PRONE,  # Calling a dict.iter*() method
    'W1621': IssueType.ERROR_PRONE,  # Calling a dict.view*() method
    'W1645': IssueType.ERROR_PRONE,  # Exception.message removed in Python 3
    'W1641': IssueType.ERROR_PRONE,  # Implementing __eq__ without also implementing __hash__
    'W1624': IssueType.ERROR_PRONE,  # Indexing exceptions will not work on Python 3
    'W1648': IssueType.ERROR_PRONE,  # Module moved in Python 3
    'W1625': IssueType.ERROR_PRONE,  # Raising a string exception
    'W1611': IssueType.ERROR_PRONE,  # StandardError built-in referenced
    'W1662': IssueType.ERROR_PRONE,  # Using a variable that was bound inside a comprehension
    'W1661': IssueType.ERROR_PRONE,  # Using an exception object that was bound by an except handler
    'W1640': IssueType.ERROR_PRONE,  # Using the cmp argument for list.sort / sorted
    'W1630': IssueType.ERROR_PRONE,  # __cmp__ method defined
    'W1614': IssueType.ERROR_PRONE,  # __coerce__ method defined
    'W1615': IssueType.ERROR_PRONE,  # __delslice__ method defined
    'W1642': IssueType.ERROR_PRONE,  # __div__ method defined
    'W1616': IssueType.ERROR_PRONE,  # __getslice__ method defined
    'W1628': IssueType.ERROR_PRONE,  # __hex__ method defined
    'W1643': IssueType.ERROR_PRONE,  # __idiv__ method defined
    'W1629': IssueType.ERROR_PRONE,  # __nonzero__ method defined
    'W1627': IssueType.ERROR_PRONE,  # __oct__ method defined
    'W1644': IssueType.ERROR_PRONE,  # __rdiv__ method defined
    'W1617': IssueType.ERROR_PRONE,  # __setslice__ method defined
    'W1601': IssueType.ERROR_PRONE,  # apply built-in referenced
    'W1602': IssueType.ERROR_PRONE,  # basestring built-in referenced
    'W1603': IssueType.ERROR_PRONE,  # buffer built-in referenced
    'W1604': IssueType.ERROR_PRONE,  # cmp built-in referenced
    'W1605': IssueType.ERROR_PRONE,  # coerce built-in referenced
    'W1619': IssueType.ERROR_PRONE,  # division w/o __future__ statement
    'W1606': IssueType.ERROR_PRONE,  # execfile built-in referenced
    'W1607': IssueType.ERROR_PRONE,  # file built-in referenced
    'W1618': IssueType.ERROR_PRONE,  # import missing `from __future__ import absolute_import`
    'W1632': IssueType.ERROR_PRONE,  # input built-in referenced
    'W1634': IssueType.ERROR_PRONE,  # intern built-in referenced
    'W1608': IssueType.ERROR_PRONE,  # long built-in referenced
    'W1653': IssueType.ERROR_PRONE,  # next method defined
    'W1609': IssueType.ERROR_PRONE,  # raw_input built-in referenced
    'W1610': IssueType.ERROR_PRONE,  # reduce built-in referenced
    'W1626': IssueType.ERROR_PRONE,  # reload built-in referenced
    'W1633': IssueType.ERROR_PRONE,  # round built-in referenced
    'W1647': IssueType.ERROR_PRONE,  # sys.maxint removed
    'W1635': IssueType.ERROR_PRONE,  # unichr built-in referenced
    'W1612': IssueType.ERROR_PRONE,  # unicode built-in referenced
    'W1613': IssueType.ERROR_PRONE,  # xrange built-in referenced

    # Refactoring checker
    'R1702': IssueType.COMPLEXITY,  # Too many nested blocks
    'C0113': IssueType.BEST_PRACTICES,  # Boolean expression contains an unneeded negation
    'C0201': IssueType.BEST_PRACTICES,  # Consider iterating the dictionary directly instead of calling .keys()
    'C0206': IssueType.BEST_PRACTICES,  # Consider iterating with .items()
    'C0200': IssueType.BEST_PRACTICES,  # Consider using enumerate instead of iterating with range and len
    'C1801': IssueType.BEST_PRACTICES,  # Do not use `len(foo)` without comparison to determine if a 'foo' is empty
    'C0207': IssueType.BEST_PRACTICES,  # use-maxsplit-arg
    'C0208': IssueType.BEST_PRACTICES,  # Use a sequence type when iterating over values

    # Stdlib checker
    'W1501': IssueType.ERROR_PRONE,  # bad-open-mode

    # String checker
    'W1308': IssueType.ERROR_PRONE,  # Duplicate string formatting argument, consider passing as named argument
    'W1305': IssueType.ERROR_PRONE,  # Format string contains both automatic numbering and manual specification
    'W1300': IssueType.ERROR_PRONE,  # Format string dictionary key should be a string
    'W1302': IssueType.ERROR_PRONE,  # Invalid format string
    'W1306': IssueType.ERROR_PRONE,  # Missing format attribute in format specifier
    'W1303': IssueType.ERROR_PRONE,  # Missing keyword argument for format string
    'W1304': IssueType.ERROR_PRONE,  # Unused format argument
    'W1301': IssueType.ERROR_PRONE,  # Unused key in format string dictionary
    'W1309': IssueType.ERROR_PRONE,  # Using an f-string that does not have any interpolated variables
    'W1310': IssueType.ERROR_PRONE,  # Using formatting for a string that does not have any interpolated variables
    'W1307': IssueType.ERROR_PRONE,  # Using invalid lookup key in format specifier

    # Variables check
    'W0632': IssueType.ERROR_PRONE,  # Possible unbalanced tuple unpacking with sequence
    'W0622': IssueType.ERROR_PRONE,  # Redefining built-in
    'W0631': IssueType.ERROR_PRONE,  # Using possibly undefined loop variable

    # Other
    'W0312': IssueType.CODE_STYLE,  # mixed indentation
}

# C convention related checks
# R refactoring related checks
# W warnings for stylistic issues, or minor programming issues
# E errors, for probable bugs in the code

CATEGORY_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'C': IssueType.CODE_STYLE,
    'R': IssueType.BEST_PRACTICES,
    'W': IssueType.BEST_PRACTICES,
    'E': IssueType.ERROR_PRONE,
}
