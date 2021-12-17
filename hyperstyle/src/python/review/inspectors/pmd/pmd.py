import csv
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

from hyperstyle.src.python.review.application_config import LanguageVersion
from hyperstyle.src.python.review.common.file_system import check_set_up_env_variable, new_temp_dir
from hyperstyle.src.python.review.common.subprocess_runner import run_in_subprocess
from hyperstyle.src.python.review.inspectors.base_inspector import BaseInspector
from hyperstyle.src.python.review.inspectors.common import remove_prefix
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, CodeIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.pmd.issue_types import PMD_RULE_TO_ISSUE_TYPE

logger = logging.getLogger(__name__)

PMD_DIRECTORY_ENV = 'PMD_DIRECTORY'
PMD_VERSION_ENV = 'PMD_VERSION'

PATH_TOOLS_PMD_FILES = Path(__file__).parent / 'files'
PATH_TOOLS_PMD_RULES_SET = PATH_TOOLS_PMD_FILES / 'config.xml'
DEFAULT_JAVA_VERSION = LanguageVersion.JAVA_11


class PMDInspector(BaseInspector):
    inspector_type = InspectorType.PMD
    has_access = False

    def _create_command(self, path: Path,
                        output_path: Path,
                        language_version: LanguageVersion,
                        n_cpu: int) -> List[str]:
        path_tools_pmd_shell = f'{os.environ[PMD_DIRECTORY_ENV]}/pmd-bin-{os.environ[PMD_VERSION_ENV]}/bin/run.sh'
        if not self.has_access:
            os.chmod(path_tools_pmd_shell, 0o777)
            self.has_access = True
        return [
            path_tools_pmd_shell,
            'pmd', '-d', str(path), '-no-cache',
            '-R', PATH_TOOLS_PMD_RULES_SET,
            '-language', 'java',
            '-version', self._get_java_version(language_version),
            '-f', 'csv', '-r', str(output_path),
            '-t', str(n_cpu),
        ]

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:
        if not (check_set_up_env_variable(PMD_DIRECTORY_ENV) and check_set_up_env_variable(PMD_VERSION_ENV)):
            return []

        with new_temp_dir() as temp_dir:
            output_path = Path(temp_dir / 'out.csv')

            language_version = config.get('language_version')
            if language_version is None:
                logger.info(
                    f"The version of Java is not passed. The version to be used is: {DEFAULT_JAVA_VERSION.value}.",
                )
                language_version = DEFAULT_JAVA_VERSION

            command = self._create_command(path, output_path, language_version, config['n_cpu'])
            run_in_subprocess(command)
            return self.parse_output(output_path)

    def parse_output(self, output_path: Path) -> List[BaseIssue]:
        """
        Parses the PMD output, which is a csv file, and returns a list of the issues found there.

        If the passed path is not a file, an empty list is returned.
        """
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
                    origin_class=row['Rule'],
                    description=row['Description'],
                    inspector_type=self.inspector_type,
                    difficulty=IssueDifficulty.get_by_issue_type(self.choose_issue_type(row['Rule'])),
                ) for row in reader]

    @classmethod
    def choose_issue_type(cls, rule: str) -> IssueType:
        """
        Defines IssueType by PMD rule name using config.
        """
        issue_type = PMD_RULE_TO_ISSUE_TYPE.get(rule)
        if not issue_type:
            logger.warning('%s: %s - unknown rule' %
                           (cls.inspector_type.value, rule))
            return IssueType.BEST_PRACTICES

        return issue_type

    @staticmethod
    def _get_java_version(language_version: LanguageVersion) -> str:
        """
        Converts language_version to the version of Java that PMD can work with.

        For example, java11 will be converted to 11.
        """
        java_version = language_version.value

        if not language_version.is_java():
            logger.warning(
                f"The version passed is not the Java version. The version to be used is: {DEFAULT_JAVA_VERSION.value}.",
            )
            java_version = DEFAULT_JAVA_VERSION.value

        return remove_prefix(java_version, "java")
