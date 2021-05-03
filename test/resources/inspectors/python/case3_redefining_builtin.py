a = int(input())
b = int(input())

range = range(a, b + 1)

list = list(filter(lambda x: x % 3 == 0, range))
print(sum(list) / len(list))
