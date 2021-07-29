import csv
import logging
import os
from pathlib import Path
from typing import Dict, List

from src.python.review.application_config import LanguageVersion
from src.python.review.common.file_system import new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, CodeIssue, IssueType
from src.python.review.inspectors.pmd.issue_types import RULE_TO_ISSUE_TYPE

logger = logging.getLogger(__name__)

PATH_TOOLS_PMD_FILES = Path(__file__).parent / 'files'
PATH_TOOLS_PMD_SHELL_SCRIPT = PATH_TOOLS_PMD_FILES / 'bin' / 'run.sh'
PATH_TOOLS_PMD_RULES_SET = PATH_TOOLS_PMD_FILES / 'bin' / 'basic.xml'


class PMDInspector(BaseInspector):
    inspector_type = InspectorType.PMD

    def __init__(self):
        os.chmod(PATH_TOOLS_PMD_SHELL_SCRIPT, 0o777)

    @classmethod
    def _create_command(cls, path: Path,
                        output_path: Path,
                        java_version: LanguageVersion,
                        n_cpu: int) -> List[str]:
        return [
            PATH_TOOLS_PMD_SHELL_SCRIPT,
            'pmd', '-d', str(path), '-no-cache',
            '-R', PATH_TOOLS_PMD_RULES_SET,
            '-language', 'java',
            '-version', java_version.value,
            '-f', 'csv', '-r', str(output_path),
            '-t', str(n_cpu)
        ]

    def inspect(self, path: Path, config: Dict) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            output_path = Path(temp_dir / 'out.csv')

            language_version = config.get('language_version')
            if language_version is None:
                language_version = LanguageVersion.JAVA_11

            command = self._create_command(path, output_path, language_version, config['n_cpu'])
            run_in_subprocess(command)
            return self.parse_output(output_path)

    def parse_output(self, output_path: Path) -> List[BaseIssue]:
        if not output_path.is_file():
            logger.error('%s: error - no output file' % self.inspector_type.value)
            return []

        with open(str(output_path)) as out_file:
            reader = csv.DictReader(out_file)
            return [
                CodeIssue(
                    file_path=Path(row['File']),
                    line_no=int(row['Line']),
                    column_no=1,
                    type=self.choose_issue_type(row['Rule']),
                    origin_class=row['Rule set'],
                    description=row['Description'],
                    inspector_type=self.inspector_type,
                ) for row in reader]

    @classmethod
    def choose_issue_type(cls, rule: str) -> IssueType:
        issue_type = RULE_TO_ISSUE_TYPE.get(rule)
        if not issue_type:
            logger.warning('%s: %s - unknown rule' %
                           (cls.inspector_type.value, rule))
            return IssueType.BEST_PRACTICES

        return issue_type
