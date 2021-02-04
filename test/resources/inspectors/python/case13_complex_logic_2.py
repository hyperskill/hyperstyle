elements = list(input('Enter cells: '))
y = 0
o = 0
for x in elements:
    if x == 'X':
        y = y + 1
    elif x == 'O':
        o = o + 1

odds = abs(y - o)

up_row = [elements[0], elements[1], elements[2]]
mid_row = [elements[3], elements[4], elements[5]]
down_row = [elements[6], elements[7], elements[8]]

up_col = [elements[0], elements[3], elements[6]]
mid_col = [elements[1], elements[4], elements[7]]
down_col = [elements[2], elements[5], elements[8]]

diagonal1 = [elements[0], elements[4], elements[8]]
diagonal2 = [elements[2], elements[4], elements[6]]

full_field = [up_row, up_col, mid_row, mid_col, down_row, down_col, diagonal1, diagonal2]

x_win = ['X', 'X', 'X']
o_win = ['O', 'O', 'O']

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
        print('X wins')
    elif o_win in full_field and x_win not in full_field:
        print(field)
        print('O wins')
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
