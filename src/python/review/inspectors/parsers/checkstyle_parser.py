import logging
import re
from pathlib import Path
from typing import Callable, Dict, List
from xml.etree import ElementTree

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.issue import BaseIssue, BoolExprLenIssue, CodeIssue, CyclomaticComplexityIssue, \
    FuncLenIssue, IssueType, LineLenIssue
from src.python.review.inspectors.tips import get_bool_expr_len_tip, get_cyclomatic_complexity_tip, get_func_len_tip, \
    get_line_len_tip

logger = logging.getLogger(__name__)


# TODO Needs testing
def parse_checkstyle_file_result(
        file_path: Path,
        inspector_type: InspectorType,
        choose_issue_type: Callable[[str], IssueType],
        origin_class_to_pattern_dict: Dict[str, str]) -> List[BaseIssue]:
    if not file_path.is_file():
        logger.error('%s: error - no output file' % inspector_type.value)
        return []

    file_content = file_path.read_text()

    if not file_content:
        logger.error('%s: error - empty file' % inspector_type.value)
        return []

    tree = ElementTree.parse(file_path)

    issues: List[BaseIssue] = []
    for element in tree.getroot():
        if element.tag == 'file':
            code_file_path = Path(element.attrib['name'])
            for inner_element in element:
                if inner_element.tag == 'error':
                    message = inner_element.attrib['message']
                    origin_class = inner_element.attrib['source'].split('.')[-1]
                    message = re.sub(r'\(max allowed is \d+\). ', '', message)
                    issue_type = choose_issue_type(origin_class)
                    line_no = int(inner_element.attrib['line'])

                    issue_data = {
                        'file_path': code_file_path,
                        'line_no': line_no,
                        'column_no': int(inner_element.attrib.get('column', 1)),
                        'origin_class': origin_class,
                        'inspector_type': inspector_type,
                        'type': issue_type
                    }

                    if origin_class not in origin_class_to_pattern_dict:
                        issue_data['description'] = message
                        issues.append(CodeIssue(**issue_data))
                    else:
                        pattern = origin_class_to_pattern_dict.get(origin_class)
                        metric_value = int(re.search(pattern, message,
                                                     flags=re.IGNORECASE).groups()[0])

                        if issue_type == IssueType.CYCLOMATIC_COMPLEXITY:
                            issue_data['cc_value'] = metric_value
                            issue_data['description'] = get_cyclomatic_complexity_tip()
                            issues.append(CyclomaticComplexityIssue(**issue_data))
                        elif issue_type == IssueType.FUNC_LEN:
                            issue_data['func_len'] = metric_value
                            issue_data['description'] = get_func_len_tip()
                            issues.append(FuncLenIssue(**issue_data))
                        elif issue_type == IssueType.BOOL_EXPR_LEN:
                            issue_data['bool_expr_len'] = metric_value
                            issue_data['description'] = get_bool_expr_len_tip()
                            issues.append(BoolExprLenIssue(**issue_data))
                        elif issue_type == IssueType.LINE_LEN:
                            issue_data['line_len'] = metric_value
                            issue_data['description'] = get_line_len_tip()
                            issues.append(LineLenIssue(**issue_data))

    return issues
