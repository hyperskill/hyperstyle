numbers = [0 for _ in range(10)]

list(n + 1 for n in numbers)
set(n + 1 for n in numbers)

set([n + 1 for n in numbers])
dict([(n, n * n) for n in numbers])

tuple([1, 2])  # (1, 2)
tuple([])  # ()

dict(((1, 2),))  # {1: 2}

sum([x ** 2 for x in range(10)])  # sum(x ** 2 for x in range(10))

test_dict = dict()   # we allow this
test_list = list()   # we allow this
test_tuple = tuple()  # we allow this

list([0 for _ in range(10)])

reversed(sorted([2, 3, 1]))  # sorted([2, 3, 1], reverse=True)
