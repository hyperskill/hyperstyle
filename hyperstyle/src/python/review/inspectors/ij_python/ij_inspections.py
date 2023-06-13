import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import get_content_from_file
from hyperstyle.src.python.review.common.language import Language
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
import hyperstyle.src.python.review.inspectors.ij_python.proto.model_pb2 as model_pb2
from hyperstyle.src.python.review.inspectors.ij_python.ij_client import IJClient
from hyperstyle.src.python.review.inspectors.ij_python.issue_types import IJ_PYTHON_CODE_TO_ISSUE_TYPE, \
    ISSUE_TYPE_EXCEPTIONS
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType

CODE_SERVER_HOST = "CODE_SERVER_HOST"
CODE_SERVER_PORT = "CODE_SERVER_PORT"

logger = logging.getLogger(__name__)


class IJInspector(BaseInspector):
    inspector_type = InspectorType.IJ_PYTHON

    def __init__(self, language: Language):
        self.host = os.environ.get(CODE_SERVER_HOST, "localhost")
        self.port = os.environ.get(CODE_SERVER_PORT, 8080)
        if language != language.PYTHON:
            raise Exception(f"IJ inspector does not support {language} language now. Only python is supported now.")
        self.languageId = model_pb2.LanguageId.Python

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        code = get_content_from_file(path)
        return self._get_inspection_result(code, path)

    def inspect_in_memory(self, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        return self._get_inspection_result(code, Path(""))

    @staticmethod
    def choose_issue_type(inspector: str, description: str) -> IssueType:
        if inspector in ISSUE_TYPE_EXCEPTIONS:
            for key, value in ISSUE_TYPE_EXCEPTIONS[inspector].items():
                if description in key:
                    return value

        if inspector in IJ_PYTHON_CODE_TO_ISSUE_TYPE:
            return IJ_PYTHON_CODE_TO_ISSUE_TYPE[inspector]

        # PEP-8 inspection
        return IssueType.CODE_STYLE

    def convert_to_base_issues(self, inspection_result: model_pb2.InspectionResult, file_path: Path) -> List[BaseIssue]:
        base_issues = []
        for problem in inspection_result.problems:
            issue_type = self.choose_issue_type(problem.inspector, problem.name)
            base_issues.append(
                BaseIssue(
                    origin_class=problem.inspector,
                    type=issue_type,
                    description=problem.name,
                    file_path=file_path,
                    line_no=problem.lineNumber,
                    column_no=problem.offset,
                    inspector_type=InspectorType.IJ_PYTHON,
                    difficulty=IssueDifficulty.get_by_issue_type(issue_type),
                ),
            )

        return base_issues

    def _get_inspection_result(self, code_text: str, file_path: Path) -> List[BaseIssue]:

        try:
            client = IJClient(self.host, self.port)

            code = model_pb2.Code()
            code.languageId = model_pb2.LanguageId.Python
            code.text = code_text

            inspection_result = client.inspect(code)

            return self.convert_to_base_issues(inspection_result, file_path)

        except Exception as e:
            # TODO: replace with error when add mock server into tests
            logger.info('Inspector failed to connect to code server.', e)
            return []
