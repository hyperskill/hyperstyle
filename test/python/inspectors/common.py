import pytest

from hyperstyle.src.python.review.inspectors.common import is_fstring

IS_FSTRING_TEST_DATA = [
    ('', False),
    ('abcdef', False),
    ('{{}}', False),
    ('{{0}}', False),
    ('{{false}}', False),
    ('{}', True),
    ('{2}', True),
    ('{abc}', True),
    ('{} {{}} {0} {abc}', True),
    ('This is a {f}-string!', True),
]


@pytest.mark.parametrize(('string', 'expected'), IS_FSTRING_TEST_DATA)
def test_is_fstring(string: str, expected: bool):
    assert is_fstring(string) == expected
