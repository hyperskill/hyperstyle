from math import floor


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
