from __future__ import annotations

from hyperstyle.src.python.review.inspectors.common.inspector.base_inspector import BaseIJInspector
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.common.inspector.proto import model_pb2
from hyperstyle.src.python.review.inspectors.ij_java.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.ij_java.issue_types import (
    IJ_INSPECTION_TO_ISSUE_TYPE,
    IJ_MESSAGE_TO_ISSUE_TYPE,
)


class JavaIJInspector(BaseIJInspector):
    inspector_type = InspectorType.IJ_JAVA
    language_id = model_pb2.LanguageId.java
    issue_configs = ISSUE_CONFIGS
    ij_inspection_to_issue_type = IJ_INSPECTION_TO_ISSUE_TYPE
    ij_message_to_issue_type = IJ_MESSAGE_TO_ISSUE_TYPE
