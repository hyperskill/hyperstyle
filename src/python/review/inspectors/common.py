from math import floor


def convert_percentage_of_value_to_lack_of_value(percentage_of_value: float) -> int:
    """
    Converts percentage of value to lack of value.
    Calculated by the formula: floor(100 - percentage_of_value).

    :param percentage_of_value: value in the range from 0 to 100.
    :return: lack of maintainability.
    """
    return floor(100 - percentage_of_value)
