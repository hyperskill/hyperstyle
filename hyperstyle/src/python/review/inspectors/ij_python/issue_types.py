from typing import Dict

from hyperstyle.src.python.review.inspectors.issue import IssueType

# Synchronized with https://github.com/JetBrains-Research/code-quality-ij-server/tree/master/docs/inspections/python
IJ_PYTHON_CODE_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    # BEST_PRACTICES
    'PyUnusedLocalInspection': IssueType.BEST_PRACTICES,
    'PySimplifyBooleanCheckInspection': IssueType.BEST_PRACTICES,
    'PyArgumentEqualDefaultInspection': IssueType.BEST_PRACTICES,
    'PyAttributeOutsideInitInspection': IssueType.BEST_PRACTICES,
    'PyBroadExceptionInspection': IssueType.BEST_PRACTICES,
    'PyDictCreationInspection': IssueType.BEST_PRACTICES,
    'PyFromFutureImportInspection': IssueType.BEST_PRACTICES,
    'PyReturnFromInitInspection': IssueType.BEST_PRACTICES,
    'PyListCreationInspection': IssueType.BEST_PRACTICES,
    'PySetFunctionToLiteralInspection': IssueType.BEST_PRACTICES,
    'PyProtectedMemberInspection': IssueType.BEST_PRACTICES,
    'PyMethodMayBeStaticInspection': IssueType.BEST_PRACTICES,
    'PyChainedComparisonsInspection': IssueType.BEST_PRACTICES,

    # CODE_STYLE
    'PyRedundantParenthesesInspection': IssueType.CODE_STYLE,
    'PyAugmentAssignmentInspection': IssueType.CODE_STYLE,
    'PyMethodParametersInspection': IssueType.CODE_STYLE,
    'PyUnreachableCodeInspection': IssueType.CODE_STYLE,
    'PyTrailingSemicolonInspection': IssueType.CODE_STYLE,
    'PyStatementEffectInspection': IssueType.CODE_STYLE,
    'PyPep8NamingInspection': IssueType.CODE_STYLE,
    'PyPep8Inspection': IssueType.CODE_STYLE,

    # ERROR_PRONE
    'PyDataclassInspection': IssueType.ERROR_PRONE,
    'PyDefaultArgumentInspection': IssueType.ERROR_PRONE,
    'PyAssignmentToLoopOrWithParameterInspection': IssueType.ERROR_PRONE,
    'PyAsyncCallInspection': IssueType.ERROR_PRONE,
    'PyByteLiteralInspection': IssueType.ERROR_PRONE,
    'PyCallingNonCallableInspection': IssueType.ERROR_PRONE,
    'PyComparisonWithNoneInspection': IssueType.ERROR_PRONE,
    'PyDictDuplicateKeysInspection': IssueType.ERROR_PRONE,
    'PyExceptClausesOrderInspection': IssueType.ERROR_PRONE,
    'PyFinalInspection': IssueType.ERROR_PRONE, # TODO: add exceptions to the model
    'PyGlobalUndefinedInspection': IssueType.ERROR_PRONE,
    'PyArgumentListInspection': IssueType.ERROR_PRONE,
    'PyMethodFirstArgAssignmentInspection': IssueType.ERROR_PRONE,
    'PyStringFormatInspection': IssueType.ERROR_PRONE,
    'PyMethodOverridingInspection': IssueType.ERROR_PRONE,
    'PyTupleAssignmentBalanceInspection': IssueType.ERROR_PRONE,
    'PyExceptionInheritInspection': IssueType.ERROR_PRONE,
    'PyUnboundLocalVariableInspection': IssueType.ERROR_PRONE,
    'PySuperArgumentsInspection': IssueType.ERROR_PRONE,
    'PyTupleItemAssignmentInspection': IssueType.ERROR_PRONE,
    'PyPropertyAccessInspection': IssueType.ERROR_PRONE,
    'PyNestedDecoratorsInspection': IssueType.ERROR_PRONE,
    'PyMissingConstructorInspection': IssueType.ERROR_PRONE,
    'PyDecoratorInspection': IssueType.ERROR_PRONE,
    'PyTypeCheckerInspection': IssueType.ERROR_PRONE,
    'PyNoneFunctionAssignmentInspection': IssueType.ERROR_PRONE,
    'PyShadowingNamesInspection': IssueType.ERROR_PRONE,
    'PyAbstractClassInspection': IssueType.ERROR_PRONE,
    'PyOverloadsInspection': IssueType.ERROR_PRONE,
    'PyTypeHintsInspection': IssueType.ERROR_PRONE,
    'PyTypedDictInspection': IssueType.ERROR_PRONE,
    'PyShadowingBuiltinsInspection': IssueType.ERROR_PRONE,
    'PyUnresolvedReferencesInspection': IssueType.ERROR_PRONE,
}

ISSUE_TYPE_EXCEPTIONS = {
    'PyDataclassInspection': {
        'is useless until ''__post_init__'' is declared': IssueType.BEST_PRACTICES,
        'should take all init-only variables (incl. inherited) in the same order as they are defined': IssueType.BEST_PRACTICES,
        'would not be called until \'init\' parameter is set to True \'__attrs_post_init__\' should not take any parameters except \'self\'': IssueType.BEST_PRACTICES,
    },
    'PyFinalInspection': {
        'No need to mark method in \'Final\' class as \'@final\'': IssueType.BEST_PRACTICES,
    }
}
