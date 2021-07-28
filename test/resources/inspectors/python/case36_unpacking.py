[a, b, c], [x, y, z] = (sorted(map(int, input().split())) for _ in 'lm')
if [a, b, c] == [x, y, z]:
    a = "Boxes are equal"
elif a <= x and b <= y and c <= z:
    a = "The first box is smaller than the second one"
elif a >= x and b >= y and c >= z:
    a = "The first box is larger than the second one"
else:
    a = "Boxes are incomparable"
print(a)
