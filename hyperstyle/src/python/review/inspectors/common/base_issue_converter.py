import logging
from typing import Optional

from hyperstyle.src.python.review.inspectors.issue import (
    BaseIssue,
    get_issue_class_by_issue_type,
    get_measure_name_by_measurable_issue_type,
    IssueData,
    Measurable,
)
from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfigsHandler


logger = logging.getLogger(__name__)


def convert_base_issue(base_issue: BaseIssue, issue_configs_handler: IssueConfigsHandler) -> Optional[BaseIssue]:
    """
    Convert the ``base_issue`` to a code issue or measurable one.

    If necessary, the old description is replaced by the new one and the measure is parsed using the
    ``issue_configs_handler``.

    :param base_issue: A base issue to be converted.
    :param issue_configs_handler: A handler of issue configurations.
    :return:
    """
    origin_class = base_issue.origin_class
    issue_type = base_issue.type
    description = base_issue.description
    inspector_type = base_issue.inspector_type

    issue_data = vars(base_issue)  # Get all the fields from BaseIssue, so we can change them
    issue_data[IssueData.DESCRIPTION.value] = issue_configs_handler.get_description(origin_class, description)

    issue_class = get_issue_class_by_issue_type(issue_type)
    if issubclass(issue_class, Measurable):
        measure = issue_configs_handler.parse_measure(origin_class, description)
        if measure is None:
            logger.error(f'{inspector_type.value}: Unable to parse measure.')
            return None

        issue_data[get_measure_name_by_measurable_issue_type(issue_type)] = measure

    try:
        return issue_class(**issue_data)
    except Exception as exception:
        logger.error(f'{inspector_type.value}: Unable to create a new issue. {exception}')
        return None
