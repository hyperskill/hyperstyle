from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Union

from src.python.review.inspectors.inspector_type import InspectorType


class IssueType(Enum):
    CODE_STYLE = 'CODE_STYLE'
    BEST_PRACTICES = 'BEST_PRACTICES'
    ERROR_PRONE = 'ERROR_PRONE'
    FUNC_LEN = 'FUNC_LEN'
    LINE_LEN = 'LINE_LEN'
    CYCLOMATIC_COMPLEXITY = 'CYCLOMATIC_COMPLEXITY'
    BOOL_EXPR_LEN = 'BOOL_EXPR_LEN'
    COMPLEXITY = 'COMPLEXITY'
    ARCHITECTURE = 'ARCHITECTURE'
    INHERITANCE_DEPTH = 'INHERITANCE_DEPTH'
    CHILDREN_NUMBER = 'CHILDREN_NUMBER'
    WEIGHTED_METHOD = 'WEIGHTED_METHOD'
    COUPLING = 'COUPLING'
    COHESION = 'COHESION'
    CLASS_RESPONSE = 'CLASS_RESPONSE'
    METHOD_NUMBER = 'METHOD_NUMBER'


# Keys in results dictionary
class IssueData(Enum):
    # Base fields
    FILE_PATH = 'file_path'
    LINE_NUMBER = 'line_no'
    COLUMN_NUMBER = 'column_no'
    ORIGIN_ClASS = 'origin_class'
    INSPECTOR_TYPE = 'inspector_type'

    # Additional fields
    ISSUE_TYPE = 'type'
    DESCRIPTION = 'description'

    LINE_LEN = 'line_len'
    FUNCTION_LEN = 'func_len'
    BOOL_EXPR_LEN = 'bool_expr_len'
    CYCLOMATIC_COMPLEXITY = 'cc_value'

    @classmethod
    def get_base_issue_data_dict(cls, file_path: Union[str, Path], inspector_type: InspectorType, line_number: int = 1,
                                 column_number: int = 1, origin_class: str = '') -> Dict[str, Any]:
        return {
            cls.FILE_PATH.value: file_path,
            cls.LINE_NUMBER.value: line_number,
            cls.COLUMN_NUMBER.value: column_number,
            cls.ORIGIN_ClASS.value: origin_class,
            cls.INSPECTOR_TYPE.value: inspector_type
        }


@dataclass(frozen=True, eq=True)
class BaseIssue:
    file_path: Path
    line_no: int
    column_no: int

    description: str
    origin_class: str

    inspector_type: InspectorType
    type: IssueType


@dataclass(frozen=True)
class CodeIssue(BaseIssue):
    pass


@dataclass(frozen=True)
class BoolExprLenIssue(BaseIssue):
    bool_expr_len: int
    type = IssueType.BOOL_EXPR_LEN


@dataclass(frozen=True)
class FuncLenIssue(BaseIssue):
    func_len: int
    type = IssueType.FUNC_LEN


@dataclass(frozen=True)
class LineLenIssue(BaseIssue):
    line_len: int
    type = IssueType.LINE_LEN


@dataclass(frozen=True)
class CyclomaticComplexityIssue(BaseIssue):
    cc_value: int
    type = IssueType.CYCLOMATIC_COMPLEXITY


@dataclass(frozen=True)
class InheritanceIssue(BaseIssue):
    inheritance_tree_depth: int
    type = IssueType.INHERITANCE_DEPTH


@dataclass(frozen=True)
class ChildrenNumberIssue(BaseIssue):
    children_number: int
    type = IssueType.CHILDREN_NUMBER


@dataclass(frozen=True)
class WeightedMethodIssue(BaseIssue):
    weighted_method: int
    type = IssueType.WEIGHTED_METHOD


@dataclass(frozen=True)
class CouplingIssue(BaseIssue):
    class_objects_coupling: int
    type = IssueType.COUPLING


@dataclass(frozen=True)
class CohesionIssue(BaseIssue):
    cohesion_lack: int
    type = IssueType.COHESION


@dataclass(frozen=True)
class ClassResponseIssue(BaseIssue):
    class_response: int
    type = IssueType.CLASS_RESPONSE


@dataclass(frozen=True)
class MethodNumberIssue(BaseIssue):
    method_number: int
    type = IssueType.METHOD_NUMBER
