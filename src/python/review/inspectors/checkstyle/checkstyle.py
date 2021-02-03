import logging
from pathlib import Path
from typing import List

from src.python.review.common.file_system import new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.checkstyle.issue_types import CHECK_CLASS_NAME_TO_ISSUE_TYPE
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, IssueType
from src.python.review.inspectors.parsers.checkstyle_parser import parse_checkstyle_file_result

logger = logging.getLogger(__name__)

PATH_TOOLS_PMD_FILES = Path(__file__).parent / 'files'
PATH_TOOLS_CHECKSTYLE_JAR = PATH_TOOLS_PMD_FILES / 'checkstyle.jar'
PATH_TOOLS_CHECKSTYLE_CONFIG = PATH_TOOLS_PMD_FILES / 'config.xml'


class CheckstyleInspector(BaseInspector):
    inspector_type = InspectorType.CHECKSTYLE

    skipped_issues = [
        'EmptyLineSeparatorCheck',
    ]

    origin_class_to_pattern = {
        'CyclomaticComplexityCheck':
            r'Cyclomatic Complexity is (\d+)',

        'JavaNCSSCheck':
            r'NCSS for this method is (\d+)',

        'BooleanExpressionComplexityCheck':
            r'Boolean expression complexity is (\d+)',

        'LineLengthCheck':
            r'Line is longer than \d+ characters \(found (\d+)\)'
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path) -> List[str]:
        return [
            'java', '-jar', PATH_TOOLS_CHECKSTYLE_JAR,
            '-c', PATH_TOOLS_CHECKSTYLE_CONFIG,
            '-f', 'xml', '-o', output_path, str(path)
        ]

    def inspect(self, path: Path, config: dict) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = temp_dir / 'output.xml'
            command = self._create_command(path, output_path)
            run_in_subprocess(command)

            issues = parse_checkstyle_file_result(Path(output_path),
                                                  self.inspector_type,
                                                  self.choose_issue_type,
                                                  self.origin_class_to_pattern)
            return [
                issue for issue in issues
                if issue.origin_class not in self.skipped_issues
            ]

    @classmethod
    def choose_issue_type(cls, check_class: str) -> IssueType:
        check_class_name = check_class.split('.')[-1]
        issue_type = CHECK_CLASS_NAME_TO_ISSUE_TYPE.get(check_class_name)
        if not issue_type:
            logger.warning('Checkstyle: %s - unknown check class' % check_class_name)
            issue_type = IssueType.BEST_PRACTICES

        return issue_type
