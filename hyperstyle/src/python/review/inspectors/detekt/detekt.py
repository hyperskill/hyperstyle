import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.common.file_system import check_set_up_env_variable, new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.detekt.issue_types import DETEKT_CLASS_NAME_TO_ISSUE_TYPE
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.parsers.xml_parser import parse_xml_file_result

logger = logging.getLogger(__name__)

DETEKT_DIRECTORY_ENV = 'DETEKT_DIRECTORY'
check_set_up_env_variable(DETEKT_DIRECTORY_ENV)
DETEKT_VERSION_ENV = 'DETEKT_VERSION'
check_set_up_env_variable(DETEKT_VERSION_ENV)

PATH_TO_DETEKT_CLI = f'{os.environ[DETEKT_DIRECTORY_ENV]}/detekt-cli-{os.environ[DETEKT_VERSION_ENV]}/bin/detekt-cli'
PATH_DETEKT_PLUGIN = f'{os.environ[DETEKT_DIRECTORY_ENV]}/detekt-formatting-{os.environ[DETEKT_VERSION_ENV]}.jar'

PATH_TOOLS_PMD_FILES = Path(__file__).parent / 'files'
PATH_DETEKT_CONFIG = PATH_TOOLS_PMD_FILES / 'detekt-config.yml'


class DetektInspector(BaseInspector):
    inspector_type = InspectorType.DETEKT

    origin_class_to_pattern = {
        'LongMethod':
            r'The function .* is too long \((\d+)\)',
        'ComplexCondition':
            r'This condition is too complex \((\d+)\)',
        'ComplexMethod':
            r'The function .* appears to be too complex \((\d+)\)',
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path):
        command = [
            PATH_TO_DETEKT_CLI,
            '--config', PATH_DETEKT_CONFIG,
            '--plugins', PATH_DETEKT_PLUGIN,
            '--report', f'xml:{output_path}',
            '--input', str(path),
        ]
        return command

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)

            run_in_subprocess(command)
            return parse_xml_file_result(output_path,
                                         self.inspector_type,
                                         self.choose_issue_type,
                                         IssueDifficulty.get_by_issue_type,
                                         self.origin_class_to_pattern,
                                         {})

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:
        issue_type = DETEKT_CLASS_NAME_TO_ISSUE_TYPE.get(issue_class)
        if not issue_type:
            logger.info(f'{cls.inspector_type.value}: {issue_class} - unknown origin class')
            return IssueType.BEST_PRACTICES
        return issue_type
