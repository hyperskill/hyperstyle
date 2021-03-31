elements = input()

row1 = elements[:3]
row2 = elements[3:6]
row3 = elements[6:]

CROSS = 'X' * 3
ZERO = 'O' * 3

row_with_x = row1 == CROSS or row2 == CROSS or row3 == CROSS
row_with_o = row1 == ZERO or row2 == ZERO or row3 == ZERO

if row1 == CROSS or row2 == CROSS or row3 == CROSS:
    print('X wins')

if CROSS == row1 or CROSS == row2:
    print('X wins')
