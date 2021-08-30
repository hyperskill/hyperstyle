from typing import Dict

from src.python.review.inspectors.issue import IssueType

DETECT_CLASS_NAME_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # Comments
    # 'AbsentOrWrongFileLicense': IssueType.BEST_PRACTICES,
    # 'CommentOverPrivateFunction': IssueType.BEST_PRACTICES,
    # 'CommentOverPrivateProperty': IssueType.BEST_PRACTICES,
    # 'DeprecatedBlockTag': IssueType.BEST_PRACTICES,
    # 'EndOfSentenceFormat': IssueType.CODE_STYLE,
    # 'UndocumentedPublicClass': IssueType.BEST_PRACTICES,
    # 'UndocumentedPublicFunction': IssueType.BEST_PRACTICES,
    # 'UndocumentedPublicProperty': IssueType.BEST_PRACTICES,

    # Complexity
    'ComplexCondition': IssueType.BOOL_EXPR_LEN,
    # 'ComplexInterface': IssueType.COMPLEXITY,
    'ComplexMethod': IssueType.CYCLOMATIC_COMPLEXITY,
    # 'LabeledExpression': IssueType.COMPLEXITY,
    'LargeClass': IssueType.COMPLEXITY,
    'LongMethod': IssueType.FUNC_LEN,
    'LongParameterList': IssueType.COMPLEXITY,
    # 'MethodOverloading': IssueType.COMPLEXITY,
    # 'NamedArguments': IssueType.COMPLEXITY,
    'NestedBlockDepth': IssueType.COMPLEXITY,
    # 'ReplaceSafeCallChainWithRun': IssueType.BEST_PRACTICES,
    'StringLiteralDuplication': IssueType.BEST_PRACTICES,
    'TooManyFunctions': IssueType.COMPLEXITY,

    # Coroutines
    # 'GlobalCoroutineUsage': IssueType.BEST_PRACTICES,
    # 'RedundantSuspendModifier': IssueType.BEST_PRACTICES,
    # 'SleepInsteadOfDelay': IssueType.BEST_PRACTICES,
    # 'SuspendFunWithFlowReturnType': IssueType.BEST_PRACTICES,

    # Empty-blocks
    'EmptyCatchBlock': IssueType.BEST_PRACTICES,
    'EmptyClassBlock': IssueType.BEST_PRACTICES,
    'EmptyDefaultConstructor': IssueType.BEST_PRACTICES,
    'EmptyDoWhileBlock': IssueType.BEST_PRACTICES,
    'EmptyElseBlock': IssueType.BEST_PRACTICES,
    'EmptyFinallyBlock': IssueType.BEST_PRACTICES,
    'EmptyForBlock': IssueType.BEST_PRACTICES,
    'EmptyFunctionBlock': IssueType.BEST_PRACTICES,
    'EmptyIfBlock': IssueType.BEST_PRACTICES,
    'EmptyInitBlock': IssueType.BEST_PRACTICES,
    'EmptyKtFile': IssueType.BEST_PRACTICES,
    'EmptySecondaryConstructor': IssueType.BEST_PRACTICES,
    'EmptyTryBlock': IssueType.BEST_PRACTICES,
    'EmptyWhenBlock': IssueType.BEST_PRACTICES,
    'EmptyWhileBlock': IssueType.BEST_PRACTICES,

    # Exceptions
    'ExceptionRaisedInUnexpectedLocation': IssueType.BEST_PRACTICES,
    # 'InstanceOfCheckForException': IssueType.BEST_PRACTICES,
    # 'NotImplementedDeclaration': IssueType.BEST_PRACTICES,
    # 'ObjectExtendsThrowable': IssueType.BEST_PRACTICES,
    # 'PrintStackTrace': IssueType.BEST_PRACTICES,
    'RethrowCaughtException': IssueType.BEST_PRACTICES,
    'ReturnFromFinally': IssueType.BEST_PRACTICES,
    # 'SwallowedException': IssueType.BEST_PRACTICES,
    'ThrowingExceptionFromFinally': IssueType.BEST_PRACTICES,
    # 'ThrowingExceptionInMain': IssueType.BEST_PRACTICES,
    'ThrowingExceptionsWithoutMessageOrCause': IssueType.BEST_PRACTICES,
    # 'ThrowingNewInstanceOfSameException': IssueType.BEST_PRACTICES,
    # 'TooGenericExceptionCaught': IssueType.BEST_PRACTICES,
    # 'TooGenericExceptionThrown': IssueType.BEST_PRACTICES,

    # Naming
    # 'BooleanPropertyNaming': IssueType.INFO,
    'ClassNaming': IssueType.CODE_STYLE,
    'ConstructorParameterNaming': IssueType.CODE_STYLE,
    'EnumNaming': IssueType.CODE_STYLE,
    # 'ForbiddenClassName': IssueType.CODE_STYLE,
    # 'FunctionMaxLength': IssueType.CODE_STYLE,
    # 'FunctionMinLength': IssueType.CODE_STYLE,
    'FunctionNaming': IssueType.CODE_STYLE,
    'FunctionParameterNaming': IssueType.CODE_STYLE,
    # 'InvalidPackageDeclaration': IssueType.ERROR_PRONE,
    # 'MatchingDeclarationName': IssueType.CODE_STYLE,
    # 'MemberNameEqualsClassName': IssueType.BEST_PRACTICES,
    # 'NoNameShadowing': IssueType.ERROR_PRONE,
    'NonBooleanPropertyPrefixedWithIs': IssueType.INFO,
    'ObjectPropertyNaming': IssueType.CODE_STYLE,
    'PackageNaming': IssueType.CODE_STYLE,
    'TopLevelPropertyNaming': IssueType.CODE_STYLE,
    # 'VariableMaxLength': IssueType.CODE_STYLE,
    # 'VariableMinLength': IssueType.CODE_STYLE,
    'VariableNaming': IssueType.CODE_STYLE,

    # Performance
    'ArrayPrimitive': IssueType.BEST_PRACTICES,
    'ForEachOnRange': IssueType.BEST_PRACTICES,
    'SpreadOperator': IssueType.BEST_PRACTICES,
    'UnnecessaryTemporaryInstantiation': IssueType.BEST_PRACTICES,

    # Potential bugs
    # 'AvoidReferentialEquality': IssueType.ERROR_PRONE,
    # 'CastToNullableType': IssueType.ERROR_PRONE,
    # 'Deprecation': IssueType.ERROR_PRONE,
    # 'DontDowncastCollectionTypes': IssueType.ERROR_PRONE,
    # 'DoubleMutabilityForCollection': IssueType.BEST_PRACTICES,
    'DuplicateCaseInWhenExpression': IssueType.ERROR_PRONE,
    'EqualsAlwaysReturnsTrueOrFalse': IssueType.ERROR_PRONE,
    'EqualsWithHashCodeExist': IssueType.ERROR_PRONE,
    # 'ExitOutsideMain': IssueType.BEST_PRACTICES,
    'ExplicitGarbageCollectionCall': IssueType.ERROR_PRONE,
    # 'HasPlatformType': IssueType.ERROR_PRONE,
    # 'IgnoredReturnValue': IssueType.ERROR_PRONE,
    # 'ImplicitDefaultLocale': IssueType.ERROR_PRONE,
    # 'ImplicitUnitReturnType': IssueType.ERROR_PRONE,
    'InvalidRange': IssueType.ERROR_PRONE,
    'IteratorHasNextCallsNextMethod': IssueType.ERROR_PRONE,
    'IteratorNotThrowingNoSuchElementException': IssueType.ERROR_PRONE,
    # 'LateinitUsage': IssueType.ERROR_PRONE,
    'MapGetWithNotNullAssertionOperator': IssueType.ERROR_PRONE,
    'MissingWhenCase': IssueType.ERROR_PRONE,
    'NullableToStringCall': IssueType.BEST_PRACTICES,
    'RedundantElseInWhen': IssueType.ERROR_PRONE,
    'UnconditionalJumpStatementInLoop': IssueType.ERROR_PRONE,
    'UnnecessaryNotNullOperator': IssueType.ERROR_PRONE,
    'UnnecessarySafeCall': IssueType.ERROR_PRONE,
    # 'UnreachableCatchBlock': IssueType.ERROR_PRONE,
    'UnreachableCode': IssueType.ERROR_PRONE,
    'UnsafeCallOnNullableType': IssueType.ERROR_PRONE,
    # 'UnusedUnaryOperator': IssueType.ERROR_PRONE,
    'UnsafeCast': IssueType.ERROR_PRONE,
    'UselessPostfixExpression': IssueType.ERROR_PRONE,
    'WrongEqualsTypeParameter': IssueType.ERROR_PRONE,

    # Formatting
    # 'AnnotationOnSeparateLine': IssueType.CODE_STYLE,
    # 'AnnotationSpacing': IssueType.CODE_STYLE,
    # 'ArgumentListWrapping': IssueType.CODE_STYLE,
    'ChainWrapping': IssueType.CODE_STYLE,
    'CommentSpacing': IssueType.CODE_STYLE,
    'EnumEntryNameCase': IssueType.CODE_STYLE,
    # 'Filename': IssueType.CODE_STYLE,
    # 'FinalNewline': IssueType.CODE_STYLE,
    'ImportOrdering': IssueType.CODE_STYLE,
    'Indentation': IssueType.CODE_STYLE,
    # 'MaximumLineLength': IssueType.CODE_STYLE,
    # 'ModifierOrdering': IssueType.CODE_STYLE,
    'MultiLineIfElse': IssueType.CODE_STYLE,
    # 'NoBlankLineBeforeRbrace': IssueType.CODE_STYLE,
    'NoConsecutiveBlankLines': IssueType.CODE_STYLE,
    # 'NoEmptyClassBody': IssueType.CODE_STYLE,
    # 'NoEmptyFirstLineInMethodBlock': IssueType.CODE_STYLE,
    'NoLineBreakAfterElse': IssueType.CODE_STYLE,
    'NoLineBreakBeforeAssignment': IssueType.CODE_STYLE,
    'NoMultipleSpaces': IssueType.CODE_STYLE,
    'NoSemicolons': IssueType.CODE_STYLE,
    # 'NoTrailingSpaces': IssueType.CODE_STYLE,
    # 'NoUnitReturn': IssueType.CODE_STYLE,
    # 'NoUnusedImports': IssueType.CODE_STYLE,
    # 'NoWildcardImports': IssueType.CODE_STYLE,
    # 'PackageName': IssueType.CODE_STYLE,
    'ParameterListWrapping': IssueType.CODE_STYLE,
    # 'SpacingAroundAngleBrackets': IssueType.CODE_STYLE,
    'SpacingAroundColon': IssueType.CODE_STYLE,
    'SpacingAroundComma': IssueType.CODE_STYLE,
    'SpacingAroundCurly': IssueType.CODE_STYLE,
    'SpacingAroundDot': IssueType.CODE_STYLE,
    # 'SpacingAroundDoubleColon': IssueType.CODE_STYLE,
    'SpacingAroundKeyword': IssueType.CODE_STYLE,
    'SpacingAroundOperators': IssueType.CODE_STYLE,
    'SpacingAroundParens': IssueType.CODE_STYLE,
    'SpacingAroundRangeOperator': IssueType.CODE_STYLE,
    # 'SpacingAroundUnaryOperator': IssueType.CODE_STYLE,
    # 'SpacingBetweenDeclarationsWithAnnotations': IssueType.CODE_STYLE,
    # 'SpacingBetweenDeclarationsWithComments': IssueType.CODE_STYLE,
    'StringTemplate': IssueType.CODE_STYLE,

    # Style
    # 'ClassOrdering': IssueType.BEST_PRACTICES,
    'CollapsibleIfStatements': IssueType.BEST_PRACTICES,
    # 'DataClassContainsFunctions': IssueType.BEST_PRACTICES,
    # 'DataClassShouldBeImmutable': IssueType.BEST_PRACTICES,
    # 'DestructuringDeclarationWithTooManyEntries': IssueType.BEST_PRACTICES,
    'EqualsNullCall': IssueType.BEST_PRACTICES,
    # 'EqualsOnSignatureLine': IssueType.CODE_STYLE,
    # 'ExplicitCollectionElementAccessMethod': IssueType.BEST_PRACTICES,
    # 'ExplicitItLambdaParameter': IssueType.BEST_PRACTICES,
    # 'ExpressionBodySyntax': IssueType.BEST_PRACTICES,
    # 'ForbiddenComment': IssueType.BEST_PRACTICES,
    # 'ForbiddenImport': IssueType.BEST_PRACTICES,
    # 'ForbiddenMethodCall': IssueType.BEST_PRACTICES,
    # 'ForbiddenPublicDataClass': IssueType.BEST_PRACTICES,
    # 'ForbiddenVoid': IssueType.BEST_PRACTICES,
    # 'FunctionOnlyReturningConstant': IssueType.BEST_PRACTICES,
    'LibraryCodeMustSpecifyReturnType': IssueType.BEST_PRACTICES,
    # 'LibraryEntitiesShouldNotBePublic': IssueType.BEST_PRACTICES,
    # 'LoopWithTooManyJumpStatements': IssueType.COMPLEXITY,
    'MagicNumber': IssueType.INFO,
    'MandatoryBracesIfStatements': IssueType.CODE_STYLE,
    'MandatoryBracesLoops': IssueType.CODE_STYLE,
    # TODO: Change to LINE_LEN when Detekt is able to display the line length in the message to this inspection
    'MaxLineLength': IssueType.CODE_STYLE,
    'MayBeConst': IssueType.BEST_PRACTICES,
    'ModifierOrder': IssueType.CODE_STYLE,
    # 'MultilineLambdaItParameter': IssueType.BEST_PRACTICES,
    # 'NestedClassesVisibility': IssueType.BEST_PRACTICES,
    # 'NewLineAtEndOfFile': IssueType.CODE_STYLE,
    # 'NoTabs': IssueType.CODE_STYLE,
    # 'ObjectLiteralToLambda': IssueType.BEST_PRACTICES,
    'OptionalAbstractKeyword': IssueType.CODE_STYLE,
    'OptionalUnit': IssueType.CODE_STYLE,
    'OptionalWhenBraces': IssueType.CODE_STYLE,
    # 'PreferToOverPairSyntax': IssueType.BEST_PRACTICES,
    'ProtectedMemberInFinalClass': IssueType.BEST_PRACTICES,
    'RedundantExplicitType': IssueType.CODE_STYLE,
    # 'RedundantHigherOrderMapUsage': IssueType.BEST_PRACTICES,
    'RedundantVisibilityModifierRule': IssueType.CODE_STYLE,
    # 'ReturnCount': IssueType.COMPLEXITY,
    'SafeCast': IssueType.BEST_PRACTICES,
    # 'SerialVersionUIDInSerializableClass': IssueType.BEST_PRACTICES,
    'SpacingBetweenPackageAndImports': IssueType.CODE_STYLE,
    # 'ThrowsCount': IssueType.COMPLEXITY,
    # 'TrailingWhitespace': IssueType.CODE_STYLE,
    # 'UnderscoresInNumericLiterals': IssueType.CODE_STYLE,
    'UnnecessaryAbstractClass': IssueType.BEST_PRACTICES,
    # 'UnnecessaryAnnotationUseSiteTarget': IssueType.BEST_PRACTICES,
    'UnnecessaryApply': IssueType.BEST_PRACTICES,
    # 'UnnecessaryFilter': IssueType.BEST_PRACTICES,
    'UnnecessaryInheritance': IssueType.BEST_PRACTICES,
    'UnnecessaryLet': IssueType.BEST_PRACTICES,
    'UnnecessaryParentheses': IssueType.CODE_STYLE,
    # 'UntilInsteadOfRangeTo': IssueType.BEST_PRACTICES,
    'UnusedImports': IssueType.BEST_PRACTICES,
    'UnusedPrivateClass': IssueType.BEST_PRACTICES,
    # 'UnusedPrivateMember': IssueType.BEST_PRACTICES,
    # 'UseArrayLiteralsInAnnotations': IssueType.BEST_PRACTICES,
    'UseCheckNotNull': IssueType.BEST_PRACTICES,
    'UseCheckOrError': IssueType.BEST_PRACTICES,
    'UseDataClass': IssueType.BEST_PRACTICES,
    'UseEmptyCounterpart': IssueType.BEST_PRACTICES,
    # 'UseIfEmptyOrIfBlank': IssueType.BEST_PRACTICES,
    'UseIfInsteadOfWhen': IssueType.BEST_PRACTICES,
    # 'UseIsNullOrEmpty': IssueType.BEST_PRACTICES,
    # 'UseOrEmpty': IssueType.BEST_PRACTICES,
    'UseRequire': IssueType.BEST_PRACTICES,
    'UseRequireNotNull': IssueType.BEST_PRACTICES,
    'UselessCallOnNotNull': IssueType.BEST_PRACTICES,
    # 'UtilityClassWithPublicConstructor': IssueType.BEST_PRACTICES,
    'VarCouldBeVal': IssueType.BEST_PRACTICES,
    'WildcardImport': IssueType.BEST_PRACTICES,
}
