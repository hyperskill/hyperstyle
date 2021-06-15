# According to https://seanwasere.com/pylint--list-msgs/
ALL_ISSUES = {
    'C0102': 'Used when the name is listed in the black list (unauthorized names).',
    'C0103': 'Used when the name doesn\'t conform to naming rules associated to its type (constant, variable, '
             'class...).',
    'C0111': 'Used when a module, function, class or method has no docstring.Some special methods like __init__ '
             'doesn\'t necessary require a docstring.',
    'C0112': 'Used when a module, function, class or method has an empty docstring (it would be too easy ;).',
    'C0113': 'Used when a boolean expression contains an unneeded negation.',
    'C0121': 'Used when an expression is compared to singleton values like True, False or None.',
    'C0122': 'Used when the constant is placed on the left side of a comparison. It is usually clearer in intent to '
             'place it in the right hand side of the comparison.',
    'C0123': 'The idiomatic way to perform an explicit typecheck in Python is to use isinstance(x, Y) rather than '
             'type(x) == Y, type(x) is Y. Though there are unusual situations where these give different results.',
    'C0200': 'Emitted when code that iterates with range and len is encountered. Such code can be simplified by using '
             'the enumerate builtin.',
    'C0201': 'Emitted when the keys of a dictionary are iterated through the .keys() method. It is enough to just '
             'iterate through the dictionary itself, as in "for key in dictionary".',
    'C0202': 'Used when a class method has a first argument named differently than the value specified in '
             'valid-classmethod-first-arg option (default to "cls"), recommended to easily differentiate them from '
             'regular instance methods.',
    'C0203': 'Used when a metaclass method has a first argument named differently than the value specified in '
             'valid-classmethod-first-arg option (default to "cls"), recommended to easily differentiate them from '
             'regular instance methods.',
    'C0204': 'Used when a metaclass class method has a first argument named differently than the value specified in '
             'valid-metaclass-classmethod-first-arg option (default to "mcs"), recommended to easily differentiate '
             'them from regular instance methods.',
    'C0205': 'Used when a class __slots__ is a simple string, rather than an iterable.',
    'C0301': 'Used when a line is longer than a given number of characters.',
    'C0302': 'Used when a module has too many lines, reducing its readability.',
    'C0303': 'Used when there is whitespace between the end of a line and the newline.',
    'C0304': 'Used when the last line in a file is missing a newline.',
    'C0305': 'Used when there are trailing blank lines in a file.',
    'C0321': 'Used when more than on statement are found on the same line.',
    'C0325': 'Used when a single item in parentheses follows an if, for, or other keyword.',
    'C0326': 'Used when a wrong number of spaces is used around an operator, bracket or block opener.',
    'C0327': 'Used when there are mixed (LF and CRLF) newline signs in a file.',
    'C0328': 'Used when there is different newline than expected.',
    'C0330': 'bad-continuation',
    'C0401': 'Used when a word in comment is not spelled correctly.',
    'C0402': 'Used when a word in docstring is not spelled correctly.',
    'C0403': 'Used when a word in docstring cannot be checked by enchant.',
    'C0410': 'Used when import statement importing multiple modules is detected.',
    'C0411': 'Used when PEP8 import order is not respected (standard imports first, then third-party libraries, '
             'then local imports)',
    'C0412': 'Used when imports are not grouped by packages',
    'C0413': 'Used when code and imports are mixed',
    'C0414': 'Used when an import alias is same as original package.e.g using import numpy as numpy instead of import '
             'numpy as np',
    'C1801': 'Used when Pylint detects that len(sequence) is being used inside a condition to determine if a sequence '
             'is empty. Instead of comparing the length to 0, rely on the fact that empty sequences are false.',

    'E0001': 'Used when a syntax error is raised for a module.',
    'E0011': 'Used when an unknown inline option is encountered.',
    'E0012': 'Used when a bad value for an inline option is encountered.',
    'E0100': 'Used when the special class method __init__ is turned into a generator by a yield in its body.',
    'E0101': 'Used when the special class method __init__ has an explicit return value.',
    'E0102': 'Used when a function / class / method is redefined.',
    'E0103': 'Used when break or continue keywords are used outside a loop.',
    'E0104': 'Used when a "return" statement is found outside a function or method.',
    'E0105': 'Used when a "yield" statement is found outside a function or method.',
    'E0107': 'Used when you attempt to use the C-style pre-increment or pre-decrement operator -- and ++, '
             'which doesn\'t exist in Python.',
    'E0108': 'Duplicate argument names in function definitions are syntax errors.',
    'E0110': 'Used when an abstract class with `abc.ABCMeta` as metaclass has abstract methods and is instantiated.',
    'E0111': 'Used when the first argument to reversed() builtin isn\'t a sequence (does not implement __reversed__, '
             'nor __getitem__ and __len__',
    'E0112': 'Emitted when there are more than one starred expressions (`*x`) in an assignment. This is a SyntaxError.',
    'E0113': 'Emitted when a star expression is used as a starred assignment target.',
    'E0114': 'Emitted when a star expression is not used in an assignment target.',
    'E0115': 'Emitted when a name is both nonlocal and global.',
    'E0116': 'Emitted when the `continue` keyword is found inside a finally clause, which is a SyntaxError.',
    'E0117': 'Emitted when a nonlocal variable does not have an attached name somewhere in the parent scopes',
    'E0118': 'Emitted when a name is used prior a global declaration, which results in an error since Python 3.6. '
             'This message can\'t be emitted when using Python < 3.6.',
    'E0119': 'Emitted when format function is not called on str object. '
             'This might not be what the user intended to do.',
    'E0202': 'Used when a class defines a method which is hidden by an instance attribute from an ancestor class or '
             'set by some client code.',
    'E0203': 'Used when an instance member is accessed before it\'s actually assigned.',
    'E0211': 'Used when a method which should have the bound instance as first argument has no argument defined.',
    'E0213': 'Used when a method has an attribute different the "self" as first argument. This is considered as an '
             'error since this is a so common convention that you shouldn\'t break it!',
    'E0236': 'Used when an invalid (non-string) object occurs in __slots__.',
    'E0237': 'Used when assigning to an attribute not defined in the class slots.',
    'E0238': 'Used when an invalid __slots__ is found in class. Only a string, an iterable or a sequence is permitted.',
    'E0239': 'Used when a class inherits from something which is not a class.',
    'E0240': 'Used when a class has an inconsistent method resolution order.',
    'E0241': 'Used when a class has duplicate bases.',
    'E0301': 'Used when an __iter__ method returns something which is not an iterable (i.e. has no `__next__` method)',
    'E0302': 'Emitted when a special method was defined with an invalid number of parameters. If it has too few or '
             'too many, it might not work at all.',
    'E0303': 'Used when a __len__ method returns something which is not a non-negative integer',
    'E0401': 'Used when pylint has been unable to import a module.',
    'E0402': 'Used when a relative import tries to access too many levels in the current package.',
    'E0601': 'Used when a local variable is accessed before its assignment.',
    'E0602': 'Used when an undefined variable is accessed.',
    'E0603': 'Used when an undefined variable name is referenced in __all__.',
    'E0604': 'Used when an invalid (non-string) object occurs in __all__.',
    'E0611': 'Used when a name cannot be found in a module.',
    'E0633': 'Used when something which is not a sequence is used in an unpack assignment',
    'E0701': 'Used when except clauses are not in the correct order (from the more specific to the more generic). If '
             'you don\'t fix the order, some exceptions may not be caught by the most specific handler.',
    'E0702': 'Used when something which is neither a class, an instance or a string is raised (i.e. a `TypeError` '
             'will be raised).',
    'E0703': 'Used when using the syntax "raise ... from ...", where the exception context is not an exception, '
             'nor None.',
    'E0704': 'Used when a bare raise is not used inside an except clause. This generates an error, since there are no '
             'active exceptions to be reraised. An exception to this rule is represented by a bare raise inside a '
             'finally clause, which might work, as long as an exception is raised inside the try block, '
             'but it is nevertheless a code smell that must not be relied upon.',
    'E0710': 'Used when a new style class which doesn\'t inherit from BaseException is raised.',
    'E0711': 'Used when NotImplemented is raised instead of NotImplementedError',
    'E0712': 'Used when a class which doesn\'t inherit from Exception is used as an exception in an except clause.',
    'E1003': 'Used when another argument than the current class is given as first argument of the super builtin.',
    'E1101': 'Used when a variable is accessed for an unexistent member.',
    'E1102': 'Used when an object being called has been inferred to a non callable object.',
    'E1111': 'Used when an assignment is done on a function call but the inferred function doesn\'t return anything.',
    'E1120': 'Used when a function call passes too few arguments.',
    'E1121': 'Used when a function call passes too many positional arguments.',
    'E1123': 'Used when a function call passes a keyword argument that doesn\'t correspond to one of the function\'s '
             'parameter names.',
    'E1124': 'Used when a function call would result in assigning multiple values to a function parameter, one value '
             'from a positional argument and one from a keyword argument.',
    'E1125': 'Used when a function call does not pass a mandatory keyword-only argument.',
    'E1126': 'Used when a sequence type is indexed with an invalid type. Valid types are ints, slices, and objects '
             'with an __index__ method.',
    'E1127': 'Used when a slice index is not an integer, None, or an object with an __index__ method.',
    'E1128': 'Used when an assignment is done on a function call but the inferred function returns nothing but None.',
    'E1129': 'Used when an instance in a with statement doesn\'t implement the context manager protocol('
             '__enter__/__exit__).',
    'E1130': 'Emitted when a unary operand is used on an object which does not support this type of operation.',
    'E1131': 'Emitted when a binary arithmetic operation between two operands is not supported.',
    'E1132': 'Emitted when a function call got multiple values for a keyword.',
    'E1133': 'Used when a non-iterable value is used in place where iterable is expected',
    'E1134': 'Used when a non-mapping value is used in place where mapping is expected',
    'E1135': 'Emitted when an instance in membership test expression doesn\'t implement membership protocol ('
             '__contains__/__iter__/__getitem__).',
    'E1136': 'Emitted when a subscripted value doesn\'t support subscription (i.e. doesn\'t define __getitem__ method '
             'or __class_getitem__ for a class).',
    'E1137': 'Emitted when an object does not support item assignment (i.e. doesn\'t define __setitem__ method).',
    'E1138': 'Emitted when an object does not support item deletion (i.e. doesn\'t define __delitem__ method).',
    'E1139': 'Emitted whenever we can detect that a class is using, as a metaclass, something which might be invalid '
             'for using as a metaclass.',
    'E1140': 'Emitted when a dict key is not hashable (i.e. doesn\'t define __hash__ method).',
    'E1200': 'Used when an unsupported format character is used in a logging statement format string.',
    'E1201': 'Used when a logging statement format string terminates before the end of a conversion specifier.',
    'E1205': 'Used when a logging format string is given too many arguments.',
    'E1206': 'Used when a logging format string is given too few arguments.',
    'E1300': 'Used when an unsupported format character is used in a format string.',
    'E1301': 'Used when a format string terminates before the end of a conversion specifier.',
    'E1302': 'Used when a format string contains both named (e.g. \'%(foo)d\') and unnamed (e.g. \'%d\') conversion '
             'specifiers. This is also used when a named conversion specifier contains * for the minimum field width '
             'and/or precision.',
    'E1303': 'Used when a format string that uses named conversion specifiers is used with an argument that is not a '
             'mapping.',
    'E1304': 'Used when a format string that uses named conversion specifiers is used with a dictionary that doesn\'t '
             'contain all the keys required by the format string.',
    'E1305': 'Used when a format string that uses unnamed conversion specifiers is given too many arguments.',
    'E1306': 'Used when a format string that uses unnamed conversion specifiers is given too few arguments',
    'E1307': 'Used when a type required by format string is not suitable for actual argument type',
    'E1310': 'The argument to a str.{l,r,}strip call contains a duplicate character,',
    'E1507': 'Env manipulation functions support only string type arguments. See '
             'https://docs.python.org/3/library/os.html#os.getenv.',
    'E1601': 'Used when a print statement is used (`print` is a function in Python 3)',
    'E1602': 'Used when parameter unpacking is specified for a function(Python 3 doesn\'t allow it)',
    'E1603': 'Python3 will not allow implicit unpacking of exceptions in except clauses. See '
             'http://www.python.org/dev/peps/pep-3110/',
    'E1604': 'Used when the alternate raise syntax \'raise foo, bar\' is used instead of \'raise foo(bar)\'.',
    'E1605': 'Used when the deprecated "``" (backtick) operator is used instead of the str() function.',
    'E1700': 'Used when an `yield` or `yield from` statement is found inside an async function. This message can\'t '
             'be emitted when using Python < 3.5.',
    'E1701': 'Used when an async context manager is used with an object that does not implement the async context '
             'management protocol. This message can\'t be emitted when using Python < 3.5.',

    # refactoring related checks
    'R0123': 'Used when comparing an object to a literal, which is usually what you do not want to do, since you can '
             'compare to a different literal than what was expected altogether.',
    'R0124': 'Used when something is compared against itself.',
    'R0201': 'Used when a method doesn\'t use its bound instance, and so could be written as a function.',
    'R0202': 'Used when a class method is defined without using the decorator syntax.',
    'R0203': 'Used when a static method is defined without using the decorator syntax.',
    'R0205': 'Used when a class inherit from object, which under python3 is implicit, hence can be safely removed '
             'from bases.',
    'R0401': 'Used when a cyclic import between two or more modules is detected.',
    'R0801': 'Indicates that a set of similar lines has been detected among multiple file. This usually means that '
             'the code should be refactored to avoid this duplication.',
    'R0901': 'Used when class has too many parent classes, try to reduce this to get a simpler (and so easier to use) '
             'class.',
    'R0902': 'Used when class has too many instance attributes, try to reduce this to get a simpler (and so easier to '
             'use) class.',
    'R0903': 'Used when class has too few public methods, so be sure it\'s really worth it.',
    'R0904': 'Used when class has too many public methods, try to reduce this to get a simpler (and so easier to use) '
             'class.',
    'R0911': 'Used when a function or method has too many return statement, making it hard to follow.',
    'R0912': 'Used when a function or method has too many branches, making it hard to follow.',
    'R0913': 'Used when a function or method takes too many arguments.',
    'R0914': 'Used when a function or method has too many local variables.',
    'R0915': 'Used when a function or method has too many statements. You should then split it in smaller functions / '
             'methods.',
    'R0916': 'Used when an if statement contains too many boolean expressions.',
    'R1701': 'Used when multiple consecutive isinstance calls can be merged into one.',
    'R1702': 'Used when a function or a method has too many nested blocks. This makes the code less understandable '
             'and maintainable.',
    'R1703': 'Used when an if statement can be replaced with \'bool(test)\'.',
    'R1704': 'Used when a local name is redefining an argument, which might suggest a potential error. This is taken '
             'in account only for a handful of name binding operations, such as for iteration, with statement '
             'assignment and exception handler assignment.',
    'R1705': 'Used in order to highlight an unnecessary block of code following an if containing a return statement. '
             'As such, it will warn when it encounters an else following a chain of ifs, all of them containing a '
             'return statement.',
    'R1706': 'Used when one of known pre-python 2.5 ternary syntax is used.',
    'R1707': 'In Python, a tuple is actually created by the comma symbol, not by the parentheses. Unfortunately, '
             'one can actually create a tuple by misplacing a trailing comma, which can lead to potential weird bugs '
             'in your code. You should always use parentheses explicitly for creating a tuple.',
    'R1708': 'According to PEP479, the raise of StopIteration to end the loop of a generator may lead to hard to find '
             'bugs. This PEP specify that raise StopIteration has to be replaced by a simple return statement',
    'R1709': 'Emitted when redundant pre-python 2.5 ternary syntax is used.',
    'R1710': 'According to PEP8, if any return statement returns an expression, any return statements where no value '
             'is returned should explicitly state this as return None, and an explicit return statement should be '
             'present at the end of the function (if reachable)',
    'R1711': 'Emitted when a single "return" or "return None" statement is found at the end of function or method '
             'definition. This statement can safely be removed because Python will implicitly return None',
    'R1712': 'You do not have to use a temporary variable in order to swap variables. Using "tuple unpacking" to '
             'directly swap variables makes the intention more clear.',
    'R1713': 'Using str.join(sequence) is faster, uses less memory and increases readability compared to for-loop '
             'iteration.',
    'R1714': 'To check if a variable is equal to one of many values,combine the values into a tuple and check if the '
             'variable is contained "in" it instead of checking for equality against each of the values.This is '
             'faster and less verbose.',
    'R1715': 'Using the builtin dict.get for getting a value from a dictionary if a key is present or a default if '
             'not, is simpler and considered more idiomatic, although sometimes a bit slower',
    'R1716': 'This message is emitted when pylint encounters boolean operation like"a < b and b < c", suggesting '
             'instead to refactor it to "a < b < c"',
    'R1717': 'Although there is nothing syntactically wrong with this code, it is hard to read and can be simplified '
             'to a dict comprehension.Also it is faster since you don\'t need to create another transient list',
    'R1718': 'Although there is nothing syntactically wrong with this code, it is hard to read and can be simplified '
             'to a set comprehension.Also it is faster since you don\'t need to create another transient list',
    'R1719': 'Used when an if expression can be replaced with \'bool(test)\'.',
    'R1720': 'Used in order to highlight an unnecessary block of code following an if containing a raise statement. '
             'As such, it will warn when it encounters an else following a chain of ifs, all of them containing a '
             'raise statement.',

    # warnings for stylistic issues, or minor programming issues
    'W0101': 'Used when there is some code behind a "return" or "raise" statement, which will never be accessed.',
    'W0102': 'Used when a mutable value as list or dictionary is detected in a default value for an argument.',
    'W0104': 'Used when a statement doesn\'t have (or at least seems to) any effect.',
    'W0105': 'Used when a string is used as a statement (which of course has no effect). This is a particular case of '
             'W0104 with its own message so you can easily disable it if you\'re using those strings as '
             'documentation, instead of comments.',
    'W0106': 'Used when an expression that is not a function call is assigned to nothing. Probably something else was '
             'intended.',
    'W0107': 'Used when a "pass" statement that can be avoided is encountered.',
    'W0108': 'Used when the body of a lambda expression is a function call on the same argument list as the lambda '
             'itself; such lambda expressions are in all but a few cases replaceable with the function being called '
             'in the body of the lambda.',
    'W0109': 'Used when a dictionary expression binds the same key multiple times.',
    'W0111': 'Used when assignment will become invalid in future Python release due to introducing new keyword.',
    'W0120': 'Loops should only have an else clause if they can exit early with a break statement, otherwise the '
             'statements under else should be on the same scope as the loop itself.',
    'W0122': 'Used when you use the "exec" statement (function for Python 3), to discourage its usage. That doesn\'t '
             'mean you cannot use it !',
    'W0123': 'Used when you use the "eval" function, to discourage its usage. Consider using `ast.literal_eval` for '
             'safely evaluating strings containing Python expressions from untrusted sources.',
    'W0124': 'Emitted when a `with` statement component returns multiple values and uses name binding with `as` only '
             'for a part of those values, as in with ctx() as a, b. This can be misleading, since it\'s not clear if '
             'the context manager returns a tuple or if the node without a name binding is another context manager.',
    'W0125': 'Emitted when a conditional statement (If or ternary if) uses a constant value for its test. This might '
             'not be what the user intended to do.',
    'W0143': 'This message is emitted when pylint detects that a comparison with a callable was made, which might '
             'suggest that some parenthesis were omitted, resulting in potential unwanted behaviour.',
    'W0150': 'Used when a break or a return statement is found inside the finally clause of a try...finally block: '
             'the exceptions raised in the try clause will be silently swallowed instead of being re-raised.',
    'W0199': 'A call of assert on a tuple will always evaluate to true if the tuple is not empty, and will always '
             'evaluate to false if it is.',
    'W0201': 'Used when an instance attribute is defined outside the __init__ method.',
    'W0211': 'Used when a static method has "self" or a value specified in valid- classmethod-first-arg option or '
             'valid-metaclass-classmethod-first-arg option as first argument.',
    'W0212': 'Used when a protected member (i.e. class member with a name beginning with an underscore) is access '
             'outside the class or a descendant of the class where it\'s defined.',
    'W0221': 'Used when a method has a different number of arguments than in the implemented interface or in an '
             'overridden method.',
    'W0222': 'Used when a method signature is different than in the implemented interface or in an overridden method.',
    'W0223': 'Used when an abstract method (i.e. raise NotImplementedError) is not overridden in concrete class.',
    'W0231': 'Used when an ancestor class method has an __init__ method which is not called by a derived class.',
    'W0232': 'Used when a class has no __init__ method, neither its parent classes.',
    'W0233': 'Used when an __init__ method is called on a class which is not in the direct ancestors for the analysed '
             'class.',
    'W0235': 'Used whenever we can detect that an overridden method is useless, relying on super() delegation to do '
             'the same thing as another method from the MRO.',
    'W0301': 'Used when a statement is ended by a semi-colon (";"), which isn\'t necessary (that\'s python, not C ;).',
    'W0311': 'Used when an unexpected number of indentation\'s tabulations or spaces has been found.',
    'W0312': 'Used when there are some mixed tabs and spaces in a module.',
    'W0401': 'Used when `from module import *` is detected.',
    'W0402': 'Used a module marked as deprecated is imported.',
    'W0404': 'Used when a module is reimported multiple times.',
    'W0406': 'Used when a module is importing itself.',
    'W0410': 'Python 2.5 and greater require __future__ import to be the first non docstring statement in the module.',
    'W0511': 'Used when a warning note as FIXME or XXX is detected.',
    'W0601': 'Used when a variable is defined through the "global" statement but the variable is not defined in the '
             'module scope.',
    'W0602': 'Used when a variable is defined through the "global" statement but no assignment to this variable is '
             'done.',
    'W0603': 'Used when you use the "global" statement to update a global variable. Pylint just try to discourage '
             'this usage. That doesn\'t mean you cannot use it !',
    'W0604': 'Used when you use the "global" statement at the module level since it has no effect',
    'W0611': 'Used when an imported module or variable is not used.',
    'W0612': 'Used when a variable is defined but not used.',
    'W0613': 'Used when a function or method argument is not used.',
    'W0614': 'Used when an imported module or variable is not used from a `\'from X import *\'` style import.',
    'W0621': 'Used when a variable\'s name hides a name defined in the outer scope.',
    'W0622': 'Used when a variable or function override a built-in.',
    'W0623': 'Used when an exception handler assigns the exception to an existing name',
    'W0631': 'Used when a loop variable (i.e. defined by a for loop or a list comprehension or a generator '
             'expression) is used outside the loop.',
    'W0632': 'Used when there is an unbalanced tuple unpacking in assignment',
    'W0640': 'A variable used in a closure is defined in a loop. This will result in all closures using the same '
             'value for the closed-over variable.',
    'W0641': 'Used when a variable is defined but might not be used. The possibility comes from the fact that locals('
             ') might be used, which could consume or not the said variable',
    'W0642': 'Invalid assignment to self or cls in instance or class method respectively.',
    'W0702': 'Used when an except clause doesn\'t specify exceptions type to catch.',
    'W0703': 'Used when an except catches a too general exception, possibly burying unrelated errors.',
    'W0705': 'Used when an except catches a type that was already caught by a previous handler.',
    'W0706': 'Used when an except handler uses raise as its first or only operator. This is useless because it raises '
             'back the exception immediately. Remove the raise operator or the entire try-except-raise block!',
    'W0711': 'Used when the exception to catch is of the form "except A or B:". If intending to catch multiple, '
             'rewrite as "except (A, B):"',
    'W0715': 'Used when passing multiple arguments to an exception constructor, the first of them a string literal '
             'containing what appears to be placeholders intended for formatting',
    'W0716': 'Used when an operation is done against an exception, but the operation is not valid for the exception '
             'in question. Usually emitted when having binary operations between exceptions in except handlers.',
    'W1113': 'When defining a keyword argument before variable positional arguments, one can end up in having '
             'multiple values passed for the aforementioned parameter in case the method is called with keyword '
             'arguments.',
    'W1201': 'Used when a logging statement has a call form of "logging.<logging method>(format_string % ('
             'format_args...))". Such calls should leave string interpolation to the logging method itself and be '
             'written "logging.<logging method>(format_string, format_args...)" so that the program may avoid '
             'incurring the cost of the interpolation in those cases in which no message will be logged. For more, '
             'see http://www.python.org/dev/peps/pep-0282/.',
    'W1202': 'Used when a logging statement has a call form of "logging.<logging method>(format_string.format('
             'format_args...))". Such calls should use % formatting instead, but leave interpolation to the logging '
             'function by passing the parameters as arguments.',
    'W1203': 'Used when a logging statement has a call form of "logging.method(f"..."))". Such calls should use % '
             'formatting instead, but leave interpolation to the logging function by passing the parameters as '
             'arguments.',
    'W1300': 'Used when a format string that uses named conversion specifiers is used with a dictionary whose keys '
             'are not all strings.',
    'W1301': 'Used when a format string that uses named conversion specifiers is used with a dictionary that contains '
             'keys not required by the format string.',
    'W1302': 'Used when a PEP 3101 format string is invalid.',
    'W1303': 'Used when a PEP 3101 format string that uses named fields doesn\'t '
             'receive one or more required keywords.',
    'W1304': 'Used when a PEP 3101 format string that uses named fields is used with an argument that is not required '
             'by the format string.',
    'W1305': 'Used when a PEP 3101 format string contains both automatic field numbering and manual '
             'field specification.',
    'W1306': 'Used when a PEP 3101 format string uses an attribute specifier ({0.length}), but the argument passed '
             'for formatting doesn\'t have that attribute.',
    'W1307': 'Used when a PEP 3101 format string uses a lookup specifier ({a[1]}), but the argument passed for '
             'formatting doesn\'t contain or doesn\'t have that key as an attribute.',
    'W1308': 'Used when we detect that a string formatting is repeating an argument instead of using named string '
             'arguments',
    'W1401': 'Used when a backslash is in a literal string but not as an escape.',
    'W1402': 'Used when an escape like \\u is encountered in a byte string where it has no effect.',
    'W1403': 'String literals are implicitly concatenated in a '
             'literal iterable definition : maybe a comma is missing ?',
    'W1501': 'Python supports: r, w, a[, x] modes with b, +, and U (only with r) options. '
             'See http://docs.python.org/2/library/functions.html#open',
    'W1503': 'The first argument of assertTrue and assertFalse is a condition. If a constant is passed as parameter, '
             'that condition will be always true. In this case a warning should be emitted.',
    'W1505': 'The method is marked as deprecated and will be removed in a future version of Python. Consider looking '
             'for an alternative in the documentation.',
    'W1506': 'The warning is emitted when a threading.Thread class is instantiated without the target function being '
             'passed. By default, the first parameter is the group param, not the target param.',
    'W1507': 'os.environ is not a dict object but proxy object, so shallow copy has still effects on original object. '
             'See https://bugs.python.org/issue15373 for reference.',
    'W1508': 'Env manipulation functions return None or str values. Supplying anything different as a default may '
             'cause bugs. See https://docs.python.org/3/library/os.html#os.getenv.',
    'W1509': 'The preexec_fn parameter is not safe to use in the presence of threads in your application. The child '
             'process could deadlock before exec is called. If you must use it, keep it trivial! Minimize the number '
             'of libraries you call into.https://docs.python.org/3/library/subprocess.html#popen-constructor',
    # miss some inspections that were missed from Python 3

    'I0001': 'Used to inform that a built-in module has not been checked using the raw checkers.',
    'I0010': 'Used when an inline option is either badly formatted or can\'t be used inside modules.',
    'I0011': 'Used when an inline option disables a message or a messages category.',
    'I0013': 'Used to inform that the file will not be checked',
    'I0020': 'A message was triggered on a line, but suppressed explicitly by a disable= comment in the file. '
             'This message is not generated for messages that are ignored due to configuration settings.',
    'I0021': 'Reported when a message is explicitly disabled for a line or a block of code, but never triggered.',
    'I0022': 'Some inline pylint options have been renamed or reworked, only the most recent form should be used. '
             'NOTE:skip-all is only available with pylint >= 0.26',
    'I0023': 'Used when a message is enabled or disabled by id.',
    'I1101': 'Used when a variable is accessed for non-existent member of C extension. Due to unavailability of source '
             'static analysis is impossible, but it may be performed by introspecting living objects in run-time.',
}

# According to the pylint inspector config
PYLINT_DISABLED_ISSUES = {
    'C0103',  # invalid-name
    'C0111',  # missing-docstring
    'C0301',  # line-too-long
    'C0304',  # missing-final-newline
    'E1601',  # print-statement
    'E1602',  # parameter-unpacking
    'E1603',  # unpacking-in-except
    'E1604',  # old-raise-syntax
    'E1605',
    'I0001',  # raw-checker-failed
    'I0010',  # bad-inline-option
    'I0011',  # locally-disabled
    'I0013',  # file-ignored
    'I0020',  # suppressed-message
    'I0021',  # useless-suppression
    'I0022',  # deprecated-pragma
    'I0023',  # use-symbolic-message-instead
    'R0901',  # too-many-ancestors
    'R0902',  # too-many-instance-attributes
    'R0903',  # too-few-public-methods
    'R0904',  # too-many-public-methods,
    'R0911',  # too-many-return-statements
    'R0912',  # too-many-branches
    'R0913',  # too-many-arguments
    'R0914',  # too-many-locals
    'R0916',  # too-many-boolean-expressions
    'W1601',  # apply-builtin
    'W1602',  # basestring-builtin
    'W1603',  # buffer-builtin
    'W1604',  # cmp-builtin
    'W1605',  # coerce-builtin
    'W1606',
    'W1607',  # file-builtin
    'W1608',  # long-builtin
    'W1609',  # raw_input-builtin
    'W1610',  # reduce-builtin
    'W1611',
    'W1612',  # unicode-builtin
    'W1613',
    'W1614',  # coerce-method
    'W1615',
    'W1616',
    'W1617',
    'W1618',  # no-absolute-import
    'W1619',  # old-division
    'W1620',  # dict-iter-method
    'W1621',  # dict-view-method
    'W1622',  # next-method-called
    'W1623',
    'W1624',  # indexing-exception
    'W1625',  # raising-string
    'W1626',  # reload-builtin
    'W1627',  # oct-method
    'W1628',  # hex-method
    'W1629',  # nonzero-method
    'W1630',  # cmp-method
    'W1632',  # input-builtin
    'W1633',  # round-builtin
    'W1634',  # intern-builtin
    'W1635',
    'W1636',  # map-builtin-not-iterating
    'W1637',  # zip-builtin-not-iterating
    'W1638',  # range-builtin-not-iterating
    'W1639',  # filter-builtin-not-iterating
    'W1640',  # using-cmp-argument
    'W1641',  # eq-without-hash
    'W1642',  # div-method
    'W1643',
    'W1644',
    'W1645',  # exception-message-attribute
    'W1646',
    'W1647',  # sys-max-int
    'W1648',  # bad-python3-import
    'W1649',  # deprecated-string-function
    'W1650',  # deprecated-str-translate-call
    'W1651',  # deprecated-itertools-function
    'W1652',  # deprecated-types-field
    'W1653',  # next-method-defined
    'W1654',  # dict-items-not-iterating
    'W1655',  # dict-keys-not-iterating
    'W1656',  # dict-values-not-iterating
    'W1657',  # deprecated-operator-function
    'W1658',  # deprecated-urllib-function
    'W1659',
    'W1660',  # deprecated-sys-function
    'W1661',  # exception-escape
    'W1662',  # comprehension-escape,
    'W0603',  # global-statement
    'C0413',  # wrong-import-position
    'R0915',  # too-many-statements
    'C0327',  # mixed-line-endings
    'E0401',  # import-error
    'C0303',  # trailing-whitespace
    'R1705',  # no-else-return
    'R1720',  # no-else-raise
}
