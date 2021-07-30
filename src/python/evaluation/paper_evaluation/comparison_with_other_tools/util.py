from enum import Enum, unique


@unique
class ComparisonColumnName(Enum):
    STUDENT_ID = 'student_id'
    TASK_KEY = 'task_key'
    SOLUTION = 'solution'
    TUTOR_ERROR = 'tutor_error'

    TUTOR_ISSUES = 'tutor_issues'
    HYPERSTYLE_ISSUES = 'hyperstyle_issues'
    HYPERSTYLE_INFO_ISSUES = 'hyperstyle_info_issues'
    CODE_STYLE_ISSUES_COUNT = 'code_style_issues_count'


ERROR_CONST = 'ERROR'


@unique
class TutorTask(Enum):
    EVEN = 'countEven'
    SUM_VALUES = 'sumValues'
    ODD_SUM = 'oddSum'
    SCORE = 'calculateScore'
    HAS_DOUBLED = 'hasDoubled'
    HAVE_THREE = 'haveThree'
