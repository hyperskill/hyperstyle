import abc
import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, List, Union

from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType

logger = logging.getLogger(__name__)


@unique
class IssueType(Enum):
    # Code style issues
    CODE_STYLE = 'CODE_STYLE'
    LINE_LEN = 'LINE_LEN'

    # Best practice issues
    BEST_PRACTICES = 'BEST_PRACTICES'
    FUNC_LEN = 'FUNC_LEN'
    BOOL_EXPR_LEN = 'BOOL_EXPR_LEN'
    CLASS_RESPONSE = 'CLASS_RESPONSE'
    METHOD_NUMBER = 'METHOD_NUMBER'

    # Error-prone issues
    ERROR_PRONE = 'ERROR_PRONE'

    # Code complexity issues
    COMPLEXITY = 'COMPLEXITY'
    CYCLOMATIC_COMPLEXITY = 'CYCLOMATIC_COMPLEXITY'
    INHERITANCE_DEPTH = 'INHERITANCE_DEPTH'
    CHILDREN_NUMBER = 'CHILDREN_NUMBER'
    WEIGHTED_METHOD = 'WEIGHTED_METHOD'
    COUPLING = 'COUPLING'
    COHESION = 'COHESION'
    MAINTAINABILITY = 'MAINTAINABILITY'

    # Info issues
    INFO = 'INFO'

    # Others
    UNDEFINED = 'UNDEFINED'
    ARCHITECTURE = 'ARCHITECTURE'  # TODO: Distribute into one of the main types

    def __str__(self) -> str:
        return ' '.join(self.value.lower().split('_'))

    def to_main_type(self) -> 'IssueType':
        """
        Converts the issue type to main issue type.
        Main issue types: CODE_STYLE, BEST_PRACTICES, ERROR_PRONE, COMPLEXITY, INFO.
        """
        return get_main_category_by_issue_type(self)


ISSUE_TYPE_TO_MAIN_CATEGORY = {
    # CODE_STYLE
    IssueType.CODE_STYLE: IssueType.CODE_STYLE,
    IssueType.LINE_LEN: IssueType.CODE_STYLE,

    # BEST_PRACTICES
    IssueType.BEST_PRACTICES: IssueType.BEST_PRACTICES,
    IssueType.FUNC_LEN: IssueType.BEST_PRACTICES,
    IssueType.BOOL_EXPR_LEN: IssueType.BEST_PRACTICES,
    IssueType.METHOD_NUMBER: IssueType.BEST_PRACTICES,
    IssueType.CLASS_RESPONSE: IssueType.BEST_PRACTICES,

    # ERROR_PRONE
    IssueType.ERROR_PRONE: IssueType.ERROR_PRONE,

    # COMPLEXITY
    IssueType.COMPLEXITY: IssueType.COMPLEXITY,
    IssueType.CYCLOMATIC_COMPLEXITY: IssueType.COMPLEXITY,
    IssueType.WEIGHTED_METHOD: IssueType.COMPLEXITY,
    IssueType.COUPLING: IssueType.COMPLEXITY,
    IssueType.COHESION: IssueType.COMPLEXITY,
    IssueType.MAINTAINABILITY: IssueType.COMPLEXITY,
    IssueType.CHILDREN_NUMBER: IssueType.COMPLEXITY,
    IssueType.INHERITANCE_DEPTH: IssueType.COMPLEXITY,
    IssueType.ARCHITECTURE: IssueType.COMPLEXITY,

    # INFO
    IssueType.INFO: IssueType.INFO,
}


def get_main_category_by_issue_type(issue_type: IssueType) -> IssueType:
    return ISSUE_TYPE_TO_MAIN_CATEGORY.get(issue_type, IssueType.UNDEFINED)


def main_category_to_issue_type_list_dict() -> Dict[IssueType, List[IssueType]]:
    main_category_to_issue_type = defaultdict(list)
    for key, value in ISSUE_TYPE_TO_MAIN_CATEGORY.items():
        main_category_to_issue_type[value].append(key)
    return main_category_to_issue_type


MAIN_CATEGORY_TO_ISSUE_TYPE_LIST = main_category_to_issue_type_list_dict()

IssuesStat = Dict[IssueType, int]


def get_default_issue_stat() -> IssuesStat:
    stat = {issue: 0 for issue in set(ISSUE_TYPE_TO_MAIN_CATEGORY.values())}
    stat[IssueType.UNDEFINED] = 0
    return stat


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
    DIFFICULTY = 'difficulty'

    LINE_LEN = 'line_len'
    FUNCTION_LEN = 'func_len'
    BOOL_EXPR_LEN = 'bool_expr_len'
    CYCLOMATIC_COMPLEXITY = 'cc_value'
    COHESION_LACK = 'cohesion_lack'
    MAINTAINABILITY_LACK = 'maintainability_lack'

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
            cls.INSPECTOR_TYPE.value: inspector_type,
        }


@unique
class IssueDifficulty(Enum):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'

    @classmethod
    def get_by_issue_type(cls, issue_type: IssueType) -> 'IssueDifficulty':
        issue_type_to_difficulty = {
            # Easy
            IssueType.CODE_STYLE: cls.EASY,
            IssueType.LINE_LEN: cls.EASY,
            IssueType.FUNC_LEN: cls.EASY,
            IssueType.BOOL_EXPR_LEN: cls.EASY,
            IssueType.INFO: cls.EASY,  # Because INFO should always be shown on the platforms

            # Medium
            IssueType.BEST_PRACTICES: cls.MEDIUM,

            # Hard
            IssueType.CLASS_RESPONSE: cls.HARD,
            IssueType.METHOD_NUMBER: cls.HARD,
            IssueType.ERROR_PRONE: cls.HARD,
            IssueType.COMPLEXITY: cls.HARD,
            IssueType.CYCLOMATIC_COMPLEXITY: cls.HARD,
            IssueType.INHERITANCE_DEPTH: cls.HARD,
            IssueType.CHILDREN_NUMBER: cls.HARD,
            IssueType.WEIGHTED_METHOD: cls.HARD,
            IssueType.COUPLING: cls.HARD,
            IssueType.COHESION: cls.HARD,
            IssueType.MAINTAINABILITY: cls.HARD,
            IssueType.UNDEFINED: cls.HARD,
            IssueType.ARCHITECTURE: cls.HARD,
        }

        if issue_type not in issue_type_to_difficulty:
            logger.warning(f'IssueDifficulty: {issue_type} - unknown issue type.')
            return cls.HARD

        return issue_type_to_difficulty[issue_type]


@dataclass(frozen=True, eq=True)
class ShortIssue:
    origin_class: str

    type: IssueType


@dataclass(frozen=True, eq=True)
class BaseIssue(ShortIssue):
    description: str

    file_path: Path
    line_no: int
    column_no: int

    inspector_type: InspectorType
    difficulty: IssueDifficulty


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


@dataclass(frozen=True)
class MaintainabilityLackIssue(BaseIssue, Measurable):
    maintainability_lack: int
    type = IssueType.MAINTAINABILITY

    def measure(self) -> int:
        return self.maintainability_lack


ISSUE_TYPE_TO_CLASS = {
    IssueType.CODE_STYLE: CodeIssue,
    IssueType.BEST_PRACTICES: CodeIssue,
    IssueType.ERROR_PRONE: CodeIssue,
    IssueType.COMPLEXITY: CodeIssue,
    IssueType.INFO: CodeIssue,

    IssueType.LINE_LEN: LineLenIssue,
    IssueType.FUNC_LEN: FuncLenIssue,
    IssueType.BOOL_EXPR_LEN: BoolExprLenIssue,
    IssueType.CYCLOMATIC_COMPLEXITY: CyclomaticComplexityIssue,
    IssueType.MAINTAINABILITY: MaintainabilityLackIssue,
    IssueType.COHESION: CohesionIssue,
}


def get_issue_class_by_issue_type(issue_type: IssueType):
    return ISSUE_TYPE_TO_CLASS.get(issue_type, CodeIssue)


MEASURABLE_ISSUE_TYPE_TO_MEASURE_NAME = {
    IssueType.LINE_LEN: IssueData.LINE_LEN.value,
    IssueType.FUNC_LEN: IssueData.FUNCTION_LEN.value,
    IssueType.BOOL_EXPR_LEN: IssueData.BOOL_EXPR_LEN.value,
    IssueType.CYCLOMATIC_COMPLEXITY: IssueData.CYCLOMATIC_COMPLEXITY.value,
    IssueType.MAINTAINABILITY: IssueData.MAINTAINABILITY_LACK.value,
    IssueType.COHESION: IssueData.COHESION_LACK.value,
}
