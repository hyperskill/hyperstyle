import json
import logging
import re
from pathlib import Path
from shutil import copy
from typing import AnyStr, List, Optional, Dict, Any

from src.python.review.common.file_system import new_temp_dir
from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.base_inspector import BaseInspector
from src.python.review.inspectors.inspector_type import InspectorType

from src.python.review.inspectors.issue import (
    BaseIssue,
    ChildrenNumberIssue,
    ClassResponseIssue,
    CodeIssue,
    CohesionIssue,
    CouplingIssue,
    InheritanceIssue,
    IssueType,
    MethodNumberIssue,
    WeightedMethodIssue,
    IssueData,
)

from src.python.review.inspectors.tips import (
    get_child_number_tip,
    get_class_coupling_tip,
    get_class_response_tip,
    get_cohesion_tip,
    get_inheritance_depth_tip,
    get_method_number_tip,
    get_weighted_method_tip,
)

PATH_TOOLS_SPRINGLINT_FILES = Path(__file__).parent / 'files'
PATH_SPRINGLINT_JAR = PATH_TOOLS_SPRINGLINT_FILES / 'springlint-0.6.jar'
SPRINGLINT_OUTPUT_NAME = 'springlint-result.html'

logger = logging.getLogger(__name__)


class SpringlintInspector(BaseInspector):
    inspector_type = InspectorType.SPRINGLINT

    metric_name_to_property = {
        'dit': 'inheritance_tree_depth',
        'noc': 'children_number',
        'wmc': 'weighted_method',
        'cbo': 'class_objects_coupling',
        'lcom': 'cohesion_lack',
        'rfc': 'class_response',
        'nom': 'method_number',
    }

    metric_name_to_description = {
        'dit': get_inheritance_depth_tip(),
        'noc': get_child_number_tip(),
        'wmc': get_weighted_method_tip(),
        'cbo': get_class_coupling_tip(),
        'lcom': get_cohesion_tip(),
        'rfc': get_class_response_tip(),
        'nom': get_method_number_tip(),
    }

    metric_name_to_issue_type = {
        'dit': IssueType.INHERITANCE_DEPTH,
        'noc': IssueType.CHILDREN_NUMBER,
        'wmc': IssueType.WEIGHTED_METHOD,
        'cbo': IssueType.COUPLING,
        'lcom': IssueType.COHESION,
        'rfc': IssueType.CLASS_RESPONSE,
        'nom': IssueType.METHOD_NUMBER,
    }

    @classmethod
    def _create_command(cls, path: Path, output_path: Path) -> List[str]:
        return [
            'java', '-jar',
            PATH_SPRINGLINT_JAR,
            '--output', str(output_path),
            '-otype', 'html',
            '--project', str(path),
        ]

    def inspect(self, path: Path, config: dict) -> List[BaseIssue]:
        with new_temp_dir() as temp_dir:
            if path.is_file():
                return self._inspect_file(path, temp_dir)
            else:
                return self._inspect_project(path, temp_dir)

    @classmethod
    def _inspect_project(cls, path: Path, temp_dir: Path) -> List[BaseIssue]:
        output_path = temp_dir / SPRINGLINT_OUTPUT_NAME
        command = cls._create_command(path, temp_dir)
        run_in_subprocess(command)
        return cls._parse(output_path)

    @classmethod
    def _inspect_file(cls, path: Path, temp_dir: Path) -> List[BaseIssue]:
        output_path = temp_dir / SPRINGLINT_OUTPUT_NAME
        copy(str(path), str(temp_dir))
        command = cls._create_command(temp_dir, temp_dir)
        run_in_subprocess(command)
        return cls._parse(output_path, str(path))

    @classmethod
    def _parse(cls, output_path: Path, origin_path: str = '') -> List[BaseIssue]:
        if not output_path.is_file():
            logger.error('%s: error - no output file' % cls.inspector_type.value)
            return []

        with open(str(output_path)) as out_file:
            file_content = out_file.read()
            issues: List[BaseIssue] = cls._parse_smells(file_content, origin_path)
            issues.extend(cls._parse_metrics(file_content, origin_path))
            return issues

    @classmethod
    def _parse_smells(cls, file_content: AnyStr, origin_path: str = '') -> List[BaseIssue]:
        smells_re = re.compile(r'var smells=([^;]*);', re.S)
        smells_string = smells_re.findall(file_content)[0]
        smells = json.JSONDecoder().decode(smells_string)

        issues: List[BaseIssue] = []
        for file_smell in smells:
            if origin_path:
                file_path = origin_path
            else:
                file_path = file_smell['file']
            issues.extend([CodeIssue(
                file_path=Path(file_path),
                line_no=1,
                column_no=1,
                origin_class=smell['name'],
                inspector_type=cls.inspector_type,
                type=IssueType.ARCHITECTURE,
                description=smell['description'],
            ) for smell in file_smell['smells']])

        return issues

    @classmethod
    def _parse_metrics(cls, file_content: AnyStr, origin_path: str = '') -> List[BaseIssue]:
        metrics_re = re.compile(r'var classes =([^;]*);', re.S)
        metrics_string = metrics_re.findall(file_content)[0]
        type_metrics_list = json.loads(metrics_string).items()

        issues: List[BaseIssue] = []
        for metrics_list in type_metrics_list:
            for metrics in metrics_list[1]:
                for metric_name in metrics:
                    if metric_name not in cls.metric_name_to_property:
                        continue
                    if origin_path:
                        file_path = origin_path
                    else:
                        file_path = metrics['file']
                    issues.append(cls._create_issue(metric_name,
                                                    metrics[metric_name],
                                                    Path(file_path)))
        return issues

    @classmethod
    def _create_issue(cls, metric_name: str,
                      metric_value: int, path: Path) -> Optional[BaseIssue]:
        property_name = cls.metric_name_to_property[metric_name]
        issue_data = cls._get_common_issue_data(path)
        issue_data[property_name] = metric_value
        issue_data['description'] = cls.metric_name_to_description[metric_name]
        issue_data['type'] = cls.metric_name_to_issue_type[metric_name]

        if metric_name == 'dit':
            return InheritanceIssue(**issue_data)
        if metric_name == 'noc':
            return ChildrenNumberIssue(**issue_data)
        if metric_name == 'wmc':
            return WeightedMethodIssue(**issue_data)
        if metric_name == 'cbo':
            return CouplingIssue(**issue_data)
        if metric_name == 'lcom':
            return CohesionIssue(**issue_data)
        if metric_name == 'rfc':
            return ClassResponseIssue(**issue_data)
        if metric_name == 'nom':
            return MethodNumberIssue(**issue_data)

        return None

    @classmethod
    def _get_common_issue_data(cls, file: Path) -> Dict[str, Any]:
        return IssueData.get_base_issue_data_dict(file, cls.inspector_type)
