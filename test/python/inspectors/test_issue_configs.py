import re
from typing import Callable, Dict, List, Optional, Pattern, Tuple, Type, Union

import pytest
from hyperstyle.src.python.review.inspectors.issue_configs import (
    IssueConfig,
    IssueConfigsHandler,
    IssueDescriptionParser,
    MeasurableIssueConfig,
)

MATCH_STRING = re.compile('string')
MATCH_ONE_GROUP = re.compile(r'(.*)')
MATCH_ONE_NAMED_GROUP = re.compile(r'(?P<group>.*)')
MATCH_TWO_GROUPS = re.compile(r'\((.*)\) {(.*)}')
MATCH_TWO_NAMED_GROUPS = re.compile(r'\((?P<parentheses_group>.*)\) {(?P<curly_group>.*)}')
MATCH_NAMED_AND_UNNAMED_GROUPS = re.compile(
    r'\|(.*)\| \((?P<parentheses_group>.*)\) \|(.*)\| {(?P<curly_group>.*)} \|(.*)\|',
)

PARSE_TEST_DATA = [
    (MATCH_STRING, None, '12345', None),
    (MATCH_STRING, None, 'string', None),
    (MATCH_ONE_GROUP, None, '12345', ('12345',)),
    (MATCH_ONE_GROUP, {}, '12345', ('12345',)),
    (MATCH_ONE_GROUP, {0: int}, '12345', (12345,)),
    (MATCH_ONE_GROUP, {0: float}, 'abcdef', None),
    (MATCH_ONE_GROUP, {42: int}, '123456', ('123456',)),
    (MATCH_TWO_GROUPS, None, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_GROUPS, {}, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_GROUPS, {1: float}, '(12345) {12345.6789}', ('12345', 12345.6789)),
    (MATCH_TWO_GROUPS, {0: int, 1: float}, '(12345) {12345.6789}', (12345, 12345.6789)),
    (MATCH_TWO_GROUPS, {0: float, 1: float}, '(12345.6789) {abcdef}', None),
    (MATCH_TWO_GROUPS, {42: int}, '(123) {456}', ('123', '456')),
    (MATCH_ONE_NAMED_GROUP, None, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, {}, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, {0: int}, '12345', (12345,)),
    (MATCH_ONE_NAMED_GROUP, {0: float}, 'abcdef', None),
    (MATCH_ONE_NAMED_GROUP, {42: int}, '12345', ('12345',)),
    (MATCH_TWO_NAMED_GROUPS, None, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_NAMED_GROUPS, {}, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_NAMED_GROUPS, {1: float}, '(12345) {12345.6789}', ('12345', 12345.6789)),
    (MATCH_TWO_NAMED_GROUPS, {0: int, 1: float}, '(12345) {12345.6789}', (12345, 12345.6789)),
    (MATCH_TWO_NAMED_GROUPS, {0: float, 1: float}, '(12345.6789) {abcdef}', None),
    (MATCH_TWO_NAMED_GROUPS, {42: int}, '(123) {456}', ('123', '456')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, None, '|1| (23) |4| {56} |7|', ('1', '23', '4', '56', '7')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {}, '|1| (23) |4| {56} |7|', ('1', '23', '4', '56', '7')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {1: int}, '|1| (23) |4| {56} |7|', ('1', 23, '4', '56', '7')),
    (
        MATCH_NAMED_AND_UNNAMED_GROUPS,
        {0: int, 1: float, 2: int, 3: float, 4: int},
        '|1| (3.4) |56| {7.8} |9|',
        (1, 3.4, 56, 7.8, 9),
    ),
    (
        MATCH_NAMED_AND_UNNAMED_GROUPS,
        {0: int, 1: float, 2: int, 3: float, 4: int},
        '|1| (abcdef) |56| {7.8} |9|',
        None,
    ),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {42: int}, '|1| (23) |4| {56} |7|', ('1', '23', '4', '56', '7')),
]


@pytest.mark.parametrize(('regexp', 'converter', 'description', 'expected_groups'), PARSE_TEST_DATA)
def test_parse(
    regexp: Pattern,
    converter: Optional[Union[Callable, Dict[str, Callable]]],
    description: str,
    expected_groups: Tuple,
):
    parser = IssueDescriptionParser(regexp) if converter is None else IssueDescriptionParser(regexp, converter)
    assert parser.parse(description) == expected_groups


ISSUE_CONFIG_INIT_TEST_DATA = [
    (
        IssueConfig,
        ['IC', 'This is a format string! {0}'],
        TypeError,
        'You need to specify a parser, since you are using a format string.',
    ),
    (
        IssueConfig,
        ['IC', 'This is a simple string!', IssueDescriptionParser(re.compile(''))],
        TypeError,
        'You specified the parser, but the new description is not a format string.',
    ),
    (
        IssueConfig,
        ['IC', 'This is a format string with a named format field: {name}!', IssueDescriptionParser(re.compile(''))],
        TypeError,
        'The new description contains named format fields.',
    ),
    (MeasurableIssueConfig, ['MIC', 'This is a simple string!'], TypeError, 'You must specify a parser.'),
    (
        MeasurableIssueConfig,
        ['MIC', 'This is a format string with a named format field: {name}!', IssueDescriptionParser(re.compile(''))],
        TypeError,
        'The new description contains named format fields.',
    ),
]


@pytest.mark.parametrize(('cls', 'args', 'expected_exception', 'expected_error_message'), ISSUE_CONFIG_INIT_TEST_DATA)
def test_init_raises_exception(
    cls: Type[IssueConfig],
    args: List,
    expected_exception: Type[Exception],
    expected_error_message: str,
):
    with pytest.raises(expected_exception) as excinfo:
        cls(*args)

    assert str(excinfo.value) == expected_error_message


CONFIGS = [
    IssueConfig(
        origin_class='IC-static',
        new_description="This is a new static description.",
    ),
    IssueConfig(
        origin_class='IC-dynamic',
        new_description="This is a new dynamic description: {0}.",
        parser=IssueDescriptionParser(re.compile(r'Name: (.+)')),
    ),
    MeasurableIssueConfig(
        origin_class='MIC-static',
        new_description='This is a new static description.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter={0: int},
        ),
    ),
    MeasurableIssueConfig(
        origin_class='MIC-dynamic',
        new_description="This is a new dynamic description with a metric: {0}.",
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter={0: int},
        ),
    ),
]

PARSE_DESCRIPTION_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is a description.', None),
    (CONFIGS, 'IC-dynamic', 'This is a description.', None),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', ('abcdef',)),
    (CONFIGS, 'MIC-static', 'This is a description.', None),
    (CONFIGS, 'MIC-static', 'Metric: 42', (42,)),
    (CONFIGS, 'MIC-dynamic', 'This is a description.', None),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', (42,)),
    (CONFIGS, 'unknown_issue', 'This is a description.', None),
]


@pytest.mark.parametrize(
    ('issue_configs', 'origin_class', 'description', 'expected_tuple'),
    PARSE_DESCRIPTION_TEST_DATA,
)
def test_parse_description(
    issue_configs: List[IssueConfig],
    origin_class: str,
    description: str,
    expected_tuple: Optional[Tuple],
):
    assert IssueConfigsHandler(*issue_configs)._parse_description(origin_class, description) == expected_tuple


CONFIGS_WITH_NON_DEFAULT_MEASURE_POSITION = [
    MeasurableIssueConfig(
        origin_class='MIC-good-position',
        new_description='This is a new description.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Name: (.+), Metric: (\d+)"),
            converter={1: int},
        ),
        measure_position=1,
    ),
    MeasurableIssueConfig(
        origin_class='MIC-bad-position',
        new_description='This is a new description.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter={0: int},
        ),
        measure_position=42,
    ),
]


PARSE_MEASURE_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is a description.', None),
    (CONFIGS, 'IC-dynamic', 'This is a description.', None),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', None),
    (CONFIGS, 'MIC-static', 'This is a description.', None),
    (CONFIGS, 'MIC-static', 'Metric: 42', 42),
    (CONFIGS, 'MIC-dynamic', 'This is a description.', None),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', 42),
    (CONFIGS, 'unknown_issue', 'This is a description.', None),
    (CONFIGS_WITH_NON_DEFAULT_MEASURE_POSITION, 'MIC-good-position', 'Name: Aboba, Metric: 42', 42),
    (CONFIGS_WITH_NON_DEFAULT_MEASURE_POSITION, 'MIC-good-position', 'This is a description.', None),
    (CONFIGS_WITH_NON_DEFAULT_MEASURE_POSITION, 'MIC-bad-position', 'Metric: 42', None),
    (CONFIGS_WITH_NON_DEFAULT_MEASURE_POSITION, 'MIC-bad-position', 'This is a description.', None),
]


@pytest.mark.parametrize(
    ('issue_configs', 'origin_class', 'description', 'expected_measure'),
    PARSE_MEASURE_TEST_DATA,
)
def test_parse_measure(
    issue_configs: List[IssueConfig],
    origin_class: str,
    description: str,
    expected_measure: Optional,
):
    assert IssueConfigsHandler(*issue_configs).parse_measure(origin_class, description) == expected_measure


CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING = [
    IssueConfig(
        origin_class='IC-empty-regexp',
        new_description='There is only one field: {0}.',
        parser=IssueDescriptionParser(re.compile(r'This is a description')),
    ),
    IssueConfig(
        origin_class='IC-format-less-than-regexp',
        new_description='There is only one field: {0}.',
        parser=IssueDescriptionParser(re.compile(r'Name: (.+), Age: (\d+)')),
    ),
    IssueConfig(
        origin_class='IC-format-greater-than-regexp',
        new_description='There are two fields: {0}, {1}.',
        parser=IssueDescriptionParser(re.compile(r'Name: (.+)')),
    ),
]


CONFIGS_WITH_ESCAPED_CHARACTERS = [
    IssueConfig(
        origin_class='IC-one-escaped-curly-bracket-static',
        new_description='This is an escaped symbol: {{',
    ),
    IssueConfig(
        origin_class='IC-paired-escaped-curly-bracket-static',
        new_description='This is a paired escaped curly bracket: {{}}',
    ),
    IssueConfig(
        origin_class='IC-one-escaped-curly-bracket-dynamic',
        new_description='This is an escaped symbol {{ and this is a format field {0}',
        parser=IssueDescriptionParser(re.compile(r'Name: (.+)')),
    ),
    IssueConfig(
        origin_class='IC-paired-escaped-curly-bracket-dynamic',
        new_description='This is an escaped symbol {{}} and this is a format field {0}',
        parser=IssueDescriptionParser(re.compile(r'Name: (.+)')),
    ),
]


GET_DESCRIPTION_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is a description.', 'This is a new static description.'),
    (CONFIGS, 'IC-dynamic', 'This is a description.', 'This is a description.'),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', 'This is a new dynamic description: abcdef.'),
    (CONFIGS, 'MIC-static', 'This is a description.', 'This is a new static description.'),
    (CONFIGS, 'MIC-static', 'Metric: 42', 'This is a new static description.'),
    (CONFIGS, 'MIC-dynamic', 'This is a description.', 'This is a description.'),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', 'This is a new dynamic description with a metric: 42.'),
    (CONFIGS, 'unknown_issue', 'This is a description.', 'This is a description.'),
    (
        CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING,
        'IC-empty-regexp',
        'This is a description.',
        'This is a description.',
    ),
    (
        CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING,
        'IC-format-less-than-regexp',
        'Name: Aboba, Age: 69',
        'There is only one field: Aboba.',
    ),
    (CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING, 'IC-format-greater-than-regexp', 'Name: Aboba', 'Name: Aboba'),
    (
        CONFIGS_WITH_ESCAPED_CHARACTERS,
        'IC-one-escaped-curly-bracket-static',
        'This is a description.',
        'This is an escaped symbol: {',
    ),
    (
        CONFIGS_WITH_ESCAPED_CHARACTERS,
        'IC-paired-escaped-curly-bracket-static',
        'This is a description.',
        'This is a paired escaped curly bracket: {}',  # noqa: P103
    ),
    (
        CONFIGS_WITH_ESCAPED_CHARACTERS,
        'IC-one-escaped-curly-bracket-dynamic',
        'Name: Aboba',
        'This is an escaped symbol { and this is a format field Aboba',
    ),
    (
        CONFIGS_WITH_ESCAPED_CHARACTERS,
        'IC-paired-escaped-curly-bracket-dynamic',
        'Name: Aboba',
        'This is an escaped symbol {} and this is a format field Aboba',  # noqa: P103
    ),
]


@pytest.mark.parametrize(
    ('issue_configs', 'origin_class', 'description', 'expected_description'),
    GET_DESCRIPTION_TEST_DATA,
)
def test_get_description(
    issue_configs: List[IssueConfig],
    origin_class: str,
    description: str,
    expected_description: Optional,
):
    assert IssueConfigsHandler(*issue_configs).get_description(origin_class, description) == expected_description
