import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree

from src.python.review.common.file_system import get_all_file_system_items, new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.intellij.issue_types import ISSUE_CLASS_TO_ISSUE_TYPE
from src.python.review.inspectors.issue import BaseIssue, CodeIssue, IssueDifficulty, IssueType

logger = logging.getLogger(__name__)

INTELLIJ_INSPECTOR_EXECUTABLE = os.environ.get('INTELLIJ_INSPECTOR_EXECUTABLE')
INTELLIJ_INSPECTOR_PROJECT = Path(__file__).parent / 'project'
INTELLIJ_INSPECTOR_SETTINGS = (INTELLIJ_INSPECTOR_PROJECT / '.idea' / 'inspectionProfiles' / 'custom_profiles.xml')

PYTHON_FOLDER = 'python_sources'
JAVA_FOLDER = 'java_sources/src'
KOTLIN_FOLDER = 'kotlin_sources/src'

PYTHON_SOURCES = INTELLIJ_INSPECTOR_PROJECT / PYTHON_FOLDER
JAVA_SOURCES = INTELLIJ_INSPECTOR_PROJECT / JAVA_FOLDER
KOTLIN_SOURCES = INTELLIJ_INSPECTOR_PROJECT / KOTLIN_FOLDER

SUPPORTED_EXTENSIONS = ('.java', '.py', '.kt', '.kts')


class IntelliJInspector(BaseInspector):
    inspector_type = InspectorType.INTELLIJ

    skipped_issues = [
        'Unresolved references',
    ]

    def __init__(self):
        if not JAVA_SOURCES.exists():
            JAVA_SOURCES.mkdir(parents=True)
        if not PYTHON_SOURCES.exists():
            PYTHON_SOURCES.mkdir(parents=True)
        if not KOTLIN_SOURCES.exists():
            KOTLIN_SOURCES.mkdir(parents=True)

    @staticmethod
    def create_command(output_dir_path) -> List[Union[str, Path]]:
        return [
            INTELLIJ_INSPECTOR_EXECUTABLE, INTELLIJ_INSPECTOR_PROJECT,
            INTELLIJ_INSPECTOR_SETTINGS, output_dir_path, '-v2',
        ]

    def inspect(self, path: Path, config: Dict[str, Any]) -> List[BaseIssue]:

        path_in_project_to_origin_path = self.copy_files_to_project(path)
        try:
            with new_temp_dir() as temp_dir:
                command = self.create_command(temp_dir)
                run_in_subprocess(command)
                issues = self.parse(temp_dir, path_in_project_to_origin_path)
        finally:
            for file_path_in_project in path_in_project_to_origin_path:
                file_path_in_project.unlink()

        return issues

    def copy_files_to_project(self, path: Path) -> Dict[Path, Path]:
        if path.is_file():
            root_path = path.parent
            file_paths = [path]
        elif path.is_dir():
            root_path = path
            file_paths = get_all_file_system_items(root_path)
        else:
            raise ValueError

        path_in_project_to_origin_path = {}
        for file_path in file_paths:
            if not self.check_supported_extension(file_path):
                continue

            relative_file_path = file_path.relative_to(root_path)
            file_path_in_project = self._get_file_path_in_project(relative_file_path)

            text = file_path.read_text()
            file_path_in_project.write_text(text)

            path_in_project_to_origin_path[file_path_in_project] = file_path

        return path_in_project_to_origin_path

    @staticmethod
    def check_supported_extension(file_path: Path) -> bool:
        return file_path.suffix.endswith(SUPPORTED_EXTENSIONS)

    @classmethod
    def _get_file_path_in_project(cls, relative_file_path: Path) -> Path:

        if relative_file_path.suffix.endswith('.java'):
            return JAVA_SOURCES / relative_file_path

        elif relative_file_path.suffix.endswith(('.kt', '.kts')):
            return KOTLIN_SOURCES / relative_file_path

        elif relative_file_path.suffix.endswith('.py'):
            return PYTHON_SOURCES / relative_file_path

        else:
            raise ValueError

    @classmethod
    def parse(cls, out_dir_path: Path,
              path_in_project_to_origin_path: Dict[Path, Path]) -> List[BaseIssue]:
        out_file_paths = [
            file_path for file_path in get_all_file_system_items(out_dir_path)
            if file_path.suffix.endswith('.xml') and not file_path.name.startswith('.')
        ]

        issues: List[BaseIssue] = []
        for file_path in out_file_paths:
            tree = ElementTree.parse(file_path)
            root = tree.getroot()
            for child in root:
                file_path: Optional[Path] = None
                line_no: Optional[int] = None
                issue_class: Optional[str] = None
                description: Optional[str] = None

                for element in child:
                    tag = element.tag
                    text = element.text
                    if tag == 'file':
                        file_path = Path(
                            text.replace(
                                'file://$PROJECT_DIR$',
                                str(INTELLIJ_INSPECTOR_PROJECT),
                            ),
                        )
                    elif tag == 'line':
                        line_no = int(text)
                    elif tag == 'problem_class':
                        issue_class = text
                    elif tag == 'description':
                        description = (re.compile(r'<[^<]+>')
                                       .sub('', text)
                                       .replace('#loc', ''))

                if not file_path or not line_no or not issue_class or not description:
                    continue
                else:
                    issue_type = cls.choose_issue_type(issue_class)
                    file_path = path_in_project_to_origin_path[file_path]

                    if issue_type and issue_class not in cls.skipped_issues:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_no=line_no,
                            column_no=1,
                            description=description,
                            origin_class=issue_class,
                            inspector_type=cls.inspector_type,
                            type=issue_type,
                            difficulty=IssueDifficulty.get_by_issue_type(issue_type),
                        ))

        return issues

    @classmethod
    def choose_issue_type(cls, issue_class: str) -> IssueType:

        issue_type = ISSUE_CLASS_TO_ISSUE_TYPE.get(issue_class)
        if not issue_type:
            logger.warning('%s: %s - unknown error code' %
                           (cls.inspector_type.value, issue_class))
            issue_type = None

        return issue_type
