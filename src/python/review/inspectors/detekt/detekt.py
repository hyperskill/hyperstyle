import logging
from pathlib import Path
from typing import List

from src.python.review.common.file_system import new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.detekt.issue_types import DETECT_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.inspectors.parsers.checkstyle_parser import parse_checkstyle_file_result

logger = logging.getLogger(__name__)

PATH_TOOLS_PMD_FILES = Path(__file__).parent / 'files'
PATH_DETEKT_JAR = PATH_TOOLS_PMD_FILES / 'detekt-cli-1.8.0-all.jar'
PATH_DETEKT_CONFIG = PATH_TOOLS_PMD_FILES / 'detekt-config.yml'
PATH_DETEKT_PLUGIN = PATH_TOOLS_PMD_FILES / 'detekt-formatting-1.5.1.jar'


class DetektInspector(BaseInspector):
    inspector_type = InspectorType.DETEKT

    origin_class_to_pattern = {
        'LongMethod':
            r'The function .* is too long \((\d+)\)',
        'ComplexCondition':
            r'This condition is too complex \((\d+)\)',
        'ComplexMethod':
            r'The function .* appears to be too complex \((\d+)\)'
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path):
        return [
            'java', '-jar',
            PATH_DETEKT_JAR,
            '--config', PATH_DETEKT_CONFIG,
            '--plugins', PATH_DETEKT_PLUGIN,
            '--report', f'xml:{output_path}',
            '--input', str(path)
        ]

    def inspect(self, path: Path, config) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)

            run_in_subprocess(command)
            return parse_checkstyle_file_result(output_path,
                                                self.inspector_type,
                                                self.choose_issue_type,
                                                self.origin_class_to_pattern)

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:
        issue_type = DETECT_CLASS_NAME_TO_ISSUE_TYPE.get(issue_class)
        if not issue_type:
            logger.info(f'{cls.inspector_type.value}: {issue_class} - unknown origin class')
            return IssueType.BEST_PRACTICES
        return issue_type
