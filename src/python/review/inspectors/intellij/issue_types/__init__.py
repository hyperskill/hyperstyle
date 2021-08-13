from typing import Dict

from src.python.review.inspectors.intellij.issue_types.java import (
    ISSUE_CLASS_TO_ISSUE_TYPE as JAVA_ISSUE_CLASS_TO_ISSUE_TYPE,
)
from src.python.review.inspectors.intellij.issue_types.kotlin import (
    ISSUE_CLASS_TO_ISSUE_TYPE as KOTLIN_ISSUE_CLASS_TO_ISSUE_TYPE,
)
from src.python.review.inspectors.intellij.issue_types.python import (
    ISSUE_CLASS_TO_ISSUE_TYPE as PYTHON_ISSUE_CLASS_TO_ISSUE_TYPE,
)
from src.python.review.inspectors.issue import IssueType

ISSUE_CLASS_TO_ISSUE_TYPE: Dict[str, IssueType] = {
    **JAVA_ISSUE_CLASS_TO_ISSUE_TYPE,
    **PYTHON_ISSUE_CLASS_TO_ISSUE_TYPE,
    **KOTLIN_ISSUE_CLASS_TO_ISSUE_TYPE,
}
