def f1(y):
    if not y:
        return
    return None  # error!


def f2(y):
    if not y:
        return  # error!
    return 1


def f3(y):
    if not y:
        return  # error!
    return 1


def f4():
    a = 1
    # some code that not using `a`
    print('test')
    return a  # error!
