MUTABLE_CONSTANT = {"1": 1, "2": 2}

PI = 3.14
DOUBLE_PI = 6.28
E = 2.71


def function_with_bad_try(b, c):
    result = None

    try:
        result = b / c
    except Exception:
        print("It's fine")

    return result


def bad_generator(some_value):
    if some_value:
        raise StopIteration
    yield 1


if __name__ == "__main__":

    print("Hello, World!")
