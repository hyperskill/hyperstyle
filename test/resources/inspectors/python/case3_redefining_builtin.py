a = int(input())
b = int(input())
list = list(filter(lambda x: x % 3 == 0, range(a, b + 1)))
print(sum(list) / len(list))
