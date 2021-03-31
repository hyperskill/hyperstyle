def f_1(y):
    if not y:
        return
    return None  # error!


def f_2(y):
    if not y:
        return  # error!
    return 1


def f_3(y):
    if not y:
        return  # error!
    return 1


def f_4():
    a = 1
    # some code that not using `a`
    print('test')
    return a  # error!
