from typing import Dict

from src.python.review import IssueType
from .java import ISSUE_CLASS_TO_ISSUE_TYPE as \
    JAVA_ISSUE_CLASS_TO_ISSUE_TYPE
from .kotlin import ISSUE_CLASS_TO_ISSUE_TYPE as \
    KOTLIN_ISSUE_CLASS_TO_ISSUE_TYPE
from .python import ISSUE_CLASS_TO_ISSUE_TYPE as \
    PYTHON_ISSUE_CLASS_TO_ISSUE_TYPE

ISSUE_CLASS_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    **JAVA_ISSUE_CLASS_TO_ISSUE_TYPE,
    **PYTHON_ISSUE_CLASS_TO_ISSUE_TYPE,
    **KOTLIN_ISSUE_CLASS_TO_ISSUE_TYPE
}
