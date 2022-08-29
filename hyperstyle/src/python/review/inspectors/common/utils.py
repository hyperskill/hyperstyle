import logging
from math import floor
from pathlib import Path
from string import Formatter
from typing import List

from hyperstyle.src.python.review.common.file_system import get_content_from_file
from hyperstyle.src.python.review.inspectors.inspector_type import InspectorType

logger = logging.getLogger(__name__)


def is_result_file_correct(file_path: Path, inspector_type: InspectorType) -> bool:
    """
    Check if the result of the inspectors is correct: it exists and it is not empty.
    """
    if not file_path.is_file():
        logger.error(f'{inspector_type.value}: error - no output file')
        return False

    file_content = get_content_from_file(file_path)
    if not file_content:
        logger.error(f'{inspector_type.value}: error - empty file')
        return False

    return True


def convert_percentage_of_value_to_lack_of_value(percentage_of_value: float) -> int:
    """
    Converts percentage of value to lack of value.
    Calculated by the formula: floor(100 - percentage_of_value).

    :param percentage_of_value: value in the range from 0 to 100.
    :return: lack of value.
    """
    return floor(100 - percentage_of_value)


# TODO: When upgrading to python 3.9+, replace it with removeprefix.
# See: https://docs.python.org/3.9/library/stdtypes.html#str.removeprefix
def remove_prefix(text: str, prefix: str) -> str:
    """
    Removes the prefix if it is present, otherwise returns the original string.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def _get_format_fields(input_string: str) -> List[str]:
    """
    Get all format fields from the input string.

    :param input_string: A string from which all format fields need to be extracted.
    :return: A list of format fields.
    """
    return [elem[1] for elem in Formatter().parse(input_string) if elem[1] is not None]


def contains_format_fields(input_string: str) -> bool:
    """
    Check that the input string contains format fields.

    :param input_string: A string for which you want to check whether it contains format fields or not.
    :return: Whether the input string contains format fields or not.
    """
    return len(_get_format_fields(input_string)) > 0


def contains_named_format_fields(input_string: str) -> bool:
    """
    Check that the input string contains named format fields.

    :param input_string: A string for which you want to check whether it contains named format fields or not.
    :return: Whether the input string contains named format fields or not.
    """
    return any(field != '' and not field.isdigit() for field in _get_format_fields(input_string))
