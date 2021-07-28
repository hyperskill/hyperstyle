from numpy import *

n, m = [int(_) for _ in input().split()]
mat = zeros((n, m))
s = 1
for j in range(n):
    for i in range(j, m - j):
        if s > n * m:
            break
        mat[j][i] = s
        s += 1

    for i in range(j - n + 1, -j):
        if s > n * m:
            break
        mat[i][-j - 1] = s
        s += 1
    for i in range(-j - 2, -m + j - 1, -1):
        if s > n * m:
            break
        mat[-j - 1][i] = s
        s += 1

    for i in range(-2 - j, -n + j, -1):
        if s > n * m:
            break
        mat[i][j] = s
        s += 1

for r in range(n):
    for c in range(m):
        print(str(int(mat[r][c])).ljust(2), end=' ')
    print()
