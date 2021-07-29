import logging
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List

from src.python.review.common.file_system import get_all_file_system_items
from src.python.review.common.java_compiler import javac, javac_project
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, CodeIssue, IssueType

logger = logging.getLogger(__name__)

PATH_SPOTBUGS_FILES = Path(__file__).parent / 'files'
PATH_SPOTBUGS_EXECUTABLE = PATH_SPOTBUGS_FILES / 'bin' / 'spotbugs'
PATH_SPOTBUGS_EXCLUDE = PATH_SPOTBUGS_FILES / 'spotbugs-exclude.xml'


class SpotbugsInspector(BaseInspector):
    inspector_type = InspectorType.SPOTBUGS

    @classmethod
    def _create_command(cls, path: Path) -> List[str]:
        return [
            PATH_SPOTBUGS_EXECUTABLE,
            '-quiet',  # disable warning and messages
            '-exclude',
            PATH_SPOTBUGS_EXCLUDE,
            '-textui',
            '-medium',
            str(path)
        ]

    def inspect(self, path: Path, config: Dict) -> List[BaseIssue]:
        if path.is_file():
            is_successful = javac(path)
        else:
            is_successful = javac_project(path)

        if not is_successful:
            logger.error('%s: cant compile java files')

        return self._inspect_compiled(path)

    def _inspect_compiled(self, path: Path) -> List[BaseIssue]:
        if path.is_dir():
            command = self._create_command(path)
        else:
            command = self._create_command(path.parent)
        output = run_in_subprocess(command)

        if path.is_file():
            file_paths = [path]
        else:
            file_paths = get_all_file_system_items(path)

        java_file_paths = [file_path for file_path in file_paths if file_path.suffix == '.java']
        file_path_counter = Counter(java_file_paths)
        file_name_to_path = {file_path.name: file_path for file_path in java_file_paths}
        return self._parse(output, file_path_counter, file_name_to_path)

    @classmethod
    def _parse(cls, output: str, file_path_counter: Dict[Path, int],
               file_name_to_path: Dict[str, Path]) -> List[BaseIssue]:
        lines = [line for line in output.split('\n') if line]
        issues: List[BaseIssue] = []
        for line in lines:
            try:
                issue = cls._parse_single_line(line, file_name_to_path)
                file_path = issue.file_path
                if file_path_counter[file_path] == 1:
                    issues.append(issue)
                else:
                    logger.warning(f'Cannot inspect duplicate file: {file_path}')
            except Exception as e:
                logger.warning(f'Cannot parse output line {line}', e)
        return issues

    @classmethod
    def _parse_single_line(cls, line: str, file_name_to_path: Dict[str, Path]) -> BaseIssue:
        file_name = re.compile(r'(At|In|at|in) ([^ ]+.java)').findall(line)[-1][1].strip()

        desc_start_index = line.find(':')
        desc_end_index = max(line.rfind(':'), line.rfind('.java'))

        issue_class = line[:desc_start_index].strip()
        long_desc = line[desc_start_index + 1: desc_end_index].strip()
        short_desc = long_desc.split('  ')[0]

        line_number_str = line[desc_end_index + 1:].strip()
        line_number_parsed = re.compile(r'\d+').findall(line_number_str)
        line_number = int(line_number_parsed[0]) if line_number_parsed else 0

        return CodeIssue(
            file_path=file_name_to_path[file_name],
            line_no=line_number,
            column_no=1,
            type=IssueType.ERROR_PRONE,
            origin_class=issue_class,
            description=short_desc,
            inspector_type=cls.inspector_type
        )
