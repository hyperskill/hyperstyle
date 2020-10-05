from typing import Dict

from review.inspectors.issue import IssueType

ISSUE_CLASS_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # Kotlin | Java interop issues
    'Call of Java mutator method on immutable Kotlin collection':
        IssueType.ERROR_PRONE,
    'Function or property has platform type':
        IssueType.ERROR_PRONE,
    'Kotlin non-const property used as Java constant':
        IssueType.ERROR_PRONE,
    'Not-null extension receiver of inline function can be made nullable':
        IssueType.ERROR_PRONE,
    'Package name does not match containing directory':
        IssueType.ERROR_PRONE,
    'Unsafe call of inline function with nullable extension receiver':
        IssueType.ERROR_PRONE,
    'Usage of Kotlin internal declarations from Java':
        IssueType.ERROR_PRONE,

    # Kotlin | Naming conventions
    'Class naming convention':
        IssueType.CODE_STYLE,
    'Const property naming convention':
        IssueType.CODE_STYLE,
    'Enum entry naming convention':
        IssueType.CODE_STYLE,
    'Function naming convention':
        IssueType.CODE_STYLE,
    'Local variable naming convention':
        IssueType.CODE_STYLE,
    'Object property naming convention':
        IssueType.CODE_STYLE,
    'Package naming convention':
        IssueType.CODE_STYLE,
    'Private property naming convention':
        IssueType.CODE_STYLE,
    'Property naming convention':
        IssueType.CODE_STYLE,
    'Test function naming convention':
        IssueType.CODE_STYLE,

    # Kotlin | Other issues
    '@Deprecated annotation without \'replaceWith\' argument':
        IssueType.BEST_PRACTICES,
    'Diagnostic name should be replaced':
        IssueType.BEST_PRACTICES,
    'Missing KDoc comments for public declarations':
        IssueType.BEST_PRACTICES,
    'Overriding deprecated member':
        IssueType.BEST_PRACTICES,
    'Public API declaration has implicit return type':
        IssueType.BEST_PRACTICES,
    'Replace with EnumMap':
        IssueType.BEST_PRACTICES,

    # Kotlin | Probable bugs
    'Ambiguous coroutineContext due to CoroutineScope receiver of suspend '
    'function':
        IssueType.ERROR_PRONE,
    'Ambiguous unary operator use with number constant':
        IssueType.ERROR_PRONE,
    'Array property in data class':
        IssueType.ERROR_PRONE,
    'Assignment of variable to itself':
        IssueType.ERROR_PRONE,
    'Augmented assignment creates a new collection under the hood':
        IssueType.ERROR_PRONE,
    'Constructor has non-null self reference parameter':
        IssueType.ERROR_PRONE,
    'Convert equality check with \'NaN\' to \'isNaN\' call':
        IssueType.ERROR_PRONE,
    'Covariant \'equals()\'':
        IssueType.ERROR_PRONE,
    'Deferred result is never used':
        IssueType.ERROR_PRONE,
    'Delegating to \'var\' property':
        IssueType.ERROR_PRONE,
    'Entry point function should return Unit':
        IssueType.ERROR_PRONE,
    'equals() and hashCode() not paired':
        IssueType.ERROR_PRONE,
    'Existing backing field is not assigned by the setter':
        IssueType.ERROR_PRONE,
    'Extension property conflicting with synthetic one':
        IssueType.ERROR_PRONE,
    'Implicit (unsafe) cast from dynamic type':
        IssueType.ERROR_PRONE,
    'Implicit `Nothing?` type':
        IssueType.ERROR_PRONE,
    'Iterated elements are not used in forEach':
        IssueType.ERROR_PRONE,
    'Leaking \'this\' in constructor':
        IssueType.ERROR_PRONE,
    'Private data class constructor is exposed via the \'copy\' method':
        IssueType.ERROR_PRONE,
    'Range with start greater than endInclusive is empty':
        IssueType.ERROR_PRONE,
    'Recursive equals call':
        IssueType.ERROR_PRONE,
    'Recursive property accessor':
        IssueType.ERROR_PRONE,
    'Replace \'==\' with \'Arrays.equals\'':
        IssueType.ERROR_PRONE,
    'Sealed sub-class without state and overridden equals':
        IssueType.ERROR_PRONE,
    'Suspicious \'var\' property: its setter does not influence its '
    'getter result':
        IssueType.ERROR_PRONE,
    'Suspicious callable reference used as lambda result':
        IssueType.ERROR_PRONE,
    'Suspicious combination of == and ===':
        IssueType.ERROR_PRONE,
    'Throwable not thrown':
        IssueType.ERROR_PRONE,
    'Unresolved reference in KDoc':
        IssueType.ERROR_PRONE,
    'Unused return value of a function with lambda expression body':
        IssueType.ERROR_PRONE,
    'Useless call on collection type':
        IssueType.ERROR_PRONE,
    'Useless call on not-null type':
        IssueType.ERROR_PRONE,
    'Variable in destructuring declaration uses name of a wrong data class '
    'property':
        IssueType.ERROR_PRONE,

    # Kotlin | Redundant constructs
    'Condition of \'if\' expression is constant':
        IssueType.BEST_PRACTICES,
    'Constructor parameter is never used as a property':
        IssueType.BEST_PRACTICES,
    'Explicitly given type is redundant here':
        IssueType.CODE_STYLE,
    'Null-checks replaceable with safe-calls':
        IssueType.BEST_PRACTICES,
    'Property is explicitly assigned to constructor parameter':
        IssueType.BEST_PRACTICES,
    'Redundant \'if\' statement':
        IssueType.BEST_PRACTICES,
    'Redundant \'requireNotNull\' or \'checkNotNull\' call':
        IssueType.BEST_PRACTICES,
    'Redundant \'return\' label':
        IssueType.BEST_PRACTICES,
    'Redundant \'suspend\' modifier':
        IssueType.BEST_PRACTICES,
    'Redundant \'Unit\'':
        IssueType.CODE_STYLE,
    'Redundant \'Unit\' return type':
        IssueType.CODE_STYLE,
    'Redundant \'with\' call':
        IssueType.BEST_PRACTICES,
    'Redundant Companion reference':
        IssueType.BEST_PRACTICES,
    'Redundant curly braces in string template':
        IssueType.CODE_STYLE,
    'Redundant double negation':
        IssueType.BEST_PRACTICES,
    'Redundant enum constructor invocation':
        IssueType.BEST_PRACTICES,
    'Redundant explicit \'this\'':
        IssueType.BEST_PRACTICES,
    'Redundant lambda arrow':
        IssueType.BEST_PRACTICES,
    'Redundant modality modifier':
        IssueType.BEST_PRACTICES,
    'Redundant overriding method':
        IssueType.BEST_PRACTICES,
    'Redundant property getter':
        IssueType.BEST_PRACTICES,
    'Redundant property setter':
        IssueType.BEST_PRACTICES,
    'Redundant SAM constructor':
        IssueType.BEST_PRACTICES,
    'Redundant semicolon':
        IssueType.CODE_STYLE,
    'Redundant setter parameter type':
        IssueType.BEST_PRACTICES,
    'Redundant spread operator':
        IssueType.BEST_PRACTICES,
    'Redundant visibility modifier':
        IssueType.BEST_PRACTICES,
    'Remove empty constructor body':
        IssueType.BEST_PRACTICES,
    'Remove empty primary constructor':
        IssueType.BEST_PRACTICES,
    'Remove redundant backticks':
        IssueType.BEST_PRACTICES,
    'Remove redundant call to \'toString()\' in string template':
        IssueType.BEST_PRACTICES,
    'Remove redundant calls of conversion methods':
        IssueType.BEST_PRACTICES,
    'Remove redundant qualifier name':
        IssueType.BEST_PRACTICES,
    'Remove redundant string template':
        IssueType.BEST_PRACTICES,
    'Remove unnecessary parentheses from function call with lambda':
        IssueType.BEST_PRACTICES,
    'Replace empty class body':
        IssueType.CODE_STYLE,
    'Replace single line .let':
        IssueType.BEST_PRACTICES,
    'Simplifiable \'when\'':
        IssueType.BEST_PRACTICES,
    'Unnecessary local variable':
        IssueType.BEST_PRACTICES,
    'Unnecessary supertype qualification':
        IssueType.BEST_PRACTICES,
    'Unnecessary type argument':
        IssueType.BEST_PRACTICES,
    'Unused equals expression':
        IssueType.BEST_PRACTICES,
    'Unused import directive':
        IssueType.BEST_PRACTICES,
    'Unused loop index':
        IssueType.BEST_PRACTICES,
    'Unused receiver parameter':
        IssueType.BEST_PRACTICES,
    'Unused symbol':
        IssueType.BEST_PRACTICES,
    '\'when\' has only \'else\' branch and can be simplified':
        IssueType.BEST_PRACTICES,

    # Kotlin | Style issues
    'Accessor call that can be replaced with property access syntax':
        IssueType.CODE_STYLE,
    '\'arrayOf\' call can be replaced with array literal [...]':
        IssueType.CODE_STYLE,
    '‘assert’ call can be replaced with ‘!!’ or ‘?:\'':
        IssueType.CODE_STYLE,
    'Assignment that can be replaced with operator assignment':
        IssueType.CODE_STYLE,
    'Boolean expression that can be simplified':
        IssueType.CODE_STYLE,
    'Boolean literal argument without parameter name':
        IssueType.CODE_STYLE,
    'Call chain on collection could be converted into \'Sequence\' to improve '
    'performance':
        IssueType.CODE_STYLE,
    'Call chain on collection type can be simplified':
        IssueType.CODE_STYLE,
    'Can be replaced with binary operator':
        IssueType.CODE_STYLE,
    'Can be replaced with function reference':
        IssueType.CODE_STYLE,
    'Can be replaced with lambda':
        IssueType.CODE_STYLE,
    'Cascade if can be replaced with when':
        IssueType.CODE_STYLE,
    'Class member can have \'private\' visibility':
        IssueType.BEST_PRACTICES,
    'Collection count can be converted to size':
        IssueType.CODE_STYLE,
    'Control flow with empty body':
        IssueType.BEST_PRACTICES,
    'Convert Pair constructor to \'to\' function':
        IssueType.CODE_STYLE,
    'Convert to primary constructor':
        IssueType.CODE_STYLE,
    'Convert try / finally to use() call':
        IssueType.CODE_STYLE,
    'Convert two comparisons to \'in\'':
        IssueType.CODE_STYLE,
    '\'copy\' method of data class is called without named arguments':
        IssueType.CODE_STYLE,
    'Equality check can be used instead of elvis for nullable boolean check':
        IssueType.CODE_STYLE,
    'Explicit \'get\' or \'set\' call':
        IssueType.CODE_STYLE,
    'Expression body syntax is preferable here':
        IssueType.CODE_STYLE,
    'File is not formatted according to project settings':
        IssueType.CODE_STYLE,
    'Function returning Deferred directly':
        IssueType.CODE_STYLE,
    'Function returning Result directly':
        IssueType.CODE_STYLE,
    'Function with `= { ... }` and inferred return type':
        IssueType.CODE_STYLE,
    'If-Null return/break/... foldable to \'?:\'':
        IssueType.CODE_STYLE,
    'If-Then foldable to \'?.\'':
        IssueType.CODE_STYLE,
    'If-Then foldable to \'?:\'':
        IssueType.CODE_STYLE,
    'Implicit \'this\'':
        IssueType.CODE_STYLE,
    'Java Collections static method call can be replaced with Kotlin stdlib':
        IssueType.CODE_STYLE,
    'Java Map.forEach method call should be replaced with Kotlin\'s forEach':
        IssueType.CODE_STYLE,
    'Join declaration and assignment':
        IssueType.CODE_STYLE,
    'Lambda argument inside parentheses':
        IssueType.CODE_STYLE,
    'Library function call could be simplified':
        IssueType.CODE_STYLE,
    'Local \'var\' is never modified and can be declared as \'val\'':
        IssueType.CODE_STYLE,
    'Loop can be replaced with stdlib operations':
        IssueType.CODE_STYLE,
    'Main parameter is not necessary':
        IssueType.CODE_STYLE,
    'Manually incremented index variable can be replaced with use of '
    '\'withIndex()\'':
        IssueType.CODE_STYLE,
    'map.get() with not-null assertion operator (!!)':
        IssueType.CODE_STYLE,
    'map.put() can be converted to assignment':
        IssueType.CODE_STYLE,
    'Might be \'const\'':
        IssueType.CODE_STYLE,
    'Negated boolean expression that can be simplified':
        IssueType.CODE_STYLE,
    'Nested lambda has shadowed implicit parameter':
        IssueType.CODE_STYLE,
    'Non-canonical modifier order':
        IssueType.CODE_STYLE,
    'Object literal can be converted to lambda':
        IssueType.CODE_STYLE,
    'Optionally expected annotation has no actual annotation':
        IssueType.CODE_STYLE,
    '\'protected\' visibility is effectively \'private\' in a final class':
        IssueType.CODE_STYLE,
    '\'rangeTo\' or the \'..\' call can be replaced with \'until\'':
        IssueType.CODE_STYLE,
    'Redundant \'async\' call':
        IssueType.CODE_STYLE,
    'Redundant \'else\' in \'if\'':
        IssueType.CODE_STYLE,
    'Redundant \'runCatching\' call':
        IssueType.CODE_STYLE,
    'Redundant type checks for object':
        IssueType.CODE_STYLE,
    'Remove unnecessary parentheses':
        IssueType.CODE_STYLE,
    'Replace \'!!\' with \'?:return \'':
        IssueType.CODE_STYLE,
    'Replace \'associate\' with \'associateBy\' or \'associateWith\'':
        IssueType.CODE_STYLE,
    'Replace \'toString\' with string template':
        IssueType.CODE_STYLE,
    'Replace assert boolean with assert equality':
        IssueType.CODE_STYLE,
    'Replace Java static method with Kotlin analog':
        IssueType.CODE_STYLE,
    'Replace negated \'isEmpty\' with \'isNotEmpty\'':
        IssueType.CODE_STYLE,
    'Replace Range \'start\' or \'endInclusive\' with \'first\' or \'last\'':
        IssueType.CODE_STYLE,
    'Replace size check with \'isNotEmpty()\'':
        IssueType.CODE_STYLE,
    'Replace size zero check with \'isEmpty()\'':
        IssueType.CODE_STYLE,
    'Replace with string templates':
        IssueType.CODE_STYLE,
    'Replace ’to’ with infix form':
        IssueType.CODE_STYLE,
    'Return or assignment can be lifted out':
        IssueType.CODE_STYLE,
    'Safe cast with \'return\' should be replaced with \'if\' type check':
        IssueType.CODE_STYLE,
    'Scope function can be converted to another one':
        IssueType.CODE_STYLE,
    'String concatenation that can be converted to string template':
        IssueType.CODE_STYLE,
    'Suspicious \'asDynamic\' member invocation':
        IssueType.CODE_STYLE,
    'Type parameter can have \'in\' or \'out\' variance':
        IssueType.CODE_STYLE,
    'Unlabeled return inside lambda':
        IssueType.CODE_STYLE,
    'Use destructuring declaration':
        IssueType.CODE_STYLE,
    'Variable declaration could be moved inside `when`':
        IssueType.CODE_STYLE,
    '\'when\' that can be simplified by introducing an argument':
        IssueType.CODE_STYLE,

    'Annotator': IssueType.ERROR_PRONE
}
