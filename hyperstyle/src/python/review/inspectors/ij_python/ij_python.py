from hyperstyle.src.python.review.inspectors.common.inspector.base_inspector import BaseIJInspector
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.common.inspector.proto import model_pb2
from hyperstyle.src.python.review.inspectors.common.issue.issue import IssueType
from hyperstyle.src.python.review.inspectors.ij_python.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.ij_python.issue_types import (
    IJ_PYTHON_CODE_TO_ISSUE_TYPE,
    ISSUE_TYPE_EXCEPTIONS,
)


class PythonIJInspector(BaseIJInspector):
    inspector_type = InspectorType.IJ_PYTHON
    language_id = model_pb2.LanguageId.Python
    issue_configs = ISSUE_CONFIGS

    @staticmethod
    def choose_issue_type(problem: model_pb2.Problem) -> IssueType:
        if problem.inspector in ISSUE_TYPE_EXCEPTIONS:
            for key, value in ISSUE_TYPE_EXCEPTIONS[problem.inspector].items():
                if problem.name in key:
                    return value

        if problem.inspector in IJ_PYTHON_CODE_TO_ISSUE_TYPE:
            return IJ_PYTHON_CODE_TO_ISSUE_TYPE[problem.inspector]

        # PEP-8 inspection
        return IssueType.CODE_STYLE
