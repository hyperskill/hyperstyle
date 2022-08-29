import logging
from pathlib import Path
from typing import Callable, List
from xml.etree import ElementTree

from hyperstyle.src.python.review.inspectors.common.base_issue_converter import convert_base_issue
from hyperstyle.src.python.review.inspectors.common.utils import is_result_file_correct
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType
from hyperstyle.src.python.review.inspectors.issue import BaseIssue, IssueDifficulty, IssueType
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler

logger = logging.getLogger(__name__)


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


def parse_xml_file_result(
    file_path: Path,
    inspector_type: InspectorType,
    issue_type_selector: Callable[[str], IssueType],
    difficulty_selector: Callable[[IssueType], IssueDifficulty],
    issue_configs_handler: IssueConfigsHandler,
) -> List[BaseIssue]:
    """
    Parse the output, which is a xml file, and returns a list of the issues found there.

    If the passed path is not a correct file, an empty list is returned.

    :param file_path: A path to a xml file.
    :param inspector_type: An inspector type.
    :param issue_type_selector: Determines the issue type of an inspection.
    :param difficulty_selector: Determines the difficulty of an inspection.
    :param issue_configs_handler: A handler of issue configurations.
    :return: A list of parsed issues.
    """

    if not is_result_file_correct(file_path, inspector_type):
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

            # Example: com.puppycrawl.tools.checkstyle.checks.sizes.LineLengthCheck -> LineLengthCheck
            origin_class = inner_element.attrib['source'].split('.')[-1]
            issue_type = issue_type_selector(origin_class)

            base_issue = BaseIssue(
                origin_class=origin_class,
                type=issue_type,
                description=inner_element.attrib['message'],
                file_path=code_file_path,
                line_no=int(inner_element.attrib['line']),
                column_no=int(inner_element.attrib.get('column', 1)),
                inspector_type=inspector_type,
                difficulty=difficulty_selector(issue_type),
            )

            issue = convert_base_issue(base_issue, issue_configs_handler)
            if issue is None:
                logger.error(f'{inspector_type.value}: an error occurred during converting base issue.')
                continue

            issues.append(issue)

    return issues
