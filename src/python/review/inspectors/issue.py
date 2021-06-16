import abc
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, Union

from src.python.review.inspectors.inspector_type import InspectorType


@unique
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
    INFO = 'INFO'


# Keys in results dictionary
@unique
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
    def get_base_issue_data_dict(cls,
                                 file_path: Union[str, Path],
                                 inspector_type: InspectorType,
                                 line_number: int = 1,
                                 column_number: int = 1,
                                 origin_class: str = '') -> Dict[str, Any]:
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


class Measurable(abc.ABC):
    @abc.abstractmethod
    def measure(self) -> int:
        pass


@dataclass(frozen=True)
class CodeIssue(BaseIssue):
    pass


@dataclass(frozen=True)
class BoolExprLenIssue(BaseIssue, Measurable):
    bool_expr_len: int
    type = IssueType.BOOL_EXPR_LEN

    def measure(self) -> int:
        return self.bool_expr_len


@dataclass(frozen=True)
class FuncLenIssue(BaseIssue, Measurable):
    func_len: int
    type = IssueType.FUNC_LEN

    def measure(self) -> int:
        return self.func_len


@dataclass(frozen=True)
class LineLenIssue(BaseIssue, Measurable):
    line_len: int
    type = IssueType.LINE_LEN

    def measure(self) -> int:
        return self.line_len


@dataclass(frozen=True)
class CyclomaticComplexityIssue(BaseIssue, Measurable):
    cc_value: int
    type = IssueType.CYCLOMATIC_COMPLEXITY

    def measure(self) -> int:
        return self.cc_value


@dataclass(frozen=True)
class InheritanceIssue(BaseIssue, Measurable):
    inheritance_tree_depth: int
    type = IssueType.INHERITANCE_DEPTH

    def measure(self) -> int:
        return self.inheritance_tree_depth


@dataclass(frozen=True)
class ChildrenNumberIssue(BaseIssue, Measurable):
    children_number: int
    type = IssueType.CHILDREN_NUMBER

    def measure(self) -> int:
        return self.children_number


@dataclass(frozen=True)
class WeightedMethodIssue(BaseIssue, Measurable):
    weighted_method: int
    type = IssueType.WEIGHTED_METHOD

    def measure(self) -> int:
        return self.weighted_method


@dataclass(frozen=True)
class CouplingIssue(BaseIssue, Measurable):
    class_objects_coupling: int
    type = IssueType.COUPLING

    def measure(self) -> int:
        return self.class_objects_coupling


@dataclass(frozen=True)
class CohesionIssue(BaseIssue, Measurable):
    cohesion_lack: int
    type = IssueType.COHESION

    def measure(self) -> int:
        return self.cohesion_lack


@dataclass(frozen=True)
class ClassResponseIssue(BaseIssue, Measurable):
    class_response: int
    type = IssueType.CLASS_RESPONSE

    def measure(self) -> int:
        return self.class_response


@dataclass(frozen=True)
class MethodNumberIssue(BaseIssue, Measurable):
    method_number: int
    type = IssueType.METHOD_NUMBER

    def measure(self) -> int:
        return self.method_number
