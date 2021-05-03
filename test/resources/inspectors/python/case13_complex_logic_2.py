elements = list(input('Enter cells: '))
y = 0
o = 0

CROSS_SYMBOL = 'X'
NOUGHT_SYMBOL = 'O'

for x in elements:
    if x == CROSS_SYMBOL:
        y = y + 1
    elif x == NOUGHT_SYMBOL:
        o = o + 1

odds = abs(y - o)

up_row = [elements[0], elements[1], elements[2]]
mid_row = [elements[3], elements[4], elements[5]]
down_row = [elements[6], elements[7], elements[8]]

up_col = [elements[0], elements[3], elements[6]]
mid_col = [elements[1], elements[4], elements[7]]
down_col = [elements[2], elements[5], elements[8]]

diagonal_1 = [elements[0], elements[4], elements[8]]
diagonal_2 = [elements[2], elements[4], elements[6]]

full_field = [up_row, up_col, mid_row, mid_col, down_row, down_col, diagonal_1, diagonal_2]

x_win = [CROSS_SYMBOL, CROSS_SYMBOL, CROSS_SYMBOL]
o_win = [NOUGHT_SYMBOL, NOUGHT_SYMBOL, NOUGHT_SYMBOL]

field = f"""
---------
| {elements[0]} {elements[1]} {elements[2]} |
| {elements[3]} {elements[4]} {elements[5]} |
| {elements[6]} {elements[7]} {elements[8]} |
---------
"""
if odds < 2:
    if x_win in full_field and o_win not in full_field:
        print(field)
        print(f'{CROSS_SYMBOL} wins')
    elif o_win in full_field and x_win not in full_field:
        print(field)
        print(f'{NOUGHT_SYMBOL} wins')
    elif o_win in full_field and x_win in full_field:
        print(field)
        print('Impossible')
    elif '_' not in elements:
        if o_win not in full_field and x_win not in full_field:
            print(field)
            print('Draw')
    elif '_' in elements:
        if o_win not in full_field and x_win not in full_field:
            print(field)
            print('Game not finished')
elif odds >= 2:
    print(field)
    print('Impossible')
