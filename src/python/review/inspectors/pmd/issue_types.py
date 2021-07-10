from typing import Dict

from src.python.review.inspectors.issue import IssueType

PMD_RULE_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # ---- Best Practices ----
    'AbstractClassWithoutAbstractMethod': IssueType.BEST_PRACTICES,
    'AccessorClassGeneration': IssueType.BEST_PRACTICES,
    'AccessorMethodGeneration': IssueType.BEST_PRACTICES,
    'ArrayIsStoredDirectly': IssueType.BEST_PRACTICES,
    'AvoidMessageDigestField': IssueType.BEST_PRACTICES,
    'AvoidReassigningCatchVariables': IssueType.BEST_PRACTICES,
    'AvoidReassigningLoopVariables': IssueType.BEST_PRACTICES,
    'AvoidReassigningParameters': IssueType.BEST_PRACTICES,
    'AvoidStringBufferField': IssueType.BEST_PRACTICES,
    'AvoidUsingHardCodedIP': IssueType.BEST_PRACTICES,
    'CheckResultSet': IssueType.BEST_PRACTICES,
    'ConstantsInInterface': IssueType.BEST_PRACTICES,
    'DefaultLabelNotLastInSwitchStmt': IssueType.BEST_PRACTICES,
    'ForLoopCanBeForeach': IssueType.BEST_PRACTICES,
    'ForLoopVariableCount': IssueType.BEST_PRACTICES,
    'LiteralsFirstInComparisons': IssueType.BEST_PRACTICES,
    'MethodReturnsInternalArray': IssueType.BEST_PRACTICES,
    'MissingOverride': IssueType.BEST_PRACTICES,
    'OneDeclarationPerLine': IssueType.CODE_STYLE,
    'PreserveStackTrace': IssueType.BEST_PRACTICES,
    'ReplaceEnumerationWithIterator': IssueType.BEST_PRACTICES,
    'SwitchStmtsShouldHaveDefault': IssueType.ERROR_PRONE,
    'UnusedFormalParameter': IssueType.BEST_PRACTICES,
    'UnusedLocalVariable': IssueType.BEST_PRACTICES,
    'UnusedPrivateField': IssueType.BEST_PRACTICES,
    'UnusedPrivateMethod': IssueType.BEST_PRACTICES,
    'UseCollectionIsEmpty': IssueType.BEST_PRACTICES,
    'UseStandardCharsets': IssueType.BEST_PRACTICES,
    'UseTryWithResources': IssueType.BEST_PRACTICES,
    'WhileLoopWithLiteralBoolean': IssueType.BEST_PRACTICES,
    # 'AvoidPrintStackTrace': IssueType.BEST_PRACTICES,
    # 'DoubleBraceInitialization': IssueType.BEST_PRACTICES,
    # 'GuardLogStatement': IssueType.BEST_PRACTICES,
    # 'JUnit4SuitesShouldUseSuiteAnnotation': IssueType.BEST_PRACTICES,
    # 'JUnit4TestShouldUseAfterAnnotation': IssueType.BEST_PRACTICES,
    # 'JUnit4TestShouldUseBeforeAnnotation': IssueType.BEST_PRACTICES,
    # 'JUnit4TestShouldUseTestAnnotation': IssueType.BEST_PRACTICES,
    # 'JUnit5TestShouldBePackagePrivate': IssueType.BEST_PRACTICES,
    # 'JUnitAssertionsShouldIncludeMessage': IssueType.BEST_PRACTICES,
    # 'JUnitTestContainsTooManyAsserts': IssueType.BEST_PRACTICES,
    # 'JUnitTestsShouldIncludeAssert': IssueType.BEST_PRACTICES,
    # 'JUnitUseExpected': IssueType.BEST_PRACTICES,
    # 'LooseCoupling': IssueType.BEST_PRACTICES,
    # 'PositionLiteralsFirstInCaseInsensitiveComparisons': IssueType.BEST_PRACTICES,
    # 'PositionLiteralsFirstInComparisons': IssueType.BEST_PRACTICES,
    # 'ReplaceHashtableWithMap': IssueType.BEST_PRACTICES,
    # 'ReplaceVectorWithList': IssueType.BEST_PRACTICES,
    # 'SystemPrintln': IssueType.BEST_PRACTICES,
    # 'UnusedAssignment': IssueType.BEST_PRACTICES,
    # 'UnusedImports': IssueType.BEST_PRACTICES,
    # 'UseAssertEqualsInsteadOfAssertTrue': IssueType.BEST_PRACTICES,
    # 'UseAssertNullInsteadOfAssertTrue': IssueType.BEST_PRACTICES,
    # 'UseAssertSameInsteadOfAssertTrue': IssueType.BEST_PRACTICES,
    # 'UseAssertTrueInsteadOfAssertEquals': IssueType.BEST_PRACTICES,
    # 'UseVarargs': IssueType.BEST_PRACTICES,

    # ---- Code Style ----
    'AvoidDollarSigns': IssueType.CODE_STYLE,
    'AvoidProtectedFieldInFinalClass': IssueType.BEST_PRACTICES,
    'AvoidProtectedMethodInFinalClassNotExtending': IssueType.CODE_STYLE,
    'BooleanGetMethodName': IssueType.CODE_STYLE,
    'CallSuperInConstructor': IssueType.CODE_STYLE,
    'ClassNamingConventions': IssueType.CODE_STYLE,
    'ControlStatementBraces': IssueType.CODE_STYLE,
    'EmptyMethodInAbstractClassShouldBeAbstract': IssueType.BEST_PRACTICES,
    'ExtendsObject': IssueType.BEST_PRACTICES,
    'FieldDeclarationsShouldBeAtStartOfClass': IssueType.CODE_STYLE,
    'FieldNamingConventions': IssueType.CODE_STYLE,
    'ForLoopShouldBeWhileLoop': IssueType.BEST_PRACTICES,
    'FormalParameterNamingConventions': IssueType.CODE_STYLE,
    'IdenticalCatchBranches': IssueType.BEST_PRACTICES,
    'LocalVariableNamingConventions': IssueType.CODE_STYLE,
    'MethodNamingConventions': IssueType.CODE_STYLE,
    'PackageCase': IssueType.CODE_STYLE,
    'UnnecessaryCast': IssueType.BEST_PRACTICES,
    'UnnecessaryConstructor': IssueType.BEST_PRACTICES,
    'UnnecessaryFullyQualifiedName': IssueType.CODE_STYLE,
    'UnnecessaryImport': IssueType.BEST_PRACTICES,
    'UnnecessaryLocalBeforeReturn': IssueType.CODE_STYLE,
    'UnnecessaryReturn': IssueType.CODE_STYLE,
    'UseDiamondOperator': IssueType.CODE_STYLE,
    'UselessParentheses': IssueType.CODE_STYLE,
    'UselessQualifiedThis': IssueType.CODE_STYLE,
    'UseShortArrayInitializer': IssueType.BEST_PRACTICES,
    # 'AbstractNaming': IssueType.CODE_STYLE,
    # 'AtLeastOneConstructor': IssueType.CODE_STYLE,
    # 'AvoidFinalLocalVariable': IssueType.CODE_STYLE,
    # 'AvoidPrefixingMethodParameters': IssueType.CODE_STYLE,
    # 'AvoidUsingNativeCode': IssueType.BEST_PRACTICES,
    # 'CommentDefaultAccessModifier': IssueType.CODE_STYLE,
    # 'ConfusingTernary': IssueType.BEST_PRACTICES,
    # 'DefaultPackage': IssueType.BEST_PRACTICES,
    # 'DontImportJavaLang': IssueType.BEST_PRACTICES,
    # 'DuplicateImports': IssueType.BEST_PRACTICES,
    # 'ForLoopsMustUseBraces': IssueType.CODE_STYLE,
    # 'GenericsNaming': IssueType.CODE_STYLE,
    # 'IfElseStmtsMustUseBraces': IssueType.CODE_STYLE,
    # 'IfStmtsMustUseBraces': IssueType.CODE_STYLE,
    # 'LinguisticNaming': IssueType.CODE_STYLE,
    # 'LocalHomeNamingConvention': IssueType.CODE_STYLE,
    # 'LocalInterfaceSessionNamingConvention': IssueType.CODE_STYLE,
    # 'LocalVariableCouldBeFinal': IssueType.CODE_STYLE,
    # 'LongVariable': IssueType.CODE_STYLE,
    # 'MDBAndSessionBeanNamingConvention': IssueType.CODE_STYLE,
    # 'MethodArgumentCouldBeFinal': IssueType.CODE_STYLE,
    # 'MIsLeadingVariableName': IssueType.CODE_STYLE,
    # 'NoPackage': IssueType.BEST_PRACTICES,
    # 'OnlyOneReturn': IssueType.BEST_PRACTICES,
    # 'UnnecessaryModifier': IssueType.CODE_STYLE,
    # 'UseUnderscoresInNumericLiterals': IssueType.BEST_PRACTICES,
    # 'VariableNamingConventions': IssueType.CODE_STYLE,
    # 'WhileLoopsMustUseBraces': IssueType.CODE_STYLE,

    # ---- Design ----
    'AvoidDeeplyNestedIfStmts': IssueType.COMPLEXITY,
    'AvoidRethrowingException': IssueType.BEST_PRACTICES,
    'AvoidThrowingNewInstanceOfSameException': IssueType.BEST_PRACTICES,
    'AvoidUncheckedExceptionsInSignatures': IssueType.BEST_PRACTICES,
    'CollapsibleIfStatements': IssueType.BEST_PRACTICES,
    'DoNotExtendJavaLangError': IssueType.BEST_PRACTICES,
    'ExcessiveParameterList': IssueType.BEST_PRACTICES,
    'ExcessivePublicCount': IssueType.BEST_PRACTICES,
    'GodClass': IssueType.BEST_PRACTICES,
    'LogicInversion': IssueType.BEST_PRACTICES,
    'SimplifiedTernary': IssueType.BEST_PRACTICES,
    'SimplifyBooleanAssertion': IssueType.BEST_PRACTICES,
    'SimplifyBooleanExpressions': IssueType.BEST_PRACTICES,
    'SimplifyBooleanReturns': IssueType.BEST_PRACTICES,
    'SimplifyConditional': IssueType.BEST_PRACTICES,
    'SingularField': IssueType.BEST_PRACTICES,
    'SwitchDensity': IssueType.COMPLEXITY,
    'TooManyFields': IssueType.COMPLEXITY,
    'UselessOverridingMethod': IssueType.BEST_PRACTICES,
    'UseObjectForClearerAPI': IssueType.BEST_PRACTICES,
    # 'AbstractClassWithoutAnyMethod': IssueType.BEST_PRACTICES,
    # 'AvoidCatchingGenericException': IssueType.BEST_PRACTICES,
    # 'AvoidThrowingNullPointerException': IssueType.BEST_PRACTICES,
    # 'AvoidThrowingRawExceptionTypes': IssueType.BEST_PRACTICES,
    # 'ClassWithOnlyPrivateConstructorsShouldBeFinal': IssueType.BEST_PRACTICES,
    # 'CognitiveComplexity': IssueType.COMPLEXITY,
    # 'CouplingBetweenObjects': IssueType.BEST_PRACTICES,
    # 'CyclomaticComplexity': IssueType.COMPLEXITY,
    # 'DataClass': IssueType.BEST_PRACTICES,
    # 'ExceptionAsFlowControl': IssueType.BEST_PRACTICES,
    # 'ExcessiveClassLength': IssueType.BEST_PRACTICES,
    # 'ExcessiveImports': IssueType.BEST_PRACTICES,
    # 'ExcessiveMethodLength': IssueType.COMPLEXITY,
    # 'FinalFieldCouldBeStatic': IssueType.BEST_PRACTICES,
    # 'ImmutableField': IssueType.BEST_PRACTICES,
    # 'LawOfDemeter': IssueType.BEST_PRACTICES,
    # 'LoosePackageCoupling': IssueType.BEST_PRACTICES,
    # 'ModifiedCyclomaticComplexity': IssueType.COMPLEXITY,
    # 'MutableStaticState': IssueType.BEST_PRACTICES,
    # 'NcssConstructorCount': IssueType.COMPLEXITY,
    # 'NcssCount': IssueType.COMPLEXITY,
    # 'NcssMethodCount': IssueType.COMPLEXITY,
    # 'NcssTypeCount': IssueType.COMPLEXITY,
    # 'NPathComplexity': IssueType.COMPLEXITY,
    # 'SignatureDeclareThrowsException': IssueType.BEST_PRACTICES,
    # 'StdCyclomaticComplexity': IssueType.COMPLEXITY,
    # 'TooManyMethods': IssueType.COMPLEXITY,
    # 'UseUtilityClass': IssueType.BEST_PRACTICES,

    # ---- Documentation ----
    'UncommentedEmptyConstructor': IssueType.BEST_PRACTICES,
    'UncommentedEmptyMethodBody': IssueType.BEST_PRACTICES,
    # 'CommentContent': IssueType.BEST_PRACTICES,
    # 'CommentRequired': IssueType.BEST_PRACTICES,
    # 'CommentSize': IssueType.BEST_PRACTICES,

    # ---- Error Prone ----
    'AssignmentInOperand': IssueType.ERROR_PRONE,
    'AvoidAssertAsIdentifier': IssueType.ERROR_PRONE,
    'AvoidBranchingStatementAsLastInLoop': IssueType.BEST_PRACTICES,
    'AvoidCallingFinalize': IssueType.ERROR_PRONE,
    'AvoidCatchingNPE': IssueType.ERROR_PRONE,
    'AvoidCatchingThrowable': IssueType.ERROR_PRONE,
    'AvoidDecimalLiteralsInBigDecimalConstructor': IssueType.ERROR_PRONE,
    'AvoidDuplicateLiterals': IssueType.BEST_PRACTICES,
    'AvoidEnumAsIdentifier': IssueType.ERROR_PRONE,
    'AvoidFieldNameMatchingMethodName': IssueType.BEST_PRACTICES,
    'AvoidFieldNameMatchingTypeName': IssueType.BEST_PRACTICES,
    'AvoidInstanceofChecksInCatchClause': IssueType.BEST_PRACTICES,
    'AvoidLiteralsInIfCondition': IssueType.INFO,
    'AvoidLosingExceptionInformation': IssueType.ERROR_PRONE,
    'AvoidMultipleUnaryOperators': IssueType.ERROR_PRONE,
    'AvoidUsingOctalValues': IssueType.BEST_PRACTICES,
    'BrokenNullCheck': IssueType.ERROR_PRONE,
    'CheckSkipResult': IssueType.ERROR_PRONE,
    'ClassCastExceptionWithToArray': IssueType.ERROR_PRONE,
    'CompareObjectsWithEquals': IssueType.ERROR_PRONE,
    'ComparisonWithNaN': IssueType.ERROR_PRONE,
    'ConstructorCallsOverridableMethod': IssueType.ERROR_PRONE,
    'DoNotExtendJavaLangThrowable': IssueType.ERROR_PRONE,
    'DontUseFloatTypeForLoopIndices': IssueType.ERROR_PRONE,
    'EmptyCatchBlock': IssueType.BEST_PRACTICES,
    'EmptyFinalizer': IssueType.BEST_PRACTICES,
    'EmptyFinallyBlock': IssueType.BEST_PRACTICES,
    'EmptyIfStmt': IssueType.BEST_PRACTICES,
    'EmptyInitializer': IssueType.BEST_PRACTICES,
    'EmptyStatementBlock': IssueType.BEST_PRACTICES,
    'EmptyStatementNotInLoop': IssueType.BEST_PRACTICES,
    'EmptySwitchStatements': IssueType.BEST_PRACTICES,
    'EmptySynchronizedBlock': IssueType.BEST_PRACTICES,
    'EmptyTryBlock': IssueType.BEST_PRACTICES,
    'EmptyWhileStmt': IssueType.BEST_PRACTICES,
    'EqualsNull': IssueType.ERROR_PRONE,
    'FinalizeDoesNotCallSuperFinalize': IssueType.ERROR_PRONE,
    'FinalizeOnlyCallsSuperFinalize': IssueType.ERROR_PRONE,
    'FinalizeOverloaded': IssueType.ERROR_PRONE,
    'FinalizeShouldBeProtected': IssueType.ERROR_PRONE,
    'IdempotentOperations': IssueType.BEST_PRACTICES,
    'InstantiationToGetClass': IssueType.ERROR_PRONE,
    'JumbledIncrementer': IssueType.ERROR_PRONE,
    'MethodWithSameNameAsEnclosingClass': IssueType.BEST_PRACTICES,
    'MisplacedNullCheck': IssueType.ERROR_PRONE,
    'MissingBreakInSwitch': IssueType.ERROR_PRONE,
    'MissingSerialVersionUID': IssueType.ERROR_PRONE,
    'MissingStaticMethodInNonInstantiatableClass': IssueType.ERROR_PRONE,
    'NonCaseLabelInSwitchStatement': IssueType.BEST_PRACTICES,
    'OverrideBothEqualsAndHashcode': IssueType.ERROR_PRONE,
    'ProperCloneImplementation': IssueType.ERROR_PRONE,
    'ReturnEmptyArrayRatherThanNull': IssueType.ERROR_PRONE,
    'ReturnFromFinallyBlock': IssueType.BEST_PRACTICES,
    'SimpleDateFormatNeedsLocale': IssueType.BEST_PRACTICES,
    'SingleMethodSingleton': IssueType.ERROR_PRONE,
    'SingletonClassReturningNewInstance': IssueType.ERROR_PRONE,
    'StringBufferInstantiationWithChar': IssueType.ERROR_PRONE,
    'SuspiciousEqualsMethodName': IssueType.ERROR_PRONE,
    'SuspiciousHashcodeMethodName': IssueType.ERROR_PRONE,
    'UnconditionalIfStatement': IssueType.BEST_PRACTICES,
    'UnnecessaryBooleanAssertion': IssueType.BEST_PRACTICES,
    'UnnecessaryCaseChange': IssueType.BEST_PRACTICES,
    'UnnecessaryConversionTemporary': IssueType.BEST_PRACTICES,
    'UseEqualsToCompareStrings': IssueType.ERROR_PRONE,
    # 'AssignmentToNonFinalStatic': IssueType.ERROR_PRONE,
    # 'AvoidAccessibilityAlteration': IssueType.ERROR_PRONE,
    # 'BadComparison': IssueType.ERROR_PRONE,
    # 'BeanMembersShouldSerialize': IssueType.ERROR_PRONE,
    # 'CallSuperFirst': IssueType.ERROR_PRONE,
    # 'CallSuperLast': IssueType.ERROR_PRONE,
    # 'CloneMethodMustBePublic': IssueType.ERROR_PRONE,
    # 'CloneMethodMustImplementCloneable': IssueType.ERROR_PRONE,
    # 'CloneMethodReturnTypeMustMatchClassName': IssueType.ERROR_PRONE,
    # 'CloneThrowsCloneNotSupportedException': IssueType.ERROR_PRONE,
    # 'CloseResource': IssueType.ERROR_PRONE,
    # 'DataflowAnomalyAnalysis': IssueType.ERROR_PRONE,
    # 'DetachedTestCase': IssueType.ERROR_PRONE,
    # 'DoNotCallGarbageCollectionExplicitly': IssueType.ERROR_PRONE,
    # 'DoNotCallSystemExit': IssueType.ERROR_PRONE,
    # 'DoNotHardCodeSDCard': IssueType.ERROR_PRONE,
    # 'DoNotTerminateVM': IssueType.ERROR_PRONE,
    # 'DoNotThrowExceptionInFinally': IssueType.ERROR_PRONE,
    # 'DontImportSun': IssueType.ERROR_PRONE,
    # 'ImportFromSamePackage': IssueType.BEST_PRACTICES,
    # 'InvalidLogMessageFormat': IssueType.ERROR_PRONE,
    # 'InvalidSlf4jMessageFormat': IssueType.ERROR_PRONE,
    # 'JUnitSpelling': IssueType.ERROR_PRONE,
    # 'JUnitStaticSuite': IssueType.ERROR_PRONE,
    # 'LoggerIsNotStaticFinal': IssueType.ERROR_PRONE,
    # 'MoreThanOneLogger': IssueType.ERROR_PRONE,
    # 'NonStaticInitializer': IssueType.ERROR_PRONE,
    # 'NullAssignment': IssueType.ERROR_PRONE,
    # 'ProperLogger': IssueType.ERROR_PRONE,
    # 'StaticEJBFieldShouldBeFinal': IssueType.ERROR_PRONE,
    # 'SuspiciousOctalEscape': IssueType.ERROR_PRONE,
    # 'TestClassWithoutTestCases': IssueType.ERROR_PRONE,
    # 'UnusedNullCheckInEquals': IssueType.ERROR_PRONE,
    # 'UseCorrectExceptionLogging': IssueType.ERROR_PRONE,
    # 'UselessOperationOnImmutable': IssueType.ERROR_PRONE,
    # 'UseLocaleWithCaseConversions': IssueType.ERROR_PRONE,
    # 'UseProperClassLoader': IssueType.ERROR_PRONE,

    # ---- Multithreading ----
    'AvoidThreadGroup': IssueType.ERROR_PRONE,
    'DontCallThreadRun': IssueType.ERROR_PRONE,
    'DoubleCheckedLocking': IssueType.ERROR_PRONE,
    'UnsynchronizedStaticFormatter': IssueType.ERROR_PRONE,
    'UseNotifyAllInsteadOfNotify': IssueType.ERROR_PRONE,
    # 'AvoidSynchronizedAtMethodLevel': IssueType.BEST_PRACTICES,
    # 'AvoidUsingVolatile': IssueType.ERROR_PRONE,
    # 'DoNotUseThreads': IssueType.ERROR_PRONE,
    # 'NonThreadSafeSingleton': IssueType.ERROR_PRONE,
    # 'UnsynchronizedStaticDateFormatter': IssueType.ERROR_PRONE,
    # 'UseConcurrentHashMap': IssueType.ERROR_PRONE,

    # ---- Performance ----
    'AddEmptyString': IssueType.BEST_PRACTICES,
    'AvoidArrayLoops': IssueType.BEST_PRACTICES,
    'ConsecutiveAppendsShouldReuse': IssueType.BEST_PRACTICES,
    'ConsecutiveLiteralAppends': IssueType.BEST_PRACTICES,
    'InefficientStringBuffering': IssueType.BEST_PRACTICES,
    'OptimizableToArrayCall': IssueType.BEST_PRACTICES,
    'StringToString': IssueType.BEST_PRACTICES,
    'TooFewBranchesForASwitchStatement': IssueType.BEST_PRACTICES,
    'UnnecessaryWrapperObjectCreation': IssueType.BEST_PRACTICES,
    'UseArraysAsList': IssueType.BEST_PRACTICES,
    'UselessStringValueOf': IssueType.BEST_PRACTICES,
    'UseStringBufferLength': IssueType.BEST_PRACTICES,
    # 'AppendCharacterWithChar': IssueType.BEST_PRACTICES,
    # 'AvoidCalendarDateCreation': IssueType.BEST_PRACTICES,
    # 'AvoidFileStream': IssueType.BEST_PRACTICES,
    # 'AvoidInstantiatingObjectsInLoops': IssueType.BEST_PRACTICES,
    # 'AvoidUsingShortType': IssueType.BEST_PRACTICES,
    # 'BigIntegerInstantiation': IssueType.BEST_PRACTICES,
    # 'BooleanInstantiation': IssueType.BEST_PRACTICES,
    # 'ByteInstantiation': IssueType.BEST_PRACTICES,
    # 'InefficientEmptyStringCheck': IssueType.BEST_PRACTICES,
    # 'InsufficientStringBufferDeclaration': IssueType.BEST_PRACTICES,
    # 'IntegerInstantiation': IssueType.BEST_PRACTICES,
    # 'LongInstantiation': IssueType.BEST_PRACTICES,
    # 'RedundantFieldInitializer': IssueType.BEST_PRACTICES,
    # 'ShortInstantiation': IssueType.BEST_PRACTICES,
    # 'SimplifyStartsWith': IssueType.BEST_PRACTICES,
    # 'StringInstantiation': IssueType.BEST_PRACTICES,
    # 'UseArrayListInsteadOfVector': IssueType.BEST_PRACTICES,
    # 'UseIndexOfChar': IssueType.BEST_PRACTICES,
    # 'UseIOStreamsWithApacheCommonsFileItem': IssueType.BEST_PRACTICES,
    # 'UseStringBufferForStringAppends': IssueType.BEST_PRACTICES,

    # ---- Security ----
    'HardCodedCryptoKey': IssueType.BEST_PRACTICES,
    'InsecureCryptoIv': IssueType.BEST_PRACTICES,
}
