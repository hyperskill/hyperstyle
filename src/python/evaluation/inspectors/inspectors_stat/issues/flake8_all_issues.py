# According to https://gist.github.com/sharkykh/c76c80feadc8f33b129d846999210ba3
ALL_STANDARD_ISSUES = {
    # Indentation
    'E101': 'indentation contains mixed spaces and tabs',
    'E111': 'indentation is not a multiple of four',
    'E112': 'expected an indented block',
    'E113': 'unexpected indentation',
    'E114': 'indentation is not a multiple of four (comment)',
    'E115': 'expected an indented block (comment)',
    'E116': 'unexpected indentation (comment)',
    'E121': 'continuation line under-indented for hanging indent',
    'E122': 'continuation line missing indentation or outdented',
    'E123': 'closing bracket does not match indentation of opening bracket\'s line',
    'E124': 'closing bracket does not match visual indentation',
    'E125': 'continuation line with same indent as next logical line',
    'E126': 'continuation line over-indented for hanging indent',
    'E127': 'continuation line over-indented for visual indent',
    'E128': 'continuation line under-indented for visual indent',
    'E129': 'visually indented line with same indent as next logical line',
    'E131': 'continuation line unaligned for hanging indent',
    'E133': 'closing bracket is missing indentation',

    # Whitespace
    'E201': 'whitespace after \'(\'',
    'E202': 'whitespace before \')\'',
    'E203': 'whitespace before \':\'',
    'E211': 'whitespace before \'(\'',
    'E221': 'multiple spaces before operator',
    'E222': 'multiple spaces after operator',
    'E223': 'tab before operator',
    'E224': 'tab after operator',
    'E225': 'missing whitespace around operator',
    'E226': 'missing whitespace around arithmetic operator',
    'E227': 'missing whitespace around bitwise or shift operator',
    'E228': 'missing whitespace around modulo operator',
    'E231': 'missing whitespace after \',\', \';\', or \':\'',
    'E241': 'multiple spaces after \',\'',
    'E242': 'tab after \',\'',
    'E251': 'unexpected spaces around keyword / parameter equals',
    'E261': 'at least two spaces before inline comment',
    'E262': 'inline comment should start with \'# \'',
    'E265': 'block comment should start with \'# \'',
    'E266': 'too many leading \'#\' for block comment',
    'E271': 'multiple spaces after keyword',
    'E272': 'multiple spaces before keyword',
    'E273': 'tab after keyword',
    'E274': 'tab before keyword',
    'E275': 'missing whitespace after keyword',

    # Blank line
    'E301': 'expected 1 blank line, found 0',
    'E302': 'expected 2 blank lines, found 0',
    'E303': 'too many blank lines (3)',
    'E304': 'blank lines found after function decorator',
    'E305': 'expected 2 blank lines after end of function or class',
    'E306': 'expected 1 blank line before a nested definition',

    # Import
    'E401': 'multiple imports on one line',
    'E402': 'module level import not at top of file',

    # Line length
    'E501': 'line too long (82 > 79 characters)',
    'E502': 'the backslash is redundant between brackets',

    # Statement
    'E701': 'multiple statements on one line (colon)',
    'E702': 'multiple statements on one line (semicolon)',
    'E703': 'statement ends with a semicolon',
    'E704': 'multiple statements on one line (def)',
    'E711': 'comparison to None should be \'if cond is None:\'',
    'E712': 'comparison to True should be \'if cond is True:\' or \'if cond:\'',
    'E713': 'test for membership should be \'not in\'',
    'E714': 'test for object identity should be \'is not\'',
    'E721': 'do not compare types, use \'isinstance()\'',
    'E722': 'do not use bare except, specify exception instead',
    'E731': 'do not use variables named \'l\', \'O\', or \'I\'',
    'E741': 'do not use variables named \'l\', \'O\', or \'I\'',
    'E742': 'do not define classes named \'l\', \'O\', or \'I\'',
    'E743': 'do not define functions named \'l\', \'O\', or \'I\'',

    # Runtime
    'E901': 'SyntaxError or IndentationError',
    'E902': 'IOError',

    # Indentation warning
    'W191': 'indentation contains tabs',

    # Whitespace warning
    'W291': 'trailing whitespace',
    'W292': 'no newline at end of file',
    'W293': 'blank line contains whitespace',

    # Blank line warning
    'W391': 'blank line at end of file',

    # Line break warning
    'W503': 'line break before binary operator',
    'W504': 'line break after binary operator',
    'W505': 'doc line too long (82 > 79 characters)',

    # Deprecation warning
    'W601': '.has_key() is deprecated, use \'in\'',
    'W602': 'deprecated form of raising exception',
    'W603': '\'<>\' is deprecated, use \'!=\'',
    'W604': 'backticks are deprecated, use \'repr()\'',
    'W605': 'invalid escape sequence \'x\'',
    'W606': '\'async\' and \'await\' are reserved keywords starting with Python 3.7',

    'F401': 'module imported but unused',
    'F402': 'import module from line N shadowed by loop variable',
    'F403': '\'from module import *\' used; unable to detect undefined names',
    'F404': 'future import(s) name after other statements',
    'F405': 'name may be undefined, or defined from star imports: module',
    'F406': '\'from module import *\' only allowed at module level',
    'F407': 'an undefined __future__ feature name was imported',

    'F601': 'dictionary key name repeated with different values',
    'F602': 'dictionary key variable name repeated with different values',
    'F621': 'too many expressions in an assignment with star-unpacking',
    'F622': 'two or more starred expressions in an assignment (a, *b, *c = d)',
    'F631': 'assertion test is a tuple, which are always True',

    'F701': 'a break statement outside of a while or for loop',
    'F702': 'a continue statement outside of a while or for loop',
    'F703': 'a continue statement in a finally block in a loop',
    'F704': 'a yield or yield from statement outside of a function',
    'F705': 'a return statement with arguments inside a generator',
    'F706': 'a return statement outside of a function/method',
    'F707': 'an except: block as not the last exception handler',
    'F721': 'doctest syntax error',
    'F722': 'syntax error in forward type annotation',

    'F811': 'redefinition of unused name from line N',
    'F812': 'list comprehension redefines name from line N',
    'F821': 'undefined name name',
    'F822': 'undefined name name in __all__',
    'F823': 'local variable name ... referenced before assignment',
    'F831': 'duplicate argument name in function definition',
    'F841': 'local variable name is assigned to but never used',

    'F901': 'raise NotImplemented should be raise NotImplementedError',

    'N801': 'class names should use CapWords convention',
    'N802': 'function name should be lowercase',
    'N803': 'argument name should be lowercase',
    'N804': 'first argument of a classmethod should be named \'cls\'',
    'N805': 'first argument of a method should be named \'self\'',
    'N806': 'variable in function should be lowercase',
    'N807': 'function name should not start or end with \'__\'',
    'N811': 'constant imported as non constant',
    'N812': 'lowercase imported as non lowercase',
    'N813': 'camelcase imported as lowercase',
    'N814': 'camelcase imported as constant',
    'N815': 'mixedCase variable in class scope',
    'N816': 'mixedCase variable in global scope',
}

# According to https://pypi.org/project/flake8-bugbear/
ALL_BUGBEAR_ISSUES = {
    'B001': 'Do not use bare except:, it also catches unexpected events like memory errors, interrupts, system exit, '
            'and so on. Prefer except Exception:. If you’re sure what you’re doing, be explicit and write except '
            'BaseException:. Disable E722 to avoid duplicate warnings.',
    'B002': 'Python does not support the unary prefix increment. Writing ++n is equivalent to +(+(n)), which equals '
            'n. You meant n += 1.',
    'B003': 'Assigning to os.environ doesn’t clear the environment. Subprocesses are going to see outdated variables, '
            'in disagreement with the current process. Use os.environ.clear() or the env= argument to Popen.',
    'B004': 'Using hasattr(x, \'__call__\') to test if x is callable is unreliable. If x implements custom '
            '__getattr__ or its __call__ is itself not callable, you might get misleading results. Use callable(x) '
            'for consistent results.',
    'B005': 'Using .strip() with multi-character strings is misleading the reader. It looks like stripping a '
            'substring. Move your character set to a constant if this is deliberate. Use .replace() or regular '
            'expressions to remove string fragments.',
    'B006': 'Do not use mutable data structures for argument defaults. They are created during function definition '
            'time. All calls to the function reuse this one instance of that data structure, persisting changes '
            'between them.',
    'B007': 'Loop control variable not used within the loop body. If this is intended, start the name with an '
            'underscore.',
    'B008': 'Do not perform function calls in argument defaults. The call is performed only once at function '
            'definition time. All calls to your function will reuse the result of that definition-time function call. '
            'If this is intended, assign the function call to a module-level variable and use that variable as a '
            'default value.',
    'B009': 'Do not call getattr(x, \'attr\'), instead use normal property access: x.attr. Missing a default to '
            'getattr will cause an AttributeError to be raised for non-existent properties. There is no additional '
            'safety in using getattr if you know the attribute name ahead of time.',
    'B010': 'Do not call setattr(x, \'attr\', val), instead use normal property access: x.attr = val. There is no '
            'additional safety in using setattr if you know the attribute name ahead of time.',
    'B011': 'Do not call assert False since python -O removes these calls. Instead callers should raise '
            'AssertionError().',
    'B012': 'Use of break, continue or return inside finally blocks will silence exceptions or override return values '
            'from the try or except blocks. To silence an exception, do it explicitly in the except block. To '
            'properly use a break, continue or return refactor your code so these statements are not in the finally '
            'block.',
    'B013': 'A length-one tuple literal is redundant. Write except SomeError: instead of except (SomeError,):.',
    'B014': 'Redundant exception types in except (Exception, TypeError):. Write except Exception:, which catches '
            'exactly the same exceptions.',
    'B015': 'Pointless comparison. This comparison does nothing but waste CPU instructions. Either prepend assert or '
            'remove it.',
    'B016': 'Cannot raise a literal. Did you intend to return it or raise an Exception?',
    'B017': 'self.assertRaises(Exception): should be considered evil. It can lead to your test passing even if the '
            'code being tested is never executed due to a typo. Either assert for a more specific exception (builtin '
            'or custom), use assertRaisesRegex, or use the context manager form of assertRaises (with '
            'self.assertRaises(Exception) as ex:) with an assertion against the data available in ex.',

    # Python 3 compatibility warnings
    'B301': 'Python 3 does not include .iter* methods on dictionaries. The default behavior is to return iterables. '
            'Simply remove the iter prefix from the method. For Python 2 compatibility, also prefer the Python 3 '
            'equivalent if you expect that the size of the dict to be small and bounded. The performance regression '
            'on Python 2 will be negligible and the code is going to be the clearest. Alternatively, use six.iter* or '
            'future.utils.iter*.',
    'B302': 'Python 3 does not include .view* methods on dictionaries. The default behavior is to return viewables. '
            'Simply remove the view prefix from the method. For Python 2 compatibility, also prefer the Python 3 '
            'equivalent if you expect that the size of the dict to be small and bounded. The performance regression '
            'on Python 2 will be negligible and the code is going to be the clearest. Alternatively, use six.view* or '
            'future.utils.view*.',
    'B303': 'The __metaclass__ attribute on a class definition does nothing on Python 3. Use class MyClass(BaseClass, '
            'metaclass=...). For Python 2 compatibility, use six.add_metaclass.',
    'B304': 'sys.maxint is not a thing on Python 3. Use sys.maxsize.',
    'B305': '.next() is not a thing on Python 3. Use the next() builtin. For Python 2 compatibility, use six.next().',
    'B306': 'BaseException.message has been deprecated as of Python 2.6 and is removed in Python 3. Use str(e) to '
            'access the user-readable message. Use e.args to access arguments passed to the exception.',
}

# According to https://github.com/gforcada/flake8-builtins/blob/master/flake8_builtins.py#L49
ALL_BUILTINS_ISSUES = {
    'A001': 'variable is shadowing a python builtin',
    'A002': 'argument is shadowing a python builtin',
    'A003': 'class attribute is shadowing a python builtin',
}

# According to https://github.com/afonasev/flake8-return
ALL_RETURN_ISSUES = {
    'R501': 'do not explicitly return None in function if it is the only possible return value.',
    'R502': 'do not implicitly return None in function able to return non-None value.',
    'R503': 'missing explicit return at the end of function able to return non-None value.',
    'R504': 'unecessary variable assignement before return statement.',
}

# According to https://pypi.org/project/flake8-string-format/
ALL_FORMAT_STRING_ISSUES = {
    # Presence of implicit parameters
    'P101': 'format string does contain unindexed parameters',
    'P102': 'docstring does contain unindexed parameters',
    'P103': 'other string does contain unindexed parameters',

    # Missing values in the parameters
    'P201': 'format call uses too large index (INDEX)',
    'P202': 'format call uses missing keyword (KEYWORD)',
    'P203': 'format call uses keyword arguments but no named entries',
    'P204': 'format call uses variable arguments but no numbered entries',
    'P205': 'format call uses implicit and explicit indexes together',

    # Unused values in the parameters
    'P301': 'format call provides unused index (INDEX)',
    'P302': 'format call provides unused keyword (KEYWORD)',
}

# According to https://pypi.org/project/flake8-import-order/
ALL_IMPORT_ORDER_ISSUES = {
    'I100': 'Your import statements are in the wrong order.',
    'I101': 'The names in your from import are in the wrong order.',
    'I201': 'Missing newline between import groups.',
    'I202': 'Additional newline in a group of imports.',
}

# According to https://pypi.org/project/flake8-comprehensions/
ALL_COMPREHENSIONS_ISSUES = {
    'C400': 'Unnecessary generator - rewrite as a <list> comprehension.',
    'C401': 'Unnecessary generator - rewrite as a <set> comprehension.',
    'C402': 'Unnecessary generator - rewrite as a <dict> comprehension.',

    'C403': 'Unnecessary list comprehension - rewrite as a <set> comprehension.',
    'C404': 'Unnecessary list comprehension - rewrite as a <dict> comprehension.',

    'C405': 'Unnecessary <list> literal - rewrite as a <set> literal.',
    'C406': 'Unnecessary <tuple> literal - rewrite as a <dict> literal.',

    'C408': 'Unnecessary <dict/list/tuple> call - rewrite as a literal.',

    'C409': ' Unnecessary <list> passed to <list>() - (remove the outer call to <list>``'
            '()/rewrite as a ``<list> literal).',
    'C410': ' Unnecessary <tuple> passed to <tuple>() - (remove the outer call to <tuple>``'
            '()/rewrite as a ``<tuple> literal).',

    'C411': 'Unnecessary list call - remove the outer call to list().',

    'C413': 'Unnecessary <list/reversed> call around sorted().',

    'C414': 'Unnecessary <list/reversed/set/sorted/tuple> call within <list/set/sorted/tuple>().',

    'C415': 'Unnecessary subscript reversal of iterable within <reversed/set/sorted>().',

    'C416': 'Unnecessary <list/set> comprehension - rewrite using <list/set>().',
}

# According to https://pypi.org/project/flake8-spellcheck/
ALL_SPELLCHECK_ISSUES = {
    'SC100': 'Spelling error in comments',
    'SC200': 'Spelling error in name (e.g. variable, function, class)',
}

# According to https://wemake-python-stylegui.de/en/latest/pages/usage/violations/index.html
ALL_WPS_ISSUES = {
    # Naming
    'WPS100': 'Found wrong module name',
    'WPS101': 'Found wrong module magic name',
    'WPS102': 'Found incorrect module name pattern',
    'WPS110': 'Found wrong variable name',
    'WPS111': 'Found too short name',
    'WPS112': 'Found private name pattern',
    'WPS113': 'Found same alias import',
    'WPS114': 'Found underscored number name pattern',
    'WPS115': 'Found upper-case constant in a class',
    'WPS116': 'Found consecutive underscores name',
    'WPS117': 'Found name reserved for first argument',
    'WPS118': 'Found too long name',
    'WPS119': 'Found unicode name',
    'WPS120': 'Found regular name with trailing underscore',
    'WPS121': 'Found usage of a variable marked as unused',
    'WPS122': 'Found all unused variables definition',
    'WPS123': 'Found wrong unused variable name',
    'WPS124': 'Found unreadable characters combination',
    'WPS125': 'Found builtin shadowing',

    # Complexity
    'WPS200': 'Found module with high Jones Complexity score',
    'WPS201': 'Found module with too many imports',
    'WPS202': 'Found too many module members',
    'WPS203': 'Found module with too many imported names',
    'WPS204': 'Found overused expression',
    'WPS210': 'Found too many local variables',
    'WPS211': 'Found too many arguments',
    'WPS212': 'Found too many return statements',
    'WPS213': 'Found too many expressions',
    'WPS214': 'Found too many methods',
    'WPS215': 'Too many base classes',
    'WPS216': 'Too many decorators',
    'WPS217': 'Found too many await expressions',
    'WPS218': 'Found too many `assert` statements',
    'WPS219': 'Found too deep access level',
    'WPS220': 'Found too deep nesting',
    'WPS221': 'Found line with high Jones Complexity',
    'WPS222': 'Found a condition with too much logic',
    'WPS223': 'Found too many `elif` branches',
    'WPS224': 'Found a comprehension with too many `for` statements',
    'WPS225': 'Found too many `except` cases',
    'WPS226': 'Found string constant over-use',
    'WPS227': 'Found too long yield tuple',
    'WPS228': 'Found too long compare',
    'WPS229': 'Found too long ``try`` body length',
    'WPS230': 'Found too many public instance attributes',
    'WPS231': 'Found function with too much cognitive complexity',
    'WPS232': 'Found module cognitive complexity that is too high',
    'WPS233': 'Found call chain that is too long',
    'WPS234': 'Found overly complex annotation',
    'WPS235': 'Found too many imported names from a module',
    'WPS236': 'Found too many variables used to unpack a tuple',
    'WPS237': 'Found a too complex `f` string',
    'WPS238': 'Found too many raises in a function',

    # Consistency
    'WPS300': 'Found local folder import',
    'WPS301': 'Found dotted raw import',
    'WPS302': 'Found unicode string prefix',
    'WPS303': 'Found underscored number',
    'WPS304': 'Found partial float',
    'WPS305': 'Found `f` string',
    'WPS306': 'Found class without a base class',
    'WPS307': 'Found list comprehension with multiple `if`s',
    'WPS308': 'Found constant comparison',
    'WPS309': 'Found reversed compare order',
    'WPS310': 'Found bad number suffix',
    'WPS311': 'Found multiple `in` compares',
    'WPS312': 'Found comparison of a variable to itself',
    'WPS313': 'Found parenthesis immediately after a keyword',
    'WPS314': 'Found conditional that always evaluates the same',
    'WPS315': 'Found extra `object` in parent classes list',
    'WPS316': 'Found context manager with too many assignments',
    'WPS317': 'Found incorrect multi-line parameters',
    'WPS318': 'Found extra indentation',
    'WPS319': 'Found bracket in wrong position',
    'WPS320': 'Found multi-line function type annotation',
    'WPS321': 'Found uppercase string modifier',
    'WPS322': 'Found incorrect multi-line string',
    'WPS323': 'Found `%` string formatting',
    'WPS324': 'Found inconsistent `return` statement',
    'WPS325': 'Found inconsistent `yield` statement',
    'WPS326': 'Found implicit string concatenation',
    'WPS327': 'Found useless `continue` at the end of the loop',
    'WPS328': 'Found useless node',
    'WPS329': 'Found useless `except` case',
    'WPS330': 'Found unnecessary operator',
    'WPS332': 'Found walrus operator',
    'WPS333': 'Found implicit complex compare',
    'WPS334': 'Found reversed complex comparison',
    'WPS335': 'Found incorrect `for` loop iter type',
    'WPS336': 'Found explicit string concatenation',
    'WPS337': 'Found multiline conditions',
    'WPS338': 'Found incorrect order of methods in a class',
    'WPS339': 'Found number with meaningless zeros',
    'WPS340': 'Found exponent number with positive exponent',
    'WPS341': 'Found wrong hex number case',
    'WPS342': 'Found implicit raw string',
    'WPS343': 'Found wrong complex number suffix',
    'WPS344': 'Found explicit zero division',
    'WPS345': 'Found meaningless number operation',
    'WPS346': 'Found wrong operation sign',
    'WPS347': 'Found vague import that may cause confusion',
    'WPS348': 'Found a line that starts with a dot',
    'WPS349': 'Found redundant subscript slice',
    'WPS350': 'Found usable augmented assign pattern',
    'WPS351': 'Found unnecessary literals',
    'WPS352': 'Found multiline loop',
    'WPS353': 'Found incorrect `yield from` target',
    'WPS354': 'Found consecutive `yield` expressions',
    'WPS355': 'Found an unnecessary blank line before a bracket',
    'WPS356': 'Found an unnecessary iterable unpacking',
    'WPS357': 'Found a ``\\r`` (carriage return) line break',
    'WPS358': 'Found a float zero (0.0)',
    'WPS359': 'Found an iterable unpacking to list',
    'WPS360': 'Found an unnecessary use of a raw string',
    'WPS361': 'Found an inconsistently structured comprehension',
    'WPS362': 'Found assignment to a subscript slice',

    # Best practices
    'WPS400': 'Found wrong magic comment',
    'WPS401': 'Found wrong doc comment',
    'WPS402': 'Found `noqa` comments overuse',
    'WPS403': 'Found `noqa` comments overuse',
    'WPS404': 'Found complex default value',
    'WPS405': 'Found wrong `for` loop variable definition',
    'WPS406': 'Found wrong context manager variable definition',
    'WPS407': 'Found mutable module constant',
    'WPS408': 'Found duplicate logical condition',
    'WPS409': 'Found heterogeneous compare',
    'WPS410': 'Found wrong metadata variable',
    'WPS411': 'Found empty module',
    'WPS412': 'Found `__init__.py` module with logic',
    'WPS413': 'Found bad magic module function',
    'WPS414': 'Found incorrect unpacking target',
    'WPS415': 'Found duplicate exception',
    'WPS416': 'Found `yield` inside comprehension',
    'WPS417': 'Found non-unique item in hash',
    'WPS418': 'Found exception inherited from `BaseException`',
    'WPS419': 'Found `try`/`else`/`finally` with multiple return paths',
    'WPS420': 'Found wrong keyword',
    'WPS421': 'Found wrong function call',
    'WPS422': 'Found future import',
    'WPS423': 'Found raise NotImplemented',
    'WPS424': 'Found except `BaseException`',
    'WPS425': 'Found boolean non-keyword argument',
    'WPS426': 'Found `lambda` in loop\'s body',
    'WPS427': 'Found unreachable code',
    'WPS428': 'Found statement that has no effect',
    'WPS429': 'Found multiple assign targets',
    'WPS430': 'Found nested function',
    'WPS431': 'Found nested class',
    'WPS432': 'Found magic number',
    'WPS433': 'Found nested import',
    'WPS434': 'Found reassigning variable to itself',
    'WPS435': 'Found list multiply',
    'WPS436': 'Found protected module import',
    'WPS437': 'Found protected attribute usage',
    'WPS438': 'Found `StopIteration` raising inside generator',
    'WPS439': 'Found unicode escape in a binary string',
    'WPS440': 'Found block variables overlap',
    'WPS441': 'Found control variable used after block',
    'WPS442': 'Found outer scope names shadowing',
    'WPS443': 'Found unhashable item',
    'WPS444': 'Found incorrect keyword condition',
    'WPS445': 'Found incorrectly named keyword in the starred dict',
    'WPS446': 'Found approximate constant',
    'WPS447': 'Found alphabet as strings',
    'WPS448': 'Found incorrect exception order',
    'WPS449': 'Found float used as a key',
    'WPS450': 'Found protected object import',
    'WPS451': 'Found positional-only argument',
    'WPS452': 'Found `break` or `continue` in `finally` block',
    'WPS453': 'Found executable mismatch',
    'WPS454': 'Found wrong `raise` exception type',
    'WPS455': 'Found non-trivial expression as an argument for "except"',
    'WPS456': 'Found "NaN" as argument to float()',
    'WPS457': 'Found an infinite while loop',
    'WPS458': 'Found imports collision',
    'WPS459': 'Found comparison with float or complex number',
    'WPS460': 'Found single element destructuring',
    'WPS461': 'Forbidden inline ignore',
    'WPS462': 'Wrong multiline string usage',
    'WPS463': 'Found a getter without a return value',
    'WPS464': 'Found empty comment',
    'WPS465': 'Found likely bitwise and boolean operation mixup',
    'WPS466': 'Found new-styled decorator',

    # Refactoring
    'WPS500': 'Found `else` in a loop without `break`',
    'WPS501': 'Found `finally` in `try` block without `except`',
    'WPS502': 'Found simplifiable `if` condition',
    'WPS503': 'Found useless returning `else` statement',
    'WPS504': 'Found negated condition',
    'WPS505': 'Found nested `try` block',
    'WPS506': 'Found useless lambda declaration',
    'WPS507': 'Found useless `len()` compare',
    'WPS508': 'Found incorrect `not` with compare usage',
    'WPS509': 'Found incorrectly nested ternary',
    'WPS510': 'Found `in` used with a non-set container',
    'WPS511': 'Found separate `isinstance` calls that can be merged for',
    'WPS512': 'Found `isinstance` call with a single element tuple',
    'WPS513': 'Found implicit `elif` condition',
    'WPS514': 'Found implicit `in` condition',
    'WPS515': 'Found `open()` used without a context manager',
    'WPS516': 'Found `type()` used to compare types',
    'WPS517': 'Found pointless starred expression',
    'WPS518': 'Found implicit `enumerate()` call',
    'WPS519': 'Found implicit `sum()` call',
    'WPS520': 'Found compare with falsy constant',
    'WPS521': 'Found wrong `is` compare',
    'WPS522': 'Found implicit primitive in a form of `lambda`',
    'WPS523': 'Found incorrectly swapped variables',
    'WPS524': 'Found self assignment  with refactored assignment',
    'WPS525': 'Found wrong `in` compare with single item container',
    'WPS526': 'Found implicit `yield from` usage',
    'WPS527': 'Found not a tuple used as an argument',
    'WPS528': 'Found implicit `.items()` usage',
    'WPS529': 'Found implicit `.get()` dict usage',
    'WPS530': 'Found implicit negative index',
    'WPS531': 'Found simplifiable returning `if` condition in a function',

    # OOP
    'WPS600': 'Found subclassing a builtin',
    'WPS601': 'Found shadowed class attribute',
    'WPS602': 'Found using `@staticmethod`',
    'WPS603': 'Found using restricted magic method',
    'WPS604': 'Found incorrect node inside `class` body',
    'WPS605': 'Found method without arguments',
    'WPS606': 'Found incorrect base class',
    'WPS607': 'Found incorrect `__slots__` syntax',
    'WPS608': 'Found incorrect `super()` call',
    'WPS609': 'Found direct magic attribute usage',
    'WPS610': 'Found forbidden `async` magic method usage',
    'WPS611': 'Found forbidden `yield` magic method usage',
    'WPS612': 'Found useless overwritten method',
    'WPS613': 'Found incorrect `super()` call context: incorrect name access',
    'WPS614': 'Found descriptor applied on a function',
    'WPS615': 'Found unpythonic getter or setter',
}

# According to the flake8 inspector config
FLAKE8_DISABLED_ISSUES = {
    'W291',
    'W292',  # no newline at end of file
    'W293',
    'W503',  # line break before binary operator
    'C408',  # unnecessary (dict/list/tuple) call - rewrite as a literal
    'E501',  # line too long
    'E800',  # commented out code
    'I101',  # order of imports within a line
    'I202',  # additional new line
    'Q000',
    'E301', 'E302', 'E303', 'E304', 'E305',
    'E402',  # module level import not at top of file
    'I100',  # Import statements are in the wrong order
    # WPS: Naming
    'WPS110',  # Forbid blacklisted variable names.
    'WPS111',  # Forbid short variable or module names.
    'WPS112',  # Forbid private name pattern.
    'WPS114',  # Forbid names with underscored numbers pattern.
    'WPS125',  # Forbid variable or module names which shadow builtin names.
    # WPS: Consistency
    'WPS303',  # Forbid underscores in numbers.
    'WPS305',  # Forbid f strings.
    'WPS306',  # Forbid writing classes without base classes.
    'WPS318',  # Forbid extra indentation.
    'WPS323',  # Forbid % formatting on strings.
    'WPS324',  # Enforce consistent return statements.
    'WPS335',  # Forbid wrong for loop iter targets.
    'WPS358',  # Forbid using float zeros: 0.0.
    'WPS362',  # Forbid assignment to a subscript slice.
    # WPS: Best practices
    'WPS404',  # Forbid complex defaults.
    'WPS420',  # Forbid some python keywords.
    'WPS421',  # Forbid calling some built-in functions.(e.g., print)
    'WPS429',  # Forbid multiple assignments on the same line.
    'WPS430',  # Forbid nested functions.
    'WPS431',  # Forbid nested classes.
    'WPS435',  # Forbid multiplying lists.
    # WPS: Refactoring
    'WPS518',  # Forbid implicit enumerate() calls.
    'WPS527',  # Require tuples as arguments for frozenset.
    # WPS: OOP
    'WPS602',  # Forbid @staticmethod decorator.
    # flake8-string-format
    'P101',
    'P102',
    'P103',
    'F522',  # unused named arguments.
    'F523',  # unused positional arguments.
    'F524',  # missing argument.
    'F525',  # mixing automatic and manual numbering.
    # flake8-commas
    'C814',  # missing trailing comma in Python 2
}
