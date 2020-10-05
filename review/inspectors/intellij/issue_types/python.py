from typing import Dict

from review.inspectors.issue import IssueType

ISSUE_CLASS_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'Access to a protected member of a class or a module':
        IssueType.BEST_PRACTICES,

    'Access to properties':
        IssueType.ERROR_PRONE,

    'Argument passed to function is equal to default parameter value':
        IssueType.BEST_PRACTICES,

    'Assigning function call that doesn\'t return anything':
        IssueType.BEST_PRACTICES,

    'Assignment can be replaced with augmented assignment':
        IssueType.BEST_PRACTICES,

    'Assignment to \'for\' loop or \'with\' statement parameter':
        IssueType.BEST_PRACTICES,

    'Bad except clauses order':
        IssueType.ERROR_PRONE,

    'Boolean variable check can be simplified':
        IssueType.BEST_PRACTICES,

    'Byte literal contains characters > 255':
        IssueType.ERROR_PRONE,

    'Calling a method by class using an instance of a different class':
        IssueType.BEST_PRACTICES,

    'Chained comparisons can be simplified':
        IssueType.BEST_PRACTICES,

    'Checks that functions decorated by pytest parametrize have correct arguments':
        IssueType.ERROR_PRONE,

    'Class has no __init__ method':
        IssueType.BEST_PRACTICES,

    'Class must implement all abstract methods':
        IssueType.ERROR_PRONE,

    'Class specific decorator on method outside class':
        IssueType.BEST_PRACTICES,

    'Classic style class usage':
        IssueType.BEST_PRACTICES,

    'Code compatibility inspection':
        IssueType.ERROR_PRONE,

    'Command-line inspection':
        IssueType.ERROR_PRONE,

    'Comparison with None performed with equality operators':
        IssueType.BEST_PRACTICES,

    'Coroutine is not awaited':
        IssueType.ERROR_PRONE,

    'Cython variable usage before declaration':
        IssueType.ERROR_PRONE,

    'Dataclass definition and usages':
        IssueType.ERROR_PRONE,

    'Default argument is mutable':
        IssueType.ERROR_PRONE,

    'Definition of __slots__ in a class':
        IssueType.ERROR_PRONE,

    'Deprecated function, class or module':
        IssueType.ERROR_PRONE,

    'Dictionary contains duplicate keys':
        IssueType.ERROR_PRONE,

    'Dictionary creation could be rewritten by dictionary literal':
        IssueType.BEST_PRACTICES,

    'Errors in string formatting operations':
        IssueType.ERROR_PRONE,

    'Exception doesn\'t inherit from standard \'\'Exception\'\' class':
        IssueType.ERROR_PRONE,

    'File contains non-ASCII character':
        IssueType.ERROR_PRONE,

    'Final classes, methods and variables':
        IssueType.ERROR_PRONE,

    'from __future__ import must be the first executable statement':
        IssueType.ERROR_PRONE,

    'Function call can be replaced with set literal':
        IssueType.BEST_PRACTICES,

    'Global variable is undefined at the module level':
        IssueType.ERROR_PRONE,

    'Incompatible signatures of __new__ and __init__':
        IssueType.ERROR_PRONE,

    'Inconsistent indentation':
        IssueType.ERROR_PRONE,

    'Incorrect call arguments':
        IssueType.ERROR_PRONE,

    'Incorrect docstring':
        IssueType.BEST_PRACTICES,

    '__init__ method that returns a value':
        IssueType.ERROR_PRONE,

    'Instance attribute defined outside __init__':
        IssueType.BEST_PRACTICES,
    'Invalid interpreter configured':
        IssueType.ERROR_PRONE,

    'List creation could be rewritten by list literal':
        IssueType.BEST_PRACTICES,

    'Method may be static':
        IssueType.BEST_PRACTICES,

    'Method signature does not match signature of overridden method':
        IssueType.ERROR_PRONE,

    'Methods having troubles with first parameter':
        IssueType.ERROR_PRONE,

    'Missed call to __init__ of super class':
        IssueType.ERROR_PRONE,

    'Missing or empty docstring':
        IssueType.BEST_PRACTICES,

    'Missing type hinting for function definition':
        IssueType.BEST_PRACTICES,

    'Namedtuple definition':
        IssueType.ERROR_PRONE,

    'No encoding specified for file':
        IssueType.BEST_PRACTICES,

    'Old-style class contains new-style class features':
        IssueType.ERROR_PRONE,

    'Overloads in regular Python files':
        IssueType.ERROR_PRONE,

    'Package requirements':
        IssueType.ERROR_PRONE,

    'PEP 8 coding style violation':
        IssueType.CODE_STYLE,

    'PEP 8 naming convention violation':
        IssueType.CODE_STYLE,

    'Problematic nesting of decorators':
        IssueType.BEST_PRACTICES,

    'Property definitions':
        IssueType.ERROR_PRONE,

    'Protocol definition and usages':
        IssueType.ERROR_PRONE,

    'Raising a string exception':
        IssueType.ERROR_PRONE,

    'Reassignment of method\'s first argument':
        IssueType.ERROR_PRONE,

    'Redeclared names without usage':
        IssueType.ERROR_PRONE,

    'Redundant parentheses':
        IssueType.CODE_STYLE,

    'Shadowing built-ins':
        IssueType.ERROR_PRONE,

    'Shadowing names from outer scopes':
        IssueType.BEST_PRACTICES,

    'Single quoted docstring':
        IssueType.BEST_PRACTICES,

    'Statement has no effect':
        IssueType.ERROR_PRONE,

    'Stub packages advertiser':
        IssueType.BEST_PRACTICES,

    'Stub packages compatibility inspection':
        IssueType.ERROR_PRONE,

    'Too broad exception clauses':
        IssueType.BEST_PRACTICES,

    'Trailing semicolon in statement':
        IssueType.CODE_STYLE,

    'Trying to call a non-callable object':
        IssueType.ERROR_PRONE,

    'Tuple assignment balance is incorrect':
        IssueType.ERROR_PRONE,

    'Tuple item assignment':
        IssueType.ERROR_PRONE,

    'Type checker':
        IssueType.ERROR_PRONE,

    'Type hints definitions and usages':
        IssueType.ERROR_PRONE,

    'Type in docstring doesn\'t match inferred type':
        IssueType.BEST_PRACTICES,

    'TypedDict definition and usages':
        IssueType.ERROR_PRONE,

    'Unbound local variable':
        IssueType.ERROR_PRONE,

    'Unnecessary backslash':
        IssueType.BEST_PRACTICES,

    'Unreachable code':
        IssueType.ERROR_PRONE,

    'Unresolved references':
        IssueType.ERROR_PRONE,

    'Unused local':
        IssueType.BEST_PRACTICES,

    'Wrong arguments to call super':
        IssueType.ERROR_PRONE,
}
