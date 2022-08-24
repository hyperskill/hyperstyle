import logging
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Pattern, Tuple, Union

from hyperstyle.src.python.review.inspectors.common import is_fstring

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IssueDescriptionParser:
    """
    Parser for an issue description.

    The ``converter`` can be:

    - A function --
      In this case, all groups obtained from the description using the ``regexp`` will be converted using this function.

    - A dictionary --
      In this case, the corresponding converter will be applied to the named group obtained by the ``regexp``.
      All groups in the ``regexp`` must be named, otherwise unnamed groups will be skipped.
      For those groups for which no converter is defined, the default converter will be used.

    By default, the converter is equal to the ``str`` function.
    """

    regexp: Pattern[str]
    converter: Union[Callable, Dict[str, Callable]] = str

    def parse(self, description: str) -> Optional[Tuple]:
        """
        Parse the description into a tuple of converted regex groups.

        :return: A tuple of converted regex groups. If there is an error during parsing, None will be returned.
        """

        match = self.regexp.search(description)
        if match is None or not match.groups():
            logger.error(f'Unable to parse ("{self.regexp.pattern}") the description: {description}')
            return None

        try:
            if isinstance(self.converter, dict):
                args = tuple(self.converter.get(name, str)(group) for name, group in match.groupdict().items())
            else:
                args = tuple(self.converter(group) for group in match.groups())
        except Exception as exception:
            logger.error(f'Unable to convert the groups: {exception}')
            return None

        return args


@dataclass(frozen=True)
class IssueConfig:
    """
    Custom config for a code issue.

    Required fields:

    - ``origin_class`` -- An origin class of issue.
    - ``new_description`` -- A new description for the issue. Can be a format string, but in this case the ``parser``
      must be specified.

    Optional fields:

    - ``parser`` -- A description parser.

    If you just want to replace the issue description with a static one, specify only the ``new_description``.
    Otherwise, the ``new_description`` must be a format string, the ``parser`` must be specified and
    the number of groups in the regex must match the number of fields in the ``new_description``.
    """

    origin_class: str
    new_description: str

    parser: Optional[IssueDescriptionParser] = None

    def __post_init__(self):
        if self.parser is None and is_fstring(self.new_description):
            raise TypeError('You need to specify a parser, since you are using a format string.')

        if self.parser is not None and not is_fstring(self.new_description):
            raise TypeError('You specified the parser, but the new description is not a format string.')


@dataclass(frozen=True)
class MeasurableIssueConfig(IssueConfig):
    """
    Custom config for a measurable issue.

    Required fields:

    - ``origin_class`` -- An origin class of issue.
    - ``new_description`` -- A new description for the issue. Can be a format string.
    - ``parser`` -- A description parser. Should parse the measure.

    Optional fields:

    - ``measure_position`` -- The index by which to find the measure in a regular expression pattern. This field will be
      useful if the parser parses not only the measure, but also other data. The default value is 0.

    If you want to replace the issue description with a dynamic one, the ``new_description`` must be a format string
    and the number of groups in the regex must match the number of fields in the ``new_description``.
    """

    measure_position: int = 0

    def __post_init__(self):
        if self.parser is None:
            raise TypeError('You must specify a parser.')


class IssueConfigsHandler:
    """
    A class that handles error configs.

    It accepts error configs, turns them into dictionaries and handles requests for measures and descriptions.
    """

    origin_class_to_config: Dict[str, IssueConfig]

    def __init__(self, *issue_configs: IssueConfig):
        self.origin_class_to_config = {issue_config.origin_class: issue_config for issue_config in issue_configs}

    def _parse_description(self, origin_class: str, description: str) -> Optional[Tuple]:
        """
        Parse a description.

        :param origin_class: An origin class of issue.
        :param description: A description that needs to be parsed.
        :return: A tuple of groups that were parsed from the description with the issue parser. If there is an error
        during parsing, None will be returned.
        """
        config = self.origin_class_to_config.get(origin_class)
        parser = config.parser if config is not None else None

        if parser is None:
            logger.error(f'{origin_class}: The parser is undefined.')
            return None

        args = parser.parse(description)
        if args is None:
            logger.error(f'{origin_class}: Unable to parse description.')
            return None

        return args

    def parse_measure(self, origin_class: str, description: str) -> Optional:
        """
        Parse a measure from a description.

        :param origin_class: An origin class of issue.
        :param description: A description from which a measure must be parsed.
        :return: A measure that was parsed from the description with the issue parser. If there is an error during
        parsing, None will be returned.
        """
        args = self._parse_description(origin_class, description)
        if args is None:
            return None

        config = self.origin_class_to_config.get(origin_class)
        measure_position = config.measure_position if isinstance(config, MeasurableIssueConfig) else None

        if measure_position is None:
            logger.error(f'{origin_class}: The position of measure is undefined.')
            return None

        if measure_position >= len(args):
            logger.error(f'{origin_class}: The position of measure is out of range.')
            return None

        return args[measure_position]

    def get_description(self, origin_class: str, description: str) -> str:
        """
        Get an issue description.

        If a new description is defined for an issue, it will be returned. If necessary, the passed
        description will be parsed and all extracted elements will be formatted into a new description.

        If no new description is defined for an issue, or an error occurs during parsing or formatting,
        the original description will be returned.

        :param origin_class: An origin class of issue.
        :param description: An issue description.
        :return: An issue description.
        """
        config = self.origin_class_to_config.get(origin_class)
        new_description = config.new_description if config is not None else None

        if new_description is None:
            return description

        if not is_fstring(new_description):
            return new_description

        args = self._parse_description(origin_class, description)
        if args is None:
            return description

        try:
            return new_description.format(*args)
        except Exception as exception:
            logger.error(f'{origin_class}: Unable to format the new description: {exception}')
            return description
