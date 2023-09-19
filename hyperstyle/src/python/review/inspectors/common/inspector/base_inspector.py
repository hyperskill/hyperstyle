import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import get_content_from_file
from hyperstyle.src.python.review.inspectors.common.inspector.ij_client import IJClient
from hyperstyle.src.python.review.inspectors.common.inspector.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.common.inspector.proto import model_pb2
from hyperstyle.src.python.review.inspectors.common.issue.base_issue_converter import convert_base_issue
from hyperstyle.src.python.review.inspectors.common.issue.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.common.issue.issue_configs import IssueConfig, IssueConfigsHandler


logger = logging.getLogger(__name__)


class BaseInspector(ABC):
    """
    Each external inspector contains a dictionary in which the IssueType corresponds to the original linter classes.
    The dictionary helps to categorize errors during parsing the linters' output.

    To add a new inspector, you need:
     - to create a class that inherits from the BaseInspector class,
     - define the type of inspector (the type filed) by adding a new option in the InspectorType,
     - implement the <inspect >function.

    Typically, the <inspect> function launches a linter and parses its output (XML or JSON) to get a list of BaseIssue.

    Also, if you need to launch inspectors in memory (without using/creating a file with code, you need to implement
    <inspect_in_memory> function.

    Some inspectors (internal) do not require creating a dictionary with IssueType.
    This is connected to the fact that they do not launch an additional analysis tool and work with the code directly,
    for example, the python AST inspector.
    """

    # Type of inspection for analyzing, e.g. pylint, detekt and etc
    @property
    @abstractmethod
    def inspector_type(self) -> InspectorType:
        raise NotImplementedError('inspector_type property not implemented yet')

    @abstractmethod
    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        raise NotImplementedError('inspect method not implemented yet')

    @abstractmethod
    def inspect_in_memory(self, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        raise NotImplementedError('inspect in memory method not implemented yet')


class BaseIJInspector(BaseInspector):
    """
    Base class for every IJ-based inspector.

    It inherits from the `BaseInspector` class, so see its documentation for more information.

    To implement this kind of inspector, you should additionally specify `language_id` from the `model.proto` file,
    specify issue configs and implement the `choose_issue_type` function.

    Before running the inspector, you should set up connection parameters
    using the `setup_connection_parameters` function.
    """
    host: str
    port: int

    @property
    @abstractmethod
    def language_id(self) -> model_pb2.LanguageId:
        raise NotImplementedError('language_id property is not implemented yet')

    @property
    @abstractmethod
    def issue_configs(self) -> List[IssueConfig]:
        raise NotImplementedError('issue_configs property is not implemented yet')

    @property
    @abstractmethod
    def ij_inspection_to_issue_type(self) -> Dict[str, IssueType]:
        raise NotImplementedError('ij_inspection_to_issue_type property is not implemented yet')

    @property
    @abstractmethod
    def ij_message_to_issue_type(self) -> Dict[str, Dict[str, IssueType]]:
        raise NotImplementedError('ij_message_to_issue_type property is not implemented yet')

    def setup_connection_parameters(self, host: str, port: int):
        self.host = host
        self.port = port

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        code = get_content_from_file(path)
        return self._get_inspection_result(code, path)

    def inspect_in_memory(self, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        return self._get_inspection_result(code, Path(""))

    def convert_to_base_issues(self, inspection_result: model_pb2.InspectionResult, file_path: Path) -> List[BaseIssue]:
        base_issues = []
        issue_configs_handler = IssueConfigsHandler(*self.issue_configs)
        for problem in inspection_result.problems:
            issue_type = self.choose_issue_type(problem)
            base_issue = BaseIssue(
                origin_class=problem.inspector,
                type=issue_type,
                description=problem.name,
                file_path=file_path,
                line_no=problem.lineNumber,
                column_no=problem.offset,
                inspector_type=InspectorType.IJ_PYTHON,
                difficulty=IssueDifficulty.get_by_issue_type(issue_type),
            )

            issue = convert_base_issue(base_issue, issue_configs_handler)
            if issue is None:
                logger.error(f'{self.inspector_type.value}: an error occurred during converting a base issue.')
                continue

            base_issues.append(base_issue)

        return base_issues

    def _get_inspection_result(self, code_text: str, file_path: Path) -> List[BaseIssue]:
        if self.host is None or self.port is None:
            raise Exception('Connection parameters is not set up.')

        try:
            client = IJClient(self.host, self.port)

            code = model_pb2.Code()
            code.languageId = self.language_id
            code.text = code_text

            inspection_result = client.inspect(code)

            return self.convert_to_base_issues(inspection_result, file_path)

        except Exception as e:
            # TODO: replace with error when add mock server into tests
            logger.info('Inspector failed to connect to code server.', e)
            return []

    def choose_issue_type(self, problem: model_pb2.Problem) -> IssueType:
        if problem.inspector in self.ij_message_to_issue_type:
            for key, value in self.ij_message_to_issue_type[problem.inspector].items():
                if problem.name in key:
                    return value

        if problem.inspector in self.ij_inspection_to_issue_type:
            return self.ij_inspection_to_issue_type[problem.inspector]

        # PEP-8 inspection
        return IssueType.CODE_STYLE
