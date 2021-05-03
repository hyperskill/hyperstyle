# Wrong C-812
from math import (
    log
)

# Correct
from math import (
    sin,
)

# Wrong C-812
bad_multiline_dict = {
    "first": 1,
    "second": 2
}

# Correct
good_multiline_dict = {
    "first": 1,
    "second": 2,
}

# Wrong C-812
bad_multiline_list = [
    1,
    2,
    3
]

# Correct
good_multiline_list = [
    1,
    2,
    3,
]

# Wrong C-812
bad_multiline_tuple = (
    3,
    4
)

good_multiline_tuple = (
    3,
    4,
)


# Wrong C-812
def bad_function(
        a,
        b
):
    return log(a, b)


bad_function(
    1,
    2
)

bad_function(
    a=1,
    b=2
)


# Correct
def good_function(
        a,
        b,
):
    return a + sin(b)


good_function(
    1,
    2,
)

good_function(
    a=1,
    b=2,
)

# Wrong: C-813
print(
    "Hello",
    "World"
)

# Correct
print(
    "Hello",
    "World",
)


# Wrong: C-816
def bad_function_with_unpacking(
        a,
        b,
        **kwargs
):
    pass


# Correct
def good_function_with_unpacking(
        a,
        b,
        **kwargs,
):
    pass


# Wrong: C-815
good_function_with_unpacking(
    1,
    2,
    **good_multiline_dict
)

# Correct
good_function_with_unpacking(
    1,
    2,
    **good_multiline_dict,
)

# Wrong: C-818
bad_comma = 1,

# Correct
good_comma = (1,)

# Wrong: C-819
bad_list = [1, 2, 3, ]

# Correct:
good_list = [1, 2, 3]

# Wrong: C-819
bad_dict = {"1": 1, "2": 2, "3": 3, }

# Correct:
good_dict = {"1": 1, "2": 2, "3": 3}

# Wrong: C-819
bad_tuple = (1, 2, 3,)

# Correct
good_tuple = (1, 2, 3)
