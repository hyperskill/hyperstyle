
a = int(input())
b = int(input())
c = int(input())
d = int(input())

if a > b:
    print('a > b')

if a > b and a > b:
    print('a > b again')

if a > b and a < d:
    print('b < a < d')

if not a > b:
    print('not a > b')

if b < a < d:
    print('b < a < d again')

if a > b == True:
    print('a > b and True')

if True:
    print('qqq')

enabled = False  # It does not work now
if a > b and b < c and c > d or c < a and enabled:
    print('Too complex expression')
