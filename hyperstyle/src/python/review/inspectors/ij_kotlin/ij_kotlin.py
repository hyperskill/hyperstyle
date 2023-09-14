from hyperstyle.src.python.review.inspectors.common.inspector.base_inspector import BaseIJInspector
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.common.inspector.proto import model_pb2
from hyperstyle.src.python.review.inspectors.common.issue.issue import IssueType
from hyperstyle.src.python.review.inspectors.ij_kotlin.issue_configs import ISSUE_CONFIGS


class KotlinIJInspector(BaseIJInspector):
    inspector_type = InspectorType.IJ_KOTLIN
    language_id = model_pb2.LanguageId.kotlin
    issue_configs = ISSUE_CONFIGS

    @staticmethod
    def choose_issue_type(problem: model_pb2.Problem) -> IssueType:
        # TODO: add categorization
        return IssueType.BEST_PRACTICES
