from __future__ import annotations

import pytest

from hyperstyle.src.python.review.inspectors.common.utils import (
    _get_format_fields,
    contains_format_fields,
    contains_named_format_fields,
)

GET_FORMAT_FIELDS_TEST_DATA = [
    ("", []),
    ("abcdef", []),
    ("{{}}", []),
    ("{{0}}", []),
    ("{{false}}", []),
    ("{{abc:.3f}}", []),
    ("{}", [""]),
    ("{0}", ["0"]),
    ("{false}", ["false"]),
    ("{abc:.3f}", ["abc"]),
    ("{} {{}} {0} {abc}", ["", "0", "abc"]),
    ("This is a {f}-string!", ["f"]),
    ("{key: value for key, value in dct.items()}", ["key"]),
]


@pytest.mark.parametrize(("string", "expected_fields"), GET_FORMAT_FIELDS_TEST_DATA)
def test_get_format_fields(string: str, expected_fields: list[str]) -> None:
    assert _get_format_fields(string) == expected_fields


CONTAINS_FORMAT_FIELDS_TEST_DATA = [
    ("", False),
    ("abcdef", False),
    ("{{}}", False),
    ("{{0}}", False),
    ("{{false}}", False),
    ("{{abc:.3f}}", False),
    ("{}", True),
    ("{0}", True),
    ("{false}", True),
    ("{abc:.3f}", True),
    ("{} {{}} {0} {abc}", True),
    ("This is a {f}-string!", True),
    ("{key: value for key, value in dct.items()}", True),
]


@pytest.mark.parametrize(("string", "expected"), CONTAINS_FORMAT_FIELDS_TEST_DATA)
def test_contains_format_fields(string: str, expected: bool) -> None:
    assert contains_format_fields(string) == expected


CONTAINS_NAMED_FORMAT_FIELDS_TEST_DATA = [
    ("", False),
    ("abcdef", False),
    ("{{}}", False),
    ("{{0}}", False),
    ("{{false}}", False),
    ("{{abc:.3f}}", False),
    ("{}", False),
    ("{0}", False),
    ("{false}", True),
    ("{abc:.3f}", True),
    ("{} {{}} {0} {abc}", True),
    ("This is a {f}-string!", True),
    ("{key: value for key, value in dct.items()}", True),
]


@pytest.mark.parametrize(("string", "expected"), CONTAINS_NAMED_FORMAT_FIELDS_TEST_DATA)
def test_contains_named_format_fields(string: str, expected: bool) -> None:
    assert contains_named_format_fields(string) == expected
