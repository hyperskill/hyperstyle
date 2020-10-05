from typing import Dict

from review.inspectors.issue import IssueType

ISSUE_CLASS_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    'Interface method clashes with method in \'java.lang.Object\'':
        IssueType.BEST_PRACTICES,

    '\'Optional\' used as field or parameter type':
        IssueType.BEST_PRACTICES,

    'Incompatible bitwise mask operation':
        IssueType.ERROR_PRONE,

    'Pointless bitwise expression':
        IssueType.BEST_PRACTICES,

    'Shift operation by inappropriate constant':
        IssueType.ERROR_PRONE,

    'Abstract class may be interface':
        IssueType.BEST_PRACTICES,

    'Field can be local':
        IssueType.BEST_PRACTICES,

    'Parameter can be local':
        IssueType.BEST_PRACTICES,

    '\'private\' method declared \'final\'':
        IssueType.BEST_PRACTICES,

    '\'static\' method declared \'final\'':
        IssueType.BEST_PRACTICES,

    'Deprecated API usage':
        IssueType.BEST_PRACTICES,

    'Usage of API marked for removal':
        IssueType.ERROR_PRONE,

    'Deprecated member is still used':
        IssueType.BEST_PRACTICES,

    'Deprecated method is still used':
        IssueType.BEST_PRACTICES,

    'Javac quirks':
        IssueType.ERROR_PRONE,

    'Unchecked warning':
        IssueType.ERROR_PRONE,

    # Java language level migration aids
    '\'compare()\' method can be used to compare numbers':
        IssueType.BEST_PRACTICES,

    '\'if\' replaceable with \'switch\'':
        IssueType.BEST_PRACTICES,

    'Usages of API which isn\'t available at the configured language level':
        IssueType.ERROR_PRONE,

    # To Java 5
    'Raw use of parameterized class': IssueType.BEST_PRACTICES,
    'Unnecessary boxing': IssueType.BEST_PRACTICES,
    'Unnecessary unboxing': IssueType.BEST_PRACTICES,

    # To Java 7
    '\'equals()\' expression replaceable by \'Objects.equals()\' expression':
        IssueType.BEST_PRACTICES,

    'Explicit type can be replaced with <>':
        IssueType.BEST_PRACTICES,

    'Identical \'catch\' branches in \'try\' statement':
        IssueType.BEST_PRACTICES,

    '\'try finally\' replaceable with \'try\' with resources':
        IssueType.BEST_PRACTICES,

    # To Java 8
    'Anonymous type can be replaced with lambda':
        IssueType.BEST_PRACTICES,

    'Anonymous type can be replaced with method reference':
        IssueType.BEST_PRACTICES,

    'Anonymous type has shorter lambda alternative':
        IssueType.BEST_PRACTICES,

    'Comparator combinator can be used':
        IssueType.BEST_PRACTICES,

    'Loop can be replaced with Collection.removeIf()':
        IssueType.BEST_PRACTICES,

    # To Java 9
    'Immutable collection creation can be replaced with collection factory call':
        IssueType.BEST_PRACTICES,

    'Null check can be replaced with method call':
        IssueType.BEST_PRACTICES,

    # Java | Abstraction issues
    'Cast to a concrete class':
        IssueType.BEST_PRACTICES,
    'Chain of \'instanceof\' checks':
        IssueType.BEST_PRACTICES,
    'Class references one of its subclasses':
        IssueType.BEST_PRACTICES,
    'Collection declared by class, not interface':
        IssueType.BEST_PRACTICES,
    'Feature envy':
        IssueType.BEST_PRACTICES,
    '\'instanceof\' a concrete class':
        IssueType.BEST_PRACTICES,
    '\'instanceof\' check for \'this\'':
        IssueType.BEST_PRACTICES,
    'Local variable of concrete class':
        IssueType.BEST_PRACTICES,
    'Magic number':
        IssueType.BEST_PRACTICES,
    'Method parameter of concrete class':
        IssueType.BEST_PRACTICES,
    'Method return of concrete class':
        IssueType.BEST_PRACTICES,
    'Overly strong type cast':
        IssueType.BEST_PRACTICES,
    'Private method only used from inner class':
        IssueType.BEST_PRACTICES,
    '\'public\' method not exposed in interface':
        IssueType.BEST_PRACTICES,
    '\'public\' method with \'boolean\' parameter':
        IssueType.BEST_PRACTICES,
    'Static field of concrete class':
        IssueType.BEST_PRACTICES,
    'Static method only used from one other class':
        IssueType.BEST_PRACTICES,
    'Type may be weakened':
        IssueType.BEST_PRACTICES,
    'Type of instance field is concrete class':
        IssueType.BEST_PRACTICES,

    # Java | Assignment issues
    'Assignment replaceable with operator assignment':
        IssueType.BEST_PRACTICES,
    'Assignment to \'for\' loop parameter':
        IssueType.ERROR_PRONE,
    'Assignment to catch block parameter':
        IssueType.ERROR_PRONE,
    'Assignment to lambda parameter':
        IssueType.ERROR_PRONE,
    'Assignment to method parameter':
        IssueType.ERROR_PRONE,
    'Assignment to static field from instance context':
        IssueType.ERROR_PRONE,
    'Assignment used as condition':
        IssueType.ERROR_PRONE,
    'Constructor assigns value to field defined in superclass':
        IssueType.ERROR_PRONE,
    '\'null\' assignment':
        IssueType.BEST_PRACTICES,
    'Result of assignment used':
        IssueType.BEST_PRACTICES,
    'Value of ++ or -- used':
        IssueType.BEST_PRACTICES,

    # Java | Class metric
    'Anonymous inner class with too many methods':
        IssueType.BEST_PRACTICES,
    'Class too deep in inheritance tree':
        IssueType.BEST_PRACTICES,
    'Class with too many constructors':
        IssueType.BEST_PRACTICES,
    'Class with too many fields':
        IssueType.BEST_PRACTICES,
    'Class with too many methods':
        IssueType.BEST_PRACTICES,
    'Inner class too deeply nested':
        IssueType.BEST_PRACTICES,
    'Overly complex anonymous class':
        IssueType.BEST_PRACTICES,
    'Overly complex class':
        IssueType.BEST_PRACTICES,
    'Overly coupled class':
        IssueType.BEST_PRACTICES,

    # Java | Class structure
    'Anonymous inner class':
        IssueType.BEST_PRACTICES,
    'Class may extend adapter instead of implementing listener':
        IssueType.BEST_PRACTICES,
    'Class name differs from file name':
        IssueType.BEST_PRACTICES,
    'Class with only \'private\' constructors should be declared \'final\'':
        IssueType.BEST_PRACTICES,
    'Constant declared in abstract class':
        IssueType.BEST_PRACTICES,
    'Constant declared in interface':
        IssueType.BEST_PRACTICES,
    'Empty class':
        IssueType.BEST_PRACTICES,
    '\'final\' class':
        IssueType.BEST_PRACTICES,
    '\'final\' method':
        IssueType.BEST_PRACTICES,
    '\'final\' method in \'final\' class':
        IssueType.BEST_PRACTICES,
    'Inner class of interface':
        IssueType.BEST_PRACTICES,
    'Interface may be annotated @FunctionalInterface':
        IssueType.BEST_PRACTICES,
    'Limited-scope inner class':
        IssueType.BEST_PRACTICES,
    'Marker interface':
        IssueType.BEST_PRACTICES,
    'Method returns per-class constant':
        IssueType.BEST_PRACTICES,
    'Multiple top level classes in single file':
        IssueType.BEST_PRACTICES,
    'No-op method in abstract class':
        IssueType.BEST_PRACTICES,
    'Non-\'final\' field in enum':
        IssueType.BEST_PRACTICES,
    'Non-\'static\' initializer':
        IssueType.BEST_PRACTICES,
    '\'protected\' member in \'final\' class':
        IssueType.BEST_PRACTICES,
    '\'public\' constructor':
        IssueType.BEST_PRACTICES,
    '\'public\' constructor in non-public class':
        IssueType.BEST_PRACTICES,
    'Singleton':
        IssueType.BEST_PRACTICES,
    '\'static\', non-\'final\' field':
        IssueType.BEST_PRACTICES,

    'Utility class':
        IssueType.BEST_PRACTICES,
    'Utility class can be \'enum\'':
        IssueType.BEST_PRACTICES,
    'Utility class is not \'final\'':
        IssueType.BEST_PRACTICES,
    'Utility class with \'public\' constructor':
        IssueType.BEST_PRACTICES,
    'Utility class without \'private\' constructor':
        IssueType.BEST_PRACTICES,

    # Java | Cloning issues
    '\'clone()\' does not declare \'CloneNotSupportedException\'':
        IssueType.ERROR_PRONE,
    '\'clone()\' instantiates objects with constructor':
        IssueType.ERROR_PRONE,
    '\'clone()\' method in non-Cloneable class':
        IssueType.ERROR_PRONE,
    '\'clone()\' method not \'public\'':
        IssueType.ERROR_PRONE,
    '\'clone()\' should have return type equal to the class it contains':
        IssueType.ERROR_PRONE,
    'Cloneable class without \'clone()\' method':
        IssueType.ERROR_PRONE,
    'Use of \'clone()\' or \'Cloneable\'':
        IssueType.BEST_PRACTICES,

    # Java | Code maturity
    'Call to \'printStackTrace()\'':
        IssueType.BEST_PRACTICES,
    'Call to \'Thread.dumpStack()\'':
        IssueType.BEST_PRACTICES,
    'Inspection suppression annotation':
        IssueType.BEST_PRACTICES,
    '\'Throwable\' printed to \'System.out\'':
        IssueType.BEST_PRACTICES,
    'Use of obsolete collection type':
        IssueType.BEST_PRACTICES,
    'Use of obsolete date-time API':
        IssueType.BEST_PRACTICES,
    'Use of System.out or System.err':
        IssueType.BEST_PRACTICES,

    # Java | Code style issues
    'Array can be replaced with enum values':
        IssueType.CODE_STYLE,
    'Array creation without \'new\' expression':
        IssueType.CODE_STYLE,
    '\'assert\' message is not a String':
        IssueType.CODE_STYLE,
    'Assignment can be joined with declaration':
        IssueType.CODE_STYLE,
    'Block marker comment':
        IssueType.CODE_STYLE,
    'C-style array declaration':
        IssueType.CODE_STYLE,
    'Call to \'String.concat()\' can be replaced with \'+\'':
        IssueType.CODE_STYLE,
    'Can use bounded wildcard':
        IssueType.CODE_STYLE,
    'Chained equality comparisons':
        IssueType.CODE_STYLE,
    'Chained method calls':
        IssueType.CODE_STYLE,
    'Class explicitly extends \'java.lang.Object\'':
        IssueType.CODE_STYLE,
    'Code block contains single statement':
        IssueType.CODE_STYLE,
    'Conditional can be replaced with Optional':
        IssueType.CODE_STYLE,
    'Confusing octal escape sequence':
        IssueType.CODE_STYLE,
    'Constant expression can be evaluated':
        IssueType.CODE_STYLE,
    'Constant on the wrong side of comparison':
        IssueType.CODE_STYLE,
    'Control flow statement without braces':
        IssueType.CODE_STYLE,
    'Diamond can be replaced with explicit type arguments':
        IssueType.CODE_STYLE,
    '\'equals()\' called on Enum value':
        IssueType.CODE_STYLE,
    '\'expression.equals(\'literal\')\' rather '
    'than \'\'literal\'.equals(expression)\'':
        IssueType.CODE_STYLE,
    'Field assignment can be moved to initializer':
        IssueType.CODE_STYLE,
    'Field may be \'final\'':
        IssueType.CODE_STYLE,
    'If statement can be replaced with ?:, && or || expression':
        IssueType.CODE_STYLE,
    'Implicit call to \'super()\'':
        IssueType.CODE_STYLE,
    '\'indexOf()\' expression is replaceable with \'contains()\'':
        IssueType.CODE_STYLE,
    'Instance field access not qualified with \'this\'':
        IssueType.CODE_STYLE,
    'Instance method call not qualified with \'this\'':
        IssueType.CODE_STYLE,
    'Labeled switch rule can have code block':
        IssueType.CODE_STYLE,
    'Labeled switch rule has redundant code block':
        IssueType.CODE_STYLE,
    'Lambda body can be code block':
        IssueType.CODE_STYLE,
    'Lambda can be replaced with anonymous class':
        IssueType.CODE_STYLE,
    'Lambda parameter type can be specified':
        IssueType.CODE_STYLE,
    'Local variable or parameter can be final':
        IssueType.CODE_STYLE,
    'Method reference can be replaced with lambda':
        IssueType.CODE_STYLE,
    'Missorted modifiers':
        IssueType.CODE_STYLE,
    'Multi-catch can be split into separate catch blocks':
        IssueType.CODE_STYLE,
    'Multiple variables in one declaration':
        IssueType.CODE_STYLE,
    'Nested method call':
        IssueType.CODE_STYLE,
    'Null value for Optional type':
        IssueType.CODE_STYLE,
    'Objects.equals() can be replaced with equals()':
        IssueType.CODE_STYLE,
    '\'Optional\' contains array or collection':
        IssueType.CODE_STYLE,
    'Optional.isPresent() can be replaced with functional-style expression':
        IssueType.CODE_STYLE,
    'Raw type can be generic':
        IssueType.CODE_STYLE,
    'Redundant \'new\' expression in constant array creation':
        IssueType.CODE_STYLE,
    'Redundant field initialization':
        IssueType.CODE_STYLE,
    'Redundant interface declaration':
        IssueType.CODE_STYLE,
    'Redundant no-arg constructor':
        IssueType.CODE_STYLE,
    '\'return\' separated from the result computation':
        IssueType.CODE_STYLE,
    'Return of \'this\'':
        IssueType.CODE_STYLE,
    'Simplifiable annotation':
        IssueType.CODE_STYLE,
    'Single-element annotation':
        IssueType.CODE_STYLE,
    '\'size() == 0\' replaceable with \'isEmpty()\'':
        IssueType.CODE_STYLE,
    'Standard Charset object can be used':
        IssueType.CODE_STYLE,
    'Stream API call chain can be replaced with loop':
        IssueType.CODE_STYLE,
    'Subsequent steps can be fused into Stream API chain':
        IssueType.CODE_STYLE,
    '\'try\' statement with multiple resources can be split':
        IssueType.CODE_STYLE,
    'Type parameter explicitly extends \'java.lang.Object\'':
        IssueType.CODE_STYLE,
    'Unclear expression':
        IssueType.CODE_STYLE,
    'Unnecessarily qualified inner class access':
        IssueType.CODE_STYLE,
    'Unnecessarily qualified static access':
        IssueType.CODE_STYLE,
    'Unnecessarily qualified statically imported element':
        IssueType.CODE_STYLE,
    'Unnecessary \'final\' on local variable or parameter':
        IssueType.CODE_STYLE,
    'Unnecessary \'null\' check before \'equals()\' call':
        IssueType.CODE_STYLE,
    'Unnecessary \'super\' qualifier':
        IssueType.CODE_STYLE,
    'Unnecessary \'this\' qualifier':
        IssueType.CODE_STYLE,
    'Unnecessary call to \'super()\'':
        IssueType.CODE_STYLE,
    'Unnecessary call to \'toString()\'':
        IssueType.CODE_STYLE,
    'Unnecessary code block':
        IssueType.CODE_STYLE,
    'Unnecessary conversion to String':
        IssueType.CODE_STYLE,
    'Unnecessary enum modifier':
        IssueType.CODE_STYLE,
    'Unnecessary fully qualified name':
        IssueType.CODE_STYLE,
    'Unnecessary interface modifier':
        IssueType.CODE_STYLE,
    'Unnecessary parentheses':
        IssueType.CODE_STYLE,
    'Unnecessary qualifier for \'this\' or \'super\'':
        IssueType.CODE_STYLE,
    'Unnecessary semicolon':
        IssueType.CODE_STYLE,
    'Unqualified inner class access':
        IssueType.CODE_STYLE,
    'Unqualified static access':
        IssueType.CODE_STYLE,

    # Java | Control flow issues
    'Assertion can be replaced with if statement':
        IssueType.ERROR_PRONE,
    'Boolean expression could be replaced with conditional expression':
        IssueType.BEST_PRACTICES,
    '\'break\' statement':
        IssueType.BEST_PRACTICES,
    '\'break\' statement with label':
        IssueType.BEST_PRACTICES,
    'Conditional break inside infinite loop':
        IssueType.BEST_PRACTICES,
    'Conditional can be pushed inside branch expression':
        IssueType.BEST_PRACTICES,
    'Conditional expression (?:)':
        IssueType.BEST_PRACTICES,
    'Conditional expression with identical branches':
        IssueType.BEST_PRACTICES,
    'Conditional expression with negated condition':
        IssueType.BEST_PRACTICES,
    'Constant conditional expression':
        IssueType.BEST_PRACTICES,
    '\'continue\' statement':
        IssueType.BEST_PRACTICES,
    '\'continue\' statement with label':
        IssueType.BEST_PRACTICES,
    '\'default\' not last case in \'switch\' statement':
        IssueType.BEST_PRACTICES,
    'Double negation':
        IssueType.BEST_PRACTICES,
    'Duplicate condition in \'if\' statement':
        IssueType.BEST_PRACTICES,
    'Duplicate condition on \'&&\' or \'||\'':
        IssueType.BEST_PRACTICES,
    'Enum \'switch\' statement that misses case':
        IssueType.BEST_PRACTICES,
    'Fallthrough in \'switch\' statement':
        IssueType.BEST_PRACTICES,
    '\'for\' loop may be replaced with \'while\' loop':
        IssueType.BEST_PRACTICES,
    '\'for\' loop with missing components':
        IssueType.BEST_PRACTICES,
    'Idempotent loop body':
        IssueType.BEST_PRACTICES,
    '\'if\' statement could be replaced with conditional expression':
        IssueType.BEST_PRACTICES,
    '\'if\' statement with common parts':
        IssueType.BEST_PRACTICES,
    '\'if\' statement with negated condition':
        IssueType.BEST_PRACTICES,
    '\'if\' statement with too many branches':
        IssueType.BEST_PRACTICES,
    'Infinite loop statement':
        IssueType.BEST_PRACTICES,
    'Labeled statement':
        IssueType.BEST_PRACTICES,
    'Local variable used and declared in different \'switch\' branches':
        IssueType.BEST_PRACTICES,
    'Loop statement that does not loop':
        IssueType.BEST_PRACTICES,
    'Loop variable not updated inside loop':
        IssueType.ERROR_PRONE,
    'Loop with implicit termination condition':
        IssueType.BEST_PRACTICES,
    'Negated conditional expression':
        IssueType.BEST_PRACTICES,
    'Negated equality expression':
        IssueType.BEST_PRACTICES,
    'Nested \'switch\'':
        IssueType.BEST_PRACTICES,
    'Nested conditional expression':
        IssueType.BEST_PRACTICES,
    'Overly complex boolean expression':
        IssueType.BEST_PRACTICES,
    'Pointless \'indexOf()\' comparison':
        IssueType.BEST_PRACTICES,
    'Pointless boolean expression':
        IssueType.BEST_PRACTICES,
    'Redundant \'else\'':
        IssueType.BEST_PRACTICES,
    'Redundant \'if\' statement':
        IssueType.BEST_PRACTICES,
    'Redundant conditional expression':
        IssueType.BEST_PRACTICES,
    'Simplifiable boolean expression':
        IssueType.BEST_PRACTICES,
    'Simplifiable conditional expression':
        IssueType.BEST_PRACTICES,
    'Statement can be replaced with \'assert\' or \'Objects.requireNonNull\'':
        IssueType.BEST_PRACTICES,
    '\'switch\' statement':
        IssueType.BEST_PRACTICES,
    '\'switch\' statement with too few branches':
        IssueType.BEST_PRACTICES,
    '\'switch\' statement with too low of a branch density':
        IssueType.BEST_PRACTICES,
    '\'switch\' statement with too many branches':
        IssueType.BEST_PRACTICES,
    '\'switch\' statement without \'default\' branch':
        IssueType.BEST_PRACTICES,
    'Unnecessary \'null\' check before method call':
        IssueType.BEST_PRACTICES,

    # Java | Data flow
    'Boolean method is always inverted':
        IssueType.BEST_PRACTICES,
    'Boolean variable is always inverted':
        IssueType.BEST_PRACTICES,
    'Method call violates Law of Demeter':
        IssueType.BEST_PRACTICES,
    'Negatively named boolean variable':
        IssueType.BEST_PRACTICES,
    'Redundant local variable':
        IssueType.BEST_PRACTICES,
    'Reuse of local variable':
        IssueType.BEST_PRACTICES,
    'Scope of variable is too broad':
        IssueType.BEST_PRACTICES,
    'Use of variable whose value is known to be constant':
        IssueType.BEST_PRACTICES,

    # Java | Declaration redundancy
    'Access static member via instance reference':
        IssueType.BEST_PRACTICES,
    'Actual method parameter is the same constant':
        IssueType.BEST_PRACTICES,
    'Collector can be simplified':
        IssueType.BEST_PRACTICES,
    'Declaration access can be weaker':
        IssueType.BEST_PRACTICES,
    'Declaration can have final modifier':
        IssueType.BEST_PRACTICES,
    'Default annotation parameter value':
        IssueType.BEST_PRACTICES,
    'Duplicate throws':
        IssueType.BEST_PRACTICES,
    'Empty method':
        IssueType.BEST_PRACTICES,
    'Functional expression can be folded':
        IssueType.BEST_PRACTICES,
    'Method can be void':
        IssueType.BEST_PRACTICES,
    'Method returns the same value':
        IssueType.BEST_PRACTICES,
    'Null-check method is called with obviously non-null argument':
        IssueType.BEST_PRACTICES,
    'Optional call chain can be simplified':
        IssueType.BEST_PRACTICES,
    'Redundant \'close()\'':
        IssueType.BEST_PRACTICES,
    'Redundant \'requires\' statement in module-info':
        IssueType.BEST_PRACTICES,
    'Redundant \'throws\' clause':
        IssueType.BEST_PRACTICES,
    'Redundant lambda parameter types':
        IssueType.BEST_PRACTICES,
    'Redundant operation on empty container':
        IssueType.BEST_PRACTICES,
    'Redundant step in Stream or Optional call chain':
        IssueType.BEST_PRACTICES,
    'Stream API call chain can be simplified':
        IssueType.BEST_PRACTICES,
    'Trivial usage of functional expression':
        IssueType.BEST_PRACTICES,
    'Unnecessary module dependency':
        IssueType.BEST_PRACTICES,
    'Unused declaration':
        IssueType.BEST_PRACTICES,
    'Unused label':
        IssueType.BEST_PRACTICES,
    'Unused library':
        IssueType.BEST_PRACTICES,
    'Variable is assigned to itself':
        IssueType.BEST_PRACTICES,
    'Wrapper type may be primitive':
        IssueType.BEST_PRACTICES,

    # Java | Dependency issues
    'Class with too many dependencies':
        IssueType.BEST_PRACTICES,
    'Class with too many dependents':
        IssueType.BEST_PRACTICES,
    'Class with too many transitive dependencies':
        IssueType.BEST_PRACTICES,
    'Class with too many transitive dependents':
        IssueType.BEST_PRACTICES,
    'Cyclic class dependency':
        IssueType.BEST_PRACTICES,
    'Cyclic package dependency':
        IssueType.BEST_PRACTICES,
    'Illegal package dependencies':
        IssueType.ERROR_PRONE,

    # Java | Encapsulation
    'Accessing a non-public field of another object':
        IssueType.BEST_PRACTICES,
    'Assignment or return of field with mutable type':
        IssueType.BEST_PRACTICES,
    'Package-visible field':
        IssueType.BEST_PRACTICES,
    'Package-visible nested class':
        IssueType.BEST_PRACTICES,
    'Protected field':
        IssueType.BEST_PRACTICES,
    'Protected nested class':
        IssueType.BEST_PRACTICES,
    '\'public\' field':
        IssueType.BEST_PRACTICES,
    '\'public\' nested class':
        IssueType.BEST_PRACTICES,

    # Java | Error handling
    'Catch block may ignore exception':
        IssueType.ERROR_PRONE,
    'Caught exception is immediately rethrown':
        IssueType.BEST_PRACTICES,
    'Checked exception class':
        IssueType.BEST_PRACTICES,
    'Class directly extends \'java.lang.Throwable\'':
        IssueType.BEST_PRACTICES,
    '\'continue\' or \'break\' inside \'finally\' block':
        IssueType.ERROR_PRONE,
    'Empty \'finally\' block':
        IssueType.BEST_PRACTICES,
    'Empty \'try\' block':
        IssueType.BEST_PRACTICES,
    'Exception constructor called without arguments':
        IssueType.BEST_PRACTICES,
    '\'finally\' block which can not complete normally':
        IssueType.ERROR_PRONE,
    '\'instanceof\' on \'catch\' parameter':
        IssueType.BEST_PRACTICES,
    '\'java.lang.Error\' not rethrown':
        IssueType.ERROR_PRONE,
    '\'java.lang.ThreadDeath\' not rethrown':
        IssueType.ERROR_PRONE,
    'Nested \'try\' statement':
        IssueType.BEST_PRACTICES,
    'Non-final field of exception class':
        IssueType.BEST_PRACTICES,
    '\'null\' thrown':
        IssueType.ERROR_PRONE,
    'Overly broad \'catch\' block':
        IssueType.BEST_PRACTICES,
    'Overly broad \'throws\' clause':
        IssueType.BEST_PRACTICES,
    'Prohibited exception caught':
        IssueType.ERROR_PRONE,
    'Prohibited exception declared':
        IssueType.ERROR_PRONE,
    'Prohibited exception thrown':
        IssueType.ERROR_PRONE,
    '\'return\' inside \'finally\' block':
        IssueType.BEST_PRACTICES,
    '\'throw\' caught by containing \'try\' statement':
        IssueType.ERROR_PRONE,
    '\'throw\' inside \'catch\' block which ignores the caught exception':
        IssueType.ERROR_PRONE,
    '\'throw\' inside \'finally\' block':
        IssueType.ERROR_PRONE,
    'Unchecked exception class':
        IssueType.BEST_PRACTICES,
    'Unchecked exception declared in \'throws\' clause':
        IssueType.BEST_PRACTICES,
    'Unnecessary call to \'Throwable.initCause()\'':
        IssueType.BEST_PRACTICES,

    # Java | Finalization
    '\'finalize()\' called explicitly':
        IssueType.BEST_PRACTICES,
    '\'finalize()\' declaration':
        IssueType.BEST_PRACTICES,
    '\'finalize()\' not declared \'protected\'':
        IssueType.BEST_PRACTICES,

    # Java | General
    'Test-only class or method call in production code':
        IssueType.BEST_PRACTICES,

    # Java | Imports
    '\'*\' import':
        IssueType.BEST_PRACTICES,
    'Import from same package':
        IssueType.BEST_PRACTICES,
    '\'java.lang\' import':
        IssueType.BEST_PRACTICES,
    'Single class import':
        IssueType.BEST_PRACTICES,
    'Static import':
        IssueType.BEST_PRACTICES,
    'Unused import':
        IssueType.BEST_PRACTICES,

    # Java | Inheritance issues
    'Abstract class extends concrete class':
        IssueType.BEST_PRACTICES,
    'Abstract class which has no concrete subclass':
        IssueType.BEST_PRACTICES,
    'Abstract class without abstract methods':
        IssueType.BEST_PRACTICES,
    'Abstract method overrides abstract method':
        IssueType.BEST_PRACTICES,
    'Abstract method overrides concrete method':
        IssueType.BEST_PRACTICES,
    'Abstract method with missing implementations':
        IssueType.BEST_PRACTICES,
    'Class explicitly extends a Collection class':
        IssueType.BEST_PRACTICES,
    'Class extends annotation interface':
        IssueType.BEST_PRACTICES,
    'Class extends utility class':
        IssueType.BEST_PRACTICES,
    'Class may extend a commonly used base class':
        IssueType.BEST_PRACTICES,
    'Final declaration can\'t be overridden at runtime':
        IssueType.ERROR_PRONE,
    'Interface which has no concrete subclass':
        IssueType.BEST_PRACTICES,
    'Method does not call super method':
        IssueType.BEST_PRACTICES,
    'Method is identical to its super method':
        IssueType.BEST_PRACTICES,
    'Missing @Override annotation':
        IssueType.BEST_PRACTICES,
    'Non-varargs method overrides varargs method':
        IssueType.BEST_PRACTICES,
    'Parameter type prevents overriding':
        IssueType.BEST_PRACTICES,
    '\'public\' constructor in \'abstract\' class':
        IssueType.BEST_PRACTICES,
    'Static inheritance':
        IssueType.BEST_PRACTICES,
    'Type parameter extends final class':
        IssueType.BEST_PRACTICES,

    # Java | Initialization
    'Abstract method called during object construction':
        IssueType.ERROR_PRONE,
    'Double brace initialization':
        IssueType.ERROR_PRONE,
    'Instance field may not be initialized':
        IssueType.ERROR_PRONE,
    'Instance field used before initialization':
        IssueType.ERROR_PRONE,
    'Non-final static field is used during class initialization':
        IssueType.ERROR_PRONE,
    'Overridable method called during object construction':
        IssueType.ERROR_PRONE,
    'Overridden method called during object construction':
        IssueType.ERROR_PRONE,
    'Static field may not be initialized':
        IssueType.ERROR_PRONE,
    'Static field used before initialization':
        IssueType.ERROR_PRONE,
    '\'this\' reference escaped in object construction':
        IssueType.ERROR_PRONE,
    'Unsafe lazy initialization of \'static\' field':
        IssueType.ERROR_PRONE,

    # Java | JUnit
    '\'assertEquals()\' between objects of inconvertible types':
        IssueType.ERROR_PRONE,
    '\'assertEquals()\' called on array':
        IssueType.ERROR_PRONE,
    '\'assertEquals()\' may be \'assertSame()\'':
        IssueType.BEST_PRACTICES,
    'Assertion expression can be replaced with \'assertThat\' method call':
        IssueType.BEST_PRACTICES,
    'Constant JUnit assert argument':
        IssueType.ERROR_PRONE,
    'Expected exception never thrown in test method body':
        IssueType.ERROR_PRONE,
    'Highlight problem line in test':
        IssueType.BEST_PRACTICES,
    'JUnit test annotated with \'@Ignore\'/\'@Disabled\'':
        IssueType.BEST_PRACTICES,
    'JUnit test method in product source':
        IssueType.BEST_PRACTICES,
    'JUnit test method without any assertions':
        IssueType.ERROR_PRONE,
    'JUnit TestCase in product source':
        IssueType.BEST_PRACTICES,
    'JUnit TestCase with non-trivial constructors':
        IssueType.BEST_PRACTICES,
    'JUnit 4 test can be JUnit 5':
        IssueType.BEST_PRACTICES,
    'JUnit 4 test method in class extending JUnit 3 TestCase':
        IssueType.BEST_PRACTICES,
    'JUnit 5 malformed @Nested class':
        IssueType.BEST_PRACTICES,
    'JUnit 5 malformed parameterized test':
        IssueType.BEST_PRACTICES,
    'JUnit 5 malformed repeated test':
        IssueType.BEST_PRACTICES,
    'Malformed \'setUp()\' or \'tearDown()\' method':
        IssueType.BEST_PRACTICES,
    'Malformed @Before or @After method':
        IssueType.BEST_PRACTICES,
    'Malformed @BeforeClass/@BeforeAll or @AfterClass/@AfterAll method':
        IssueType.BEST_PRACTICES,
    'Malformed @DataPoint field':
        IssueType.BEST_PRACTICES,
    'Malformed @Rule/@ClassRule field':
        IssueType.BEST_PRACTICES,
    'Malformed test method':
        IssueType.BEST_PRACTICES,
    'Message missing on JUnit assertion':
        IssueType.BEST_PRACTICES,
    'Misordered \'assertEquals()\' arguments':
        IssueType.BEST_PRACTICES,
    'Multiple exceptions declared on test method':
        IssueType.BEST_PRACTICES,
    'Obsolete assertions in JUnit 5 tests':
        IssueType.BEST_PRACTICES,
    'Old style JUnit test method in JUnit 4 class':
        IssueType.BEST_PRACTICES,
    '@RunWith(JUnitPlatform.class) without test methods':
        IssueType.BEST_PRACTICES,
    '@RunWith(Parameterized.class) without data provider':
        IssueType.BEST_PRACTICES,
    'Simplifiable JUnit assertion':
        IssueType.BEST_PRACTICES,
    '\'suite()\' method not declared \'static\'':
        IssueType.ERROR_PRONE,
    '\'super.tearDown()\' not called from \'finally\' block':
        IssueType.ERROR_PRONE,
    'Test class with no tests':
        IssueType.ERROR_PRONE,
    'Unconstructable JUnit TestCase':
        IssueType.ERROR_PRONE,
    'Usage of obsolete \'junit.framework.Assert\' method':
        IssueType.BEST_PRACTICES,

    # Java | Logging
    'Class with multiple loggers':
        IssueType.ERROR_PRONE,
    'Class without logger':
        IssueType.BEST_PRACTICES,
    'Log condition does not match logging call':
        IssueType.BEST_PRACTICES,
    'Logger initialized with foreign class':
        IssueType.BEST_PRACTICES,
    'Logging call not guarded by log condition':
        IssueType.BEST_PRACTICES,
    'Non-constant logger':
        IssueType.BEST_PRACTICES,
    'Non-constant string concatenation as argument to logging call':
        IssueType.BEST_PRACTICES,
    'Number of placeholders does not match number of arguments in logging call':
        IssueType.BEST_PRACTICES,
    '\'public\' method without logging':
        IssueType.BEST_PRACTICES,

    # Java | Memory
    'Anonymous class may be a named \'static\' inner class':
        IssueType.BEST_PRACTICES,
    'Calls to \'System.gc()\' or \'Runtime.gc()\'':
        IssueType.BEST_PRACTICES,
    'Inner class may be \'static\'':
        IssueType.BEST_PRACTICES,
    'Return of instance of anonymous, local or inner class':
        IssueType.BEST_PRACTICES,
    'Static collection':
        IssueType.BEST_PRACTICES,
    'StringBuilder field':
        IssueType.BEST_PRACTICES,
    'Unnecessary zero length array usage':
        IssueType.BEST_PRACTICES,
    'Zero-length array allocation':
        IssueType.BEST_PRACTICES,

    # Java | Method metrics
    'Constructor with too many parameters':
        IssueType.BEST_PRACTICES,
    'Method with more than three negations':
        IssueType.BEST_PRACTICES,
    'Method with multiple loops':
        IssueType.BEST_PRACTICES,
    'Method with multiple return points':
        IssueType.BEST_PRACTICES,
    'Method with too many exceptions declared':
        IssueType.BEST_PRACTICES,
    'Method with too many parameters':
        IssueType.BEST_PRACTICES,
    'Overly complex method':
        IssueType.BEST_PRACTICES,
    'Overly coupled method':
        IssueType.BEST_PRACTICES,
    'Overly long lambda expression':
        IssueType.BEST_PRACTICES,
    'Overly long method':
        IssueType.BEST_PRACTICES,
    'Overly nested method':
        IssueType.BEST_PRACTICES,
    'Class independent of its module':
        IssueType.BEST_PRACTICES,
    'Class only used from one other module':
        IssueType.BEST_PRACTICES,
    'Inconsistent language level settings':
        IssueType.BEST_PRACTICES,
    'Module with too few classes':
        IssueType.BEST_PRACTICES,
    'Module with too many classes':
        IssueType.BEST_PRACTICES,

    # Java | Naming conventions
    'Boolean method name must start with question word':
        IssueType.CODE_STYLE,
    'Class name prefixed with package name':
        IssueType.CODE_STYLE,
    'Class name same as ancestor name':
        IssueType.CODE_STYLE,
    'Class naming convention':
        IssueType.CODE_STYLE,
    'Confusing \'main()\' method':
        IssueType.CODE_STYLE,
    'Exception class name does not end with \'Exception\'':
        IssueType.CODE_STYLE,
    'Field naming convention':
        IssueType.CODE_STYLE,
    'Java module naming conventions':
        IssueType.CODE_STYLE,
    'Lambda-unfriendly method overload':
        IssueType.CODE_STYLE,
    'Lambda parameter naming convention':
        IssueType.CODE_STYLE,
    'Local variable naming convention':
        IssueType.CODE_STYLE,
    'Method name same as class name':
        IssueType.CODE_STYLE,
    'Method name same as parent class name':
        IssueType.CODE_STYLE,
    'Method names differing only by case':
        IssueType.CODE_STYLE,
    'Method naming convention':
        IssueType.CODE_STYLE,
    'Method parameter naming convention':
        IssueType.CODE_STYLE,
    'Non-boolean method name must not start with question word':
        IssueType.CODE_STYLE,
    'Non-constant field with upper-case name':
        IssueType.CODE_STYLE,
    'Non-exception class name ends with \'Exception\'':
        IssueType.CODE_STYLE,
    'Overloaded methods with same number of parameters':
        IssueType.CODE_STYLE,
    'Overloaded varargs method':
        IssueType.CODE_STYLE,
    'Package naming convention':
        IssueType.CODE_STYLE,
    'Parameter name differs from parameter in overridden method':
        IssueType.CODE_STYLE,
    'Questionable name':
        IssueType.CODE_STYLE,
    'Standard variable names':
        IssueType.CODE_STYLE,
    'Use of \'$\' in identifier':
        IssueType.CODE_STYLE,

    # Java | Numeric issues
    'Call to \'BigDecimal\' method without a rounding mode argument':
        IssueType.ERROR_PRONE,
    '\'char\' expression used in arithmetic context':
        IssueType.ERROR_PRONE,
    'Comparison of \'short\' and \'char\' values':
        IssueType.ERROR_PRONE,
    'Comparison to Double.NaN or Float.NaN':
        IssueType.ERROR_PRONE,
    'Confusing floating-point literal':
        IssueType.ERROR_PRONE,
    'Constant call to \'java.lang.Math\'':
        IssueType.ERROR_PRONE,
    'Divide by zero':
        IssueType.ERROR_PRONE,
    '\'double\' literal cast to \'float\' could be \'float\' literal':
        IssueType.ERROR_PRONE,
    '\'equals()\' called on \'java.math.BigDecimal\'':
        IssueType.ERROR_PRONE,
    'Floating point equality comparison':
        IssueType.ERROR_PRONE,
    'Implicit numeric conversion':
        IssueType.ERROR_PRONE,
    '\'int\' literal cast to \'long\' could be \'long\' literal':
        IssueType.ERROR_PRONE,
    'Integer division in floating point context':
        IssueType.ERROR_PRONE,
    'Integer multiplication or shift implicitly cast to long':
        IssueType.ERROR_PRONE,
    '\'long\' literal ending with \'l\' instead of \'L\'':
        IssueType.ERROR_PRONE,
    'Non-reproducible call to \'java.lang.Math\'':
        IssueType.BEST_PRACTICES,
    'Number constructor call with primitive argument':
        IssueType.ERROR_PRONE,
    'Numeric cast that loses precision':
        IssueType.ERROR_PRONE,
    'Numeric overflow':
        IssueType.ERROR_PRONE,
    'Octal and decimal integers in same array':
        IssueType.ERROR_PRONE,
    'Octal integer':
        IssueType.ERROR_PRONE,
    'Overly complex arithmetic expression':
        IssueType.ERROR_PRONE,
    'Pointless arithmetic expression':
        IssueType.BEST_PRACTICES,
    'Suspicious test for oddness':
        IssueType.ERROR_PRONE,
    'Suspicious underscore in number literal':
        IssueType.ERROR_PRONE,
    'Unary plus':
        IssueType.ERROR_PRONE,
    'Unnecessary explicit numeric cast':
        IssueType.ERROR_PRONE,
    'Unnecessary unary minus':
        IssueType.ERROR_PRONE,
    'Unpredictable BigDecimal constructor call':
        IssueType.ERROR_PRONE,

    # Java | Packaging issues
    'Class independent of its package':
        IssueType.BEST_PRACTICES,
    'Class only used from one other package':
        IssueType.BEST_PRACTICES,
    'Empty directory':
        IssueType.BEST_PRACTICES,
    'Exception package':
        IssueType.BEST_PRACTICES,
    'Package with classes in multiple modules':
        IssueType.BEST_PRACTICES,
    'Package with disjoint dependency graph':
        IssueType.BEST_PRACTICES,
    'Package with too few classes':
        IssueType.BEST_PRACTICES,
    'Package with too many classes':
        IssueType.BEST_PRACTICES,

    # Java | Performance
    'Boolean constructor call':
        IssueType.BEST_PRACTICES,
    'Boxing of already boxed value':
        IssueType.BEST_PRACTICES,
    'Bulk operation can be used instead of iteration':
        IssueType.BEST_PRACTICES,
    'Call to \'Arrays.asList()\' with too few arguments':
        IssueType.BEST_PRACTICES,
    'Call to simple getter from within class':
        IssueType.BEST_PRACTICES,
    'Call to simple setter from within class':
        IssueType.BEST_PRACTICES,
    'Class initializer may be \'static\'':
        IssueType.BEST_PRACTICES,
    '\'Collection.toArray()\' call style':
        IssueType.BEST_PRACTICES,
    'Collection without initial capacity':
        IssueType.BEST_PRACTICES,
    'Concatenation with empty string':
        IssueType.BEST_PRACTICES,
    'Dynamic regular expression could be replaced by compiled Pattern':
        IssueType.BEST_PRACTICES,
    '\'equals()\' call can be replaced with \'==\'':
        IssueType.BEST_PRACTICES,
    '\'equals()\' or \'hashCode()\' called on \'java.net.URL\' object':
        IssueType.BEST_PRACTICES,
    'Explicit argument can be lambda':
        IssueType.BEST_PRACTICES,
    'Field may be \'static\'':
        IssueType.BEST_PRACTICES,
    'Inefficient Stream API call chains ending with count()':
        IssueType.BEST_PRACTICES,
    'Instantiating object to get Class object':
        IssueType.BEST_PRACTICES,
    'Iteration over \'keySet()\' may be optimized':
        IssueType.BEST_PRACTICES,
    '\'List.remove()\' called in loop':
        IssueType.BEST_PRACTICES,
    'Loop can be terminated after condition is met':
        IssueType.BEST_PRACTICES,
    'Manual array copy':
        IssueType.BEST_PRACTICES,
    'Manual array to collection copy':
        IssueType.BEST_PRACTICES,
    'Map or Set may contain \'java.net.URL\' objects':
        IssueType.BEST_PRACTICES,
    'Map replaceable with EnumMap':
        IssueType.BEST_PRACTICES,
    'Method may be \'static\'':
        IssueType.BEST_PRACTICES,
    'Non-constant String should be StringBuilder':
        IssueType.BEST_PRACTICES,
    'Object allocation in loop':
        IssueType.BEST_PRACTICES,
    'Object instantiation inside \'equals()\' or \'hashCode()\'':
        IssueType.BEST_PRACTICES,
    'Redundant \'Collection.addAll()\' call':
        IssueType.BEST_PRACTICES,
    'Redundant call to \'String.format()\'':
        IssueType.BEST_PRACTICES,
    'Set replaceable with EnumSet':
        IssueType.BEST_PRACTICES,
    'Single character string argument in \'String.indexOf()\' call':
        IssueType.BEST_PRACTICES,
    'Single character string concatenation':
        IssueType.BEST_PRACTICES,
    '\'String.equals('')\'':
        IssueType.BEST_PRACTICES,
    'String concatenation as argument to \'StringBuilder.append()\' call':
        IssueType.BEST_PRACTICES,
    'String concatenation in loop':
        IssueType.BEST_PRACTICES,
    '\'StringBuilder.toString()\' in concatenation':
        IssueType.BEST_PRACTICES,
    'StringBuilder without initial capacity':
        IssueType.BEST_PRACTICES,
    'Tail recursion':
        IssueType.BEST_PRACTICES,
    'Unnecessary temporary object in conversion from String':
        IssueType.BEST_PRACTICES,
    'Unnecessary temporary object in conversion to String':
        IssueType.BEST_PRACTICES,
    'Using \'Random.nextDouble()\' to get random integer':
        IssueType.BEST_PRACTICES,

    # Java | Portability
    'Call to \'Runtime.exec()\'':
        IssueType.ERROR_PRONE,
    'Call to \'System.exit()\' or related methods':
        IssueType.ERROR_PRONE,
    'Call to \'System.getenv()\'':
        IssueType.ERROR_PRONE,
    'Hardcoded file separator':
        IssueType.ERROR_PRONE,
    'Hardcoded line separator':
        IssueType.ERROR_PRONE,
    'Native method':
        IssueType.ERROR_PRONE,
    'Use of \'java.lang.ProcessBuilder\' class':
        IssueType.ERROR_PRONE,
    'Use of AWT peer class':
        IssueType.ERROR_PRONE,
    'Use of concrete JDBC driver class':
        IssueType.ERROR_PRONE,
    'Use of sun.* classes':
        IssueType.ERROR_PRONE,

    # Java | Probable bugs
    'Array comparison using \'==\', instead of \'Arrays.equals()\'':
        IssueType.ERROR_PRONE,
    '\'assert\' statement condition is constant':
        IssueType.ERROR_PRONE,
    '\'assert\' statement with side effects':
        IssueType.ERROR_PRONE,
    'Call to \'toString()\' on array':
        IssueType.ERROR_PRONE,
    'Call to default \'toString()\'':
        IssueType.ERROR_PRONE,
    'Call to String.replaceAll(\'.\', ...)':
        IssueType.ERROR_PRONE,
    'Cast conflicts with \'instanceof\'':
        IssueType.ERROR_PRONE,
    'Casting to incompatible interface':
        IssueType.ERROR_PRONE,
    'Class.getClass() call':
        IssueType.ERROR_PRONE,
    'Cleaner captures object reference':
        IssueType.ERROR_PRONE,
    'Collection added to self':
        IssueType.ERROR_PRONE,
    'Comparable implemented but \'equals()\' not overridden':
        IssueType.ERROR_PRONE,
    'Confusing argument to varargs method':
        IssueType.ERROR_PRONE,
    'Confusing primitive array argument to varargs method':
        IssueType.ERROR_PRONE,
    'Constant conditions & exceptions':
        IssueType.ERROR_PRONE,
    'Contract issues':
        IssueType.ERROR_PRONE,
    'Copy constructor misses field':
        IssueType.ERROR_PRONE,
    'Covariant \'equals()\'':
        IssueType.ERROR_PRONE,
    'Duplicated delimiters in java.util.StringTokenizer':
        IssueType.ERROR_PRONE,
    'Empty class initializer':
        IssueType.ERROR_PRONE,
    '\'equal()\' instead of \'equals()\'':
        IssueType.ERROR_PRONE,
    '\'equals()\' and \'hashCode()\' not paired':
        IssueType.ERROR_PRONE,
    '\'equals()\' between objects of inconvertible types':
        IssueType.ERROR_PRONE,
    '\'equals()\' called on array':
        IssueType.ERROR_PRONE,
    '\'equals()\' called on itself':
        IssueType.ERROR_PRONE,
    '\'equals()\' called on StringBuilder':
        IssueType.ERROR_PRONE,
    '\'equals()\' method which does not check class of parameter':
        IssueType.ERROR_PRONE,
    '\'hashCode()\' called on array':
        IssueType.ERROR_PRONE,
    'Infinite recursion':
        IssueType.ERROR_PRONE,
    'Inner class referenced via subclass':
        IssueType.ERROR_PRONE,
    '\'instanceof\' with incompatible interface':
        IssueType.ERROR_PRONE,
    'Instantiation of utility class':
        IssueType.ERROR_PRONE,
    'Invalid method reference used for Comparator':
        IssueType.ERROR_PRONE,
    'Iterable is used as vararg':
        IssueType.ERROR_PRONE,
    '\'Iterator.hasNext()\' which calls \'next()\'':
        IssueType.ERROR_PRONE,
    '\'Iterator.next()\' which can\'t throw \'NoSuchElementException\'':
        IssueType.ERROR_PRONE,
    'Loop executes zero or billions times':
        IssueType.ERROR_PRONE,
    'Magic Constant':
        IssueType.ERROR_PRONE,
    'Malformed format string':
        IssueType.ERROR_PRONE,
    'Malformed regular expression':
        IssueType.ERROR_PRONE,
    'Malformed XPath expression':
        IssueType.ERROR_PRONE,
    '\'Math.random()\' cast to \'int\'':
        IssueType.ERROR_PRONE,
    'Mismatched query and update of collection':
        IssueType.ERROR_PRONE,
    'Mismatched query and update of StringBuilder':
        IssueType.ERROR_PRONE,
    'Mismatched read and write of array':
        IssueType.ERROR_PRONE,
    'New object is compared using \'==\'':
        IssueType.ERROR_PRONE,
    'Non-final field referenced in \'compareTo()\'':
        IssueType.ERROR_PRONE,
    'Non-final field referenced in \'equals()\'':
        IssueType.ERROR_PRONE,
    'Non-final field referenced in \'hashCode()\'':
        IssueType.ERROR_PRONE,
    'Non-short-circuit boolean expression':
        IssueType.ERROR_PRONE,
    'Non-short-circuit operation consumes the infinite stream':
        IssueType.ERROR_PRONE,
    '@NotNull/@Nullable problems':
        IssueType.ERROR_PRONE,
    'Number comparison using \'==\', instead of \'equals()\'':
        IssueType.ERROR_PRONE,
    'Object comparison using \'==\', instead of \'equals()\'':
        IssueType.ERROR_PRONE,
    '\'Objects.equals()\' called on arrays':
        IssueType.ERROR_PRONE,
    'Optional.get() is called without isPresent() check':
        IssueType.ERROR_PRONE,
    'Overwritten Map key or Set element':
        IssueType.ERROR_PRONE,
    'Reference checked for \'null\' is not used inside \'if\'':
        IssueType.ERROR_PRONE,
    'Reflective access to a source-only annotation':
        IssueType.ERROR_PRONE,
    'Result of method call ignored':
        IssueType.ERROR_PRONE,
    'Result of object allocation ignored':
        IssueType.ERROR_PRONE,
    'Return of \'null\'':
        IssueType.ERROR_PRONE,
    'Sorted collection with non-comparable elements':
        IssueType.ERROR_PRONE,
    'Statement with empty body':
        IssueType.ERROR_PRONE,
    'Static field referenced via subclass':
        IssueType.ERROR_PRONE,
    'Static method referenced via subclass':
        IssueType.ERROR_PRONE,
    '\'String.equals()\' called with \'CharSequence\' argument':
        IssueType.ERROR_PRONE,
    'String comparison using \'==\', instead of \'equals()\'':
        IssueType.ERROR_PRONE,
    'String concatenation as argument to \'format()\' call':
        IssueType.ERROR_PRONE,
    'String concatenation as argument to \'MessageFormat.format()\' call':
        IssueType.ERROR_PRONE,
    'String literal concatenation missing whitespace':
        IssueType.ERROR_PRONE,
    'StringBuilder constructor call with \'char\' argument':
        IssueType.ERROR_PRONE,
    'Subtraction in \'compareTo()\'':
        IssueType.ERROR_PRONE,
    'Suspicious \'Collection.toArray()\' call':
        IssueType.ERROR_PRONE,
    'Suspicious \'Comparator.compare()\' implementation':
        IssueType.ERROR_PRONE,
    'Suspicious \'List.remove()\' in the loop':
        IssueType.ERROR_PRONE,
    'Suspicious \'System.arraycopy()\' call':
        IssueType.ERROR_PRONE,
    'Suspicious array cast':
        IssueType.ERROR_PRONE,
    'Suspicious Arrays method calls':
        IssueType.ERROR_PRONE,
    'Suspicious collections method calls':
        IssueType.ERROR_PRONE,
    'Suspicious indentation after control statement without braces':
        IssueType.ERROR_PRONE,
    'Suspicious integer division assignment':
        IssueType.ERROR_PRONE,
    'Suspicious usage of compare method':
        IssueType.ERROR_PRONE,
    'Suspicious variable/parameter name combination':
        IssueType.ERROR_PRONE,
    'Text label in \'switch\' statement':
        IssueType.ERROR_PRONE,
    'Throwable not thrown':
        IssueType.ERROR_PRONE,
    'Unsafe call to \'Class.newInstance()\'':
        IssueType.ERROR_PRONE,
    'Unused assignment':
        IssueType.BEST_PRACTICES,
    'Use of index 0 in JDBC ResultSet':
        IssueType.ERROR_PRONE,
    'Use of Properties object as a Hashtable':
        IssueType.ERROR_PRONE,
    'Wrong package statement':
        IssueType.ERROR_PRONE,

    # Java | Reflective access
    'MethodHandle/VarHandle type mismatch':
        IssueType.ERROR_PRONE,
    'Non-runtime annotation to be used by reflection':
        IssueType.ERROR_PRONE,
    'Reflective access across modules issues':
        IssueType.ERROR_PRONE,
    'Reflective access to nonexistent/not visible class member':
        IssueType.ERROR_PRONE,
    'Reflective invocation arguments mismatch':
        IssueType.ERROR_PRONE,

    # Java | Resource management
    'AutoCloseable used without \'try\'-with-resources':
        IssueType.BEST_PRACTICES,
    'Channel opened but not safely closed':
        IssueType.ERROR_PRONE,
    'Hibernate resource opened but not safely closed':
        IssueType.ERROR_PRONE,
    'I/O resource opened but not safely closed':
        IssueType.ERROR_PRONE,
    'JDBC resource opened but not safely closed':
        IssueType.ERROR_PRONE,
    'JNDI resource opened but not safely closed':
        IssueType.ERROR_PRONE,
    'Socket opened but not safely closed':
        IssueType.ERROR_PRONE,
    'Use of DriverManager to get JDBC connection':
        IssueType.ERROR_PRONE,

    # Java | Security
    'Access of system properties':
        IssueType.BEST_PRACTICES,
    'Call to \'Connection.prepare*()\' with non-constant string':
        IssueType.BEST_PRACTICES,
    'Call to \'Runtime.exec()\' with non-constant string':
        IssueType.BEST_PRACTICES,
    'Call to \'Statement.execute()\' with non-constant string':
        IssueType.BEST_PRACTICES,
    'Call to \'System.loadLibrary()\' with non-constant string':
        IssueType.BEST_PRACTICES,
    'Call to \'System.setSecurityManager()\'':
        IssueType.BEST_PRACTICES,
    'ClassLoader instantiation':
        IssueType.BEST_PRACTICES,
    'Cloneable class in secure context':
        IssueType.BEST_PRACTICES,
    'Custom ClassLoader':
        IssueType.BEST_PRACTICES,
    'Custom SecurityManager':
        IssueType.BEST_PRACTICES,
    'Design for extension':
        IssueType.BEST_PRACTICES,
    'Insecure random number generation':
        IssueType.BEST_PRACTICES,
    'Non-\'static\' inner class in secure context':
        IssueType.BEST_PRACTICES,
    'Non-final \'clone()\' in secure context':
        IssueType.BEST_PRACTICES,
    '\'public static\' array field':
        IssueType.BEST_PRACTICES,
    '\'public static\' collection field':
        IssueType.BEST_PRACTICES,
    'Serializable class in secure context':
        IssueType.BEST_PRACTICES,

    # Java | Serialization issues
    'Comparator class not declared Serializable':
        IssueType.ERROR_PRONE,
    'Externalizable class with \'readObject()\' or \'writeObject()\'':
        IssueType.ERROR_PRONE,
    'Externalizable class without \'public\' no-arg constructor':
        IssueType.ERROR_PRONE,
    'Instance field may not be initialized by \'readObject()\'':
        IssueType.ERROR_PRONE,
    'Non-serializable class with \'readObject()\' or \'writeObject()\'':
        IssueType.ERROR_PRONE,
    'Non-serializable class with \'serialVersionUID\'':
        IssueType.ERROR_PRONE,
    'Non-serializable field in a Serializable class':
        IssueType.ERROR_PRONE,
    'Non-serializable object bound to HttpSession':
        IssueType.ERROR_PRONE,
    'Non-serializable object passed to ObjectOutputStream':
        IssueType.ERROR_PRONE,
    '\'readObject()\' or \'writeObject()\' not declared \'private\'':
        IssueType.ERROR_PRONE,
    '\'readResolve()\' or \'writeReplace()\' not declared \'protected\'':
        IssueType.ERROR_PRONE,
    'Serializable class with unconstructable ancestor':
        IssueType.ERROR_PRONE,
    'Serializable class without \'readObject()\' and \'writeObject()\'':
        IssueType.ERROR_PRONE,
    'Serializable class without \'serialVersionUID\'':
        IssueType.ERROR_PRONE,
    'Serializable non-\'static\' inner class with non-Serializable outer class':
        IssueType.ERROR_PRONE,
    'Serializable non-\'static\' inner class without \'serialVersionUID\'':
        IssueType.ERROR_PRONE,
    'Serializable object implicitly stores non-Serializable object':
        IssueType.ERROR_PRONE,
    '\'serialPersistentFields\' field not declared \'private static final '
    'ObjectStreamField[]\'':
        IssueType.ERROR_PRONE,
    '\'serialVersionUID\' field not declared \'private static final long\'':
        IssueType.ERROR_PRONE,
    'Transient field in non-serializable class':
        IssueType.ERROR_PRONE,
    'Transient field is not initialized on deserialization':
        IssueType.ERROR_PRONE,

    # Java | Threading issues
    'Access to static field locked on instance data':
        IssueType.ERROR_PRONE,
    'AtomicFieldUpdater field not declared \'static final\'':
        IssueType.ERROR_PRONE,
    'AtomicFieldUpdater issues':
        IssueType.ERROR_PRONE,
    '\'await()\' not in loop':
        IssueType.ERROR_PRONE,
    '\'await()\' without corresponding \'signal()\'':
        IssueType.ERROR_PRONE,
    'Busy wait':
        IssueType.ERROR_PRONE,
    'Call to \'notify()\' instead of \'notifyAll()\'':
        IssueType.ERROR_PRONE,
    'Call to \'signal()\' instead of \'signalAll()\'':
        IssueType.ERROR_PRONE,
    'Call to \'System.runFinalizersOnExit()\'':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.run()\'':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.setPriority()\'':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.sleep()\' while synchronized':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.start()\' during object construction':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.stop()\', \'suspend()\' or \'resume()\'':
        IssueType.ERROR_PRONE,
    'Call to \'Thread.yield()\'':
        IssueType.ERROR_PRONE,
    'Call to a native method while locked':
        IssueType.ERROR_PRONE,
    'Class directly extends \'java.lang.Thread\'':
        IssueType.ERROR_PRONE,
    'Double-checked locking':
        IssueType.ERROR_PRONE,
    'Empty \'synchronized\' statement':
        IssueType.ERROR_PRONE,
    'Field accessed in both synchronized and unsynchronized contexts':
        IssueType.ERROR_PRONE,
    'Instantiating a Thread with default \'run()\' method':
        IssueType.ERROR_PRONE,
    'Lock acquired but not safely unlocked':
        IssueType.ERROR_PRONE,
    'Method with synchronized block could be synchronized method':
        IssueType.ERROR_PRONE,
    'Nested \'synchronized\' statement':
        IssueType.ERROR_PRONE,
    'Non-atomic operation on volatile field':
        IssueType.ERROR_PRONE,
    'Non-private field accessed in synchronized context':
        IssueType.ERROR_PRONE,
    'Non thread-safe static field access':
        IssueType.ERROR_PRONE,
    '\'notify()\' or \'notifyAll()\' called on '
    '\'java.util.concurrent.locks.Condition\' object':
        IssueType.ERROR_PRONE,
    '\'notify()\' or \'notifyAll()\' without corresponding state change':
        IssueType.ERROR_PRONE,
    '\'notify()\' without corresponding \'wait()\'':
        IssueType.ERROR_PRONE,
    '\'signal()\' without corresponding \'await()\'':
        IssueType.ERROR_PRONE,
    'Static initializer references subclass':
        IssueType.ERROR_PRONE,
    'Synchronization on \'getClass()\'':
        IssueType.ERROR_PRONE,
    'Synchronization on \'static\' field':
        IssueType.ERROR_PRONE,
    'Synchronization on \'this\'':
        IssueType.ERROR_PRONE,
    'Synchronization on a Lock object':
        IssueType.ERROR_PRONE,
    'Synchronization on a non-final field':
        IssueType.ERROR_PRONE,
    'Synchronization on an object initialized with a literal':
        IssueType.ERROR_PRONE,
    'Synchronization on local variable or method parameter':
        IssueType.ERROR_PRONE,
    '\'synchronized\' method':
        IssueType.ERROR_PRONE,
    'ThreadLocal field not declared static final':
        IssueType.ERROR_PRONE,
    '\'ThreadLocalRandom\' instance might be shared':
        IssueType.ERROR_PRONE,
    'Unconditional \'wait()\' call':
        IssueType.ERROR_PRONE,
    'Unsynchronized method overrides synchronized method':
        IssueType.ERROR_PRONE,
    'Volatile array field':
        IssueType.ERROR_PRONE,
    '\'wait()\' called on \'java.util.concurrent.locks.Condition\' object':
        IssueType.ERROR_PRONE,
    '\'wait()\' not in loop':
        IssueType.ERROR_PRONE,
    '\'wait()\' or \'await()\' without timeout':
        IssueType.ERROR_PRONE,
    '\'wait()\' or \'notify()\' while not synchronized':
        IssueType.ERROR_PRONE,
    '\'wait()\' while holding two locks':
        IssueType.ERROR_PRONE,
    '\'wait()\' without corresponding \'notify()\'':
        IssueType.ERROR_PRONE,
    '\'while\' loop spins on field':
        IssueType.ERROR_PRONE,

    # Java | toString() issues
    'Class does not override \'toString()\' method':
        IssueType.ERROR_PRONE,
    'Field not used in \'toString()\' method':
        IssueType.ERROR_PRONE,

    # Java | Verbose or redundant code constructs
    'Comparator can be simplified':
        IssueType.BEST_PRACTICES,
    'Condition is covered by further condition':
        IssueType.BEST_PRACTICES,
    'Duplicate branches in \'switch\'':
        IssueType.BEST_PRACTICES,
    'Excessive lambda usage':
        IssueType.BEST_PRACTICES,
    'Excessive range check':
        IssueType.BEST_PRACTICES,
    'Explicit array filling':
        IssueType.BEST_PRACTICES,
    'Manual min/max calculation':
        IssueType.BEST_PRACTICES,
    'Multiple occurrences of the same expression':
        IssueType.BEST_PRACTICES,
    'Redundant \'compare\' method call':
        IssueType.BEST_PRACTICES,
    'Redundant \'isInstance\' or \'cast\' call':
        IssueType.BEST_PRACTICES,
    'Redundant array creation':
        IssueType.BEST_PRACTICES,
    'Redundant Collection operation':
        IssueType.BEST_PRACTICES,
    'Redundant String operation':
        IssueType.BEST_PRACTICES,
    'Redundant type arguments':
        IssueType.BEST_PRACTICES,
    'Redundant type cast':
        IssueType.BEST_PRACTICES,
    '\'StringBuilder\' can be replaced with \'String\'':
        IssueType.BEST_PRACTICES,
    'Too weak variable type leads to unnecessary cast':
        IssueType.BEST_PRACTICES,
    'Unnecessary \'break\' statement':
        IssueType.BEST_PRACTICES,
    'Unnecessary \'continue\' statement':
        IssueType.BEST_PRACTICES,
    'Unnecessary \'default\' for enum \'switch\' statement':
        IssueType.BEST_PRACTICES,
    'Unnecessary \'return\' statement':
        IssueType.BEST_PRACTICES,
    'Unnecessary label on \'break\' statement':
        IssueType.BEST_PRACTICES,
    'Unnecessary label on \'continue\' statement':
        IssueType.BEST_PRACTICES,

    # Java | Visibility
    'Access of inherited field looks like access of element in surrounding '
    'code':
        IssueType.BEST_PRACTICES,
    'Anonymous class variable hides variable in containing method':
        IssueType.BEST_PRACTICES,
    'Call to inherited method looks like call to local method':
        IssueType.BEST_PRACTICES,
    'Field name hides field in superclass':
        IssueType.BEST_PRACTICES,
    'Inner class field hides outer class field':
        IssueType.BEST_PRACTICES,
    'Lambda parameter hides field':
        IssueType.BEST_PRACTICES,
    'Local variable hides field':
        IssueType.BEST_PRACTICES,
    'Method overloads method of superclass':
        IssueType.BEST_PRACTICES,
    'Method overrides inaccessible method of superclass':
        IssueType.BEST_PRACTICES,
    'Method tries to override static method of superclass':
        IssueType.BEST_PRACTICES,
    'Module exports/opens package to itself':
        IssueType.BEST_PRACTICES,
    'Non-accessible class is exposed':
        IssueType.BEST_PRACTICES,
    'Parameter hides field':
        IssueType.BEST_PRACTICES,
    'Type parameter hides visible type':
        IssueType.BEST_PRACTICES,
    'Usage of service not declared in \'module-info\'':
        IssueType.BEST_PRACTICES,
}
