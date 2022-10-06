import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import check_set_up_env_variable, new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.checkstyle.issue_configs import ISSUE_CONFIGS
from hyperstyle.src.python.review.inspectors.checkstyle.issue_types import CHECK_CLASS_NAME_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.common.xml_parser import parse_xml_file_result
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

logger = logging.getLogger(__name__)

CHECKSTYLE_DIRECTORY_ENV = 'CHECKSTYLE_DIRECTORY'
CHECKSTYLE_VERSION_ENV = 'CHECKSTYLE_VERSION'

PATH_TOOLS_CHECKSTYLE_FILES = Path(__file__).parent / 'files'
PATH_TOOLS_CHECKSTYLE_CONFIG = PATH_TOOLS_CHECKSTYLE_FILES / 'config.xml'


class CheckstyleInspector(BaseInspector):
    inspector_type = InspectorType.CHECKSTYLE

    # We don't support in-memory inspection for Checkstyle yet
    @classmethod
    def inspect_in_memory(cls, code: str, config: Dict[str, Any]) -> List[BaseIssue]:
        return []

    @classmethod
    def _create_command(cls, path: Path, output_path: Path) -> List[str]:
        path_checkstyle_jar = f'{os.environ[CHECKSTYLE_DIRECTORY_ENV]}/' \
                              f'checkstyle-{os.environ[CHECKSTYLE_VERSION_ENV]}-all.jar'
        return [
            'java', '-jar', path_checkstyle_jar,
            '-c', PATH_TOOLS_CHECKSTYLE_CONFIG,
            '-f', 'xml', '-o', output_path, str(path),
        ]

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        if not (check_set_up_env_variable(CHECKSTYLE_DIRECTORY_ENV) and check_set_up_env_variable(
                CHECKSTYLE_VERSION_ENV)):
            return []

        issue_configs_handler = IssueConfigsHandler(*ISSUE_CONFIGS)
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)
            run_in_subprocess(command)

            return parse_xml_file_result(
                Path(output_path),
                self.inspector_type,
                self.choose_issue_type,
                IssueDifficulty.get_by_issue_type,
                issue_configs_handler,
            )

    @classmethod
    def choose_issue_type(cls, check_class: str) -> IssueType:
        """
        Defines IssueType by Checkstyle check class using config.
        """

        # Example: com.puppycrawl.tools.checkstyle.checks.sizes.LineLengthCheck -> LineLengthCheck
        check_class_name = check_class.split('.')[-1]
        issue_type = CHECK_CLASS_NAME_TO_ISSUE_TYPE.get(check_class_name)
        if not issue_type:
            logger.warning('Checkstyle: %s - unknown check class' % check_class_name)
            return IssueType.BEST_PRACTICES

        return issue_type
