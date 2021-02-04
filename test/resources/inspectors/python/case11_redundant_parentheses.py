nuts = int(input())

if (nuts > 10):
    print('There is enough nuts')
else:
    print('Not enough nuts')

i = 1
while (i <= nuts):
    print(f'Give the nuth №{i}')
    i += 1
