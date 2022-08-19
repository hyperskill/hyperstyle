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
    (MATCH_ONE_GROUP, str, '12345', ('12345',)),
    (MATCH_ONE_GROUP, int, '12345', (12345,)),
    (MATCH_ONE_GROUP, float, '12345.6789', (12345.6789,)),
    (MATCH_ONE_GROUP, float, 'abcdef', None),
    (MATCH_TWO_GROUPS, None, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_GROUPS, str, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_GROUPS, int, '(12345) {67890}', (12345, 67890)),
    (MATCH_TWO_GROUPS, float, '(12345.6789) {67890.12345}', (12345.6789, 67890.12345)),
    (MATCH_TWO_GROUPS, float, '(abc) {def}', None),
    (MATCH_TWO_GROUPS, float, '(12345.6789) {abcdef}', None),
    (MATCH_ONE_NAMED_GROUP, None, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, str, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, int, '12345', (12345,)),
    (MATCH_ONE_NAMED_GROUP, float, '12345.6789', (12345.6789,)),
    (MATCH_ONE_NAMED_GROUP, float, 'abcdef', None),
    (MATCH_ONE_NAMED_GROUP, {'group': str}, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, {'group': int}, '12345', (12345,)),
    (MATCH_ONE_NAMED_GROUP, {'group': float}, '12345.6789', (12345.6789,)),
    (MATCH_ONE_NAMED_GROUP, {}, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, {'unknown_name': int}, '12345', ('12345',)),
    (MATCH_ONE_NAMED_GROUP, {'group': float}, 'abcdef', None),
    (MATCH_TWO_NAMED_GROUPS, None, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_NAMED_GROUPS, str, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_NAMED_GROUPS, int, '(12345) {67890}', (12345, 67890)),
    (MATCH_TWO_NAMED_GROUPS, float, '(12345.6789) {67890.12345}', (12345.6789, 67890.12345)),
    (MATCH_TWO_NAMED_GROUPS, float, '(abc) {def}', None),
    (MATCH_TWO_NAMED_GROUPS, float, '(12345.6789) {def}', None),
    (MATCH_TWO_NAMED_GROUPS, {}, '(12345) {67890}', ('12345', '67890')),
    (MATCH_TWO_NAMED_GROUPS, {'unknown_name': float}, '(abc) {def}', ('abc', 'def')),
    (MATCH_TWO_NAMED_GROUPS, {'curly_group': float}, '(abcdef) {12345.6789}', ('abcdef', 12345.6789)),
    (
        MATCH_TWO_NAMED_GROUPS,
        {'parentheses_group': int, 'curly_group': float},
        '(12345) {67890.12345}',
        (12345, 67890.12345),
    ),
    (MATCH_TWO_NAMED_GROUPS, {'parentheses_group': int, 'curly_group': float}, '(12345) {abcdef}', None),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, None, '|a| (bc) |d| {ef} |g|', ('a', 'bc', 'd', 'ef', 'g')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, str, '|a| (bc) |d| {ef} |g|', ('a', 'bc', 'd', 'ef', 'g')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, int, '|1| (23) |4| {56} |7|', (1, 23, 4, 56, 7)),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, float, '|1.2| (3.4) |5.6| {7.8} |9.0|', (1.2, 3.4, 5.6, 7.8, 9.0)),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, float, '|1.2| (bc) |d| {ef} |g|', None),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {}, '|a| (bc) |d| {ef} |g|', ('bc', 'ef')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {'unknown_name': int}, '|a| (bc) |d| {ef} |g|', ('bc', 'ef')),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {'parentheses_group': int}, '|a| (123) |d| {456} |g|', (123, '456')),
    (
        MATCH_NAMED_AND_UNNAMED_GROUPS,
        {'parentheses_group': int, 'curly_group': int},
        '|a| (123) |d| {456} |g|',
        (123, 456),
    ),
    (
        MATCH_NAMED_AND_UNNAMED_GROUPS,
        {'parentheses_group': int, 'curly_group': float},
        '|a| (123) |d| {456.789} |g|',
        (123, 456.789),
    ),
    (MATCH_NAMED_AND_UNNAMED_GROUPS, {'parentheses_group': int, 'curly_group': float}, '|a| (123) |d| {ef} |g|', None),
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
        ['IC'],
        TypeError,
        'You must specify a new description.',
    ),
    (
        IssueConfig,
        ['IC', 'This is a format string! {0}'],
        TypeError,
        'You need to specify a parser, since you are using a format string.',
    ),
    (
        IssueConfig,
        ['IC', None, IssueDescriptionParser(re.compile(''))],
        TypeError,
        'You must specify a new description.',
    ),
    (
        IssueConfig,
        ['IC', 'This is a simple string!', IssueDescriptionParser(re.compile(''))],
        TypeError,
        'You specified the parser, but the new description is not a format string.',
    ),
    (MeasurableIssueConfig, ['MIC'], TypeError, 'You must specify a parser.'),
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
        origin_class='MIC-default',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
    ),
    MeasurableIssueConfig(
        origin_class='MIC-static',
        new_description='This is a new static description.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
    ),
    MeasurableIssueConfig(
        origin_class='MIC-dynamic',
        new_description="This is a new dynamic description with a metric: {0}.",
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
    ),
]

PARSE_DESCRIPTION_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is an description.', None),
    (CONFIGS, 'IC-dynamic', 'This is an description.', None),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', ('abcdef',)),
    (CONFIGS, 'MIC-default', 'This is an description.', None),
    (CONFIGS, 'MIC-default', 'Metric: 42', (42,)),
    (CONFIGS, 'MIC-static', 'This is an description.', None),
    (CONFIGS, 'MIC-static', 'Metric: 42', (42,)),
    (CONFIGS, 'MIC-dynamic', 'This is an description.', None),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', (42,)),
    (CONFIGS, 'unknown_issue', 'This is an description.', None),
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


CONFIGS_WITH_BAD_MEASURE_POSITION = [
    MeasurableIssueConfig(
        origin_class='MIC-bad-default',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
        measure_position=42,
    ),
    MeasurableIssueConfig(
        origin_class='MIC-bad-static',
        new_description='This is a new static description.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
        measure_position=42,
    ),
    MeasurableIssueConfig(
        origin_class='MIC-bad-dynamic',
        new_description='This is a new dynamic description with a metric: {0}.',
        parser=IssueDescriptionParser(
            regexp=re.compile(r"Metric: (\d+)"),
            converter=int,
        ),
        measure_position=42,
    ),
]


PARSE_MEASURE_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is an description.', None),
    (CONFIGS, 'IC-dynamic', 'This is an description.', None),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', None),
    (CONFIGS, 'MIC-default', 'This is an description.', None),
    (CONFIGS, 'MIC-default', 'Metric: 42', 42),
    (CONFIGS, 'MIC-static', 'This is an description.', None),
    (CONFIGS, 'MIC-static', 'Metric: 42', 42),
    (CONFIGS, 'MIC-dynamic', 'This is an description.', None),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', 42),
    (CONFIGS, 'unknown_issue', 'This is an description.', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-default', 'This is an description.', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-default', 'Metric: 42', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-static', 'This is an description.', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-static', 'Metric: 42', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-dynamic', 'This is an description.', None),
    (CONFIGS_WITH_BAD_MEASURE_POSITION, 'MIC-bad-dynamic', 'Metric: 42', None),
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
        parser=IssueDescriptionParser(re.compile(r'This is an description')),
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


GET_DESCRIPTION_TEST_DATA = [
    (CONFIGS, 'IC-static', 'This is an description.', 'This is a new static description.'),
    (CONFIGS, 'IC-dynamic', 'This is an description.', 'This is an description.'),
    (CONFIGS, 'IC-dynamic', 'Name: abcdef', 'This is a new dynamic description: abcdef.'),
    (CONFIGS, 'MIC-default', 'This is an description.', 'This is an description.'),
    (CONFIGS, 'MIC-default', 'Metric: 42', 'Metric: 42'),
    (CONFIGS, 'MIC-static', 'This is an description.', 'This is a new static description.'),
    (CONFIGS, 'MIC-static', 'Metric: 42', 'This is a new static description.'),
    (CONFIGS, 'MIC-dynamic', 'This is an description.', 'This is an description.'),
    (CONFIGS, 'MIC-dynamic', 'Metric: 42', 'This is a new dynamic description with a metric: 42.'),
    (CONFIGS, 'unknown_issue', 'This is an description.', 'This is an description.'),
    (
        CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING,
        'IC-empty-regexp',
        'This is an description.',
        'This is an description.',
    ),
    (
        CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING,
        'IC-format-less-than-regexp',
        'Name: Aboba, Age: 69',
        'There is only one field: Aboba.',
    ),
    (CONFIGS_WITH_INCONSISTENT_PARSER_AND_FORMAT_STRING, 'IC-format-greater-than-regexp', 'Name: Aboba', 'Name: Aboba'),
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
