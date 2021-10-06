import logging
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from xml.etree import ElementTree

from hyperstyle.src.python.review.common.file_system import get_content_from_file
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    BoolExprLenIssue,
    CodeIssue,
    CyclomaticComplexityIssue,
    FuncLenIssue,
    IssueData,
    IssueDifficulty,
    IssueType,
    LineLenIssue,
)
from hyperstyle.src.python.review.inspectors.tips import (
    get_bool_expr_len_tip,
    get_cyclomatic_complexity_tip,
    get_func_len_tip,
    get_line_len_tip,
)

logger = logging.getLogger(__name__)


def __is_result_file_correct(file_path: Path, inspector_type: InspectorType) -> bool:
    """
    Check if the result of the inspectors is correct: it exists and it is not empty.
    """
    if not file_path.is_file():
        logger.error('%s: error - no output file' % inspector_type.value)
        return False

    file_content = get_content_from_file(file_path)
    if not file_content:
        logger.error('%s: error - empty file' % inspector_type.value)
        return False

    return True


def __parse_error_message(element: ElementTree) -> str:
    """
    Extracts the error message from the tree element and
    removes the substring '(max allowed is \\d+)' from it, if possible.
    """

    message = element.attrib['message']
    return re.sub(r'\(max allowed is \d+\). ', '', message)


# Measurable means that the issue has integer measure,
# e.g. BoolExprLenIssue, CyclomaticComplexityIssue and so on
def __parse_measurable_issue(issue_data: Dict[str, Any], issue_type: IssueType,
                             measure_value: int) -> Optional[BaseIssue]:
    """
    Depending on the issue_type creates a corresponding measurable issue.
    """

    if issue_type == IssueType.CYCLOMATIC_COMPLEXITY:
        issue_data[IssueData.CYCLOMATIC_COMPLEXITY.value] = measure_value
        issue_data[IssueData.DESCRIPTION.value] = get_cyclomatic_complexity_tip()
        return CyclomaticComplexityIssue(**issue_data)
    elif issue_type == IssueType.FUNC_LEN:
        issue_data[IssueData.FUNCTION_LEN.value] = measure_value
        issue_data[IssueData.DESCRIPTION.value] = get_func_len_tip()
        return FuncLenIssue(**issue_data)
    elif issue_type == IssueType.BOOL_EXPR_LEN:
        issue_data[IssueData.BOOL_EXPR_LEN.value] = measure_value
        issue_data[IssueData.DESCRIPTION.value] = get_bool_expr_len_tip()
        return BoolExprLenIssue(**issue_data)
    elif issue_type == IssueType.LINE_LEN:
        issue_data[IssueData.LINE_LEN.value] = measure_value
        issue_data[IssueData.DESCRIPTION.value] = get_line_len_tip()
        return LineLenIssue(**issue_data)
    return None


def __should_handle_element(element: ElementTree) -> bool:
    """
    Checks if a tree element is a file.
    """

    return element.tag == 'file'


def __is_error(element: ElementTree) -> bool:
    """
    Checks if a tree element is an error.
    """

    return element.tag == 'error'


# TODO: Needs refactoring
def parse_xml_file_result(
        file_path: Path,
        inspector_type: InspectorType,
        issue_type_selector: Callable[[str], IssueType],
        difficulty_selector: Callable[[IssueType], IssueDifficulty],
        origin_class_to_pattern: Dict[str, str],
        origin_class_to_description: Dict[str, str]) -> List[BaseIssue]:
    """
    Parses the output, which is a xml file, and returns a list of the issues found there.
    issue_type_selector determines the IssueType of an inspection.
    origin_class_to_description allows to parse measurable errors.

    If the passed path is not a correct file, an empty list is returned.
    """

    if not __is_result_file_correct(file_path, inspector_type):
        return []

    # Parse result XML
    tree = ElementTree.parse(file_path)
    issues: List[BaseIssue] = []

    for element in tree.getroot():
        if not __should_handle_element(element):
            continue

        code_file_path = Path(element.attrib['name'])
        for inner_element in element:
            if not __is_error(inner_element):
                continue

            message = __parse_error_message(inner_element)
            # Example: com.puppycrawl.tools.checkstyle.checks.sizes.LineLengthCheck -> LineLengthCheck
            origin_class = inner_element.attrib['source'].split('.')[-1]
            issue_data = IssueData.get_base_issue_data_dict(code_file_path, inspector_type,
                                                            line_number=int(inner_element.attrib['line']),
                                                            column_number=int(
                                                                inner_element.attrib.get('column', 1)),
                                                            origin_class=origin_class)

            issue_type = issue_type_selector(origin_class)
            issue_data[IssueData.ISSUE_TYPE.value] = issue_type
            issue_data[IssueData.DIFFICULTY.value] = difficulty_selector(issue_type)

            if origin_class in origin_class_to_pattern:
                pattern = origin_class_to_pattern.get(origin_class)
                measure_value = int(re.search(pattern, message,
                                              flags=re.IGNORECASE).groups()[0])

                issue = __parse_measurable_issue(issue_data, issue_type, measure_value)
            else:
                issue_data[IssueData.DESCRIPTION.value] = origin_class_to_description.get(origin_class, message)
                issue = CodeIssue(**issue_data)

            if issue is not None:
                issues.append(issue)

    return issues
