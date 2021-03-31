def max_of_three(a, b, c):
    if a < b:
        if b < c:
            return c
        return b
    if a < c:
        return c
    return a


def army_of_units(count):
    if count < 1:
        print("no army")
    elif count <= 9:
        print('few')
    elif count <= 49:
        print('pack')
    elif count <= 499:
        print("horde")
    elif count <= 999:
        print('swarm')
    else:
        print('legion')


def sequence_calculator(x, y, op):
    if op == "+":
        print(x + y)
    elif op == "-":
        print(x - y)
    elif op == "*":
        print(x * y)
    elif op == "/":
        if y == 0:
            print("Division by 0!")
        else:
            print(x / y)
    elif op == "mod":
        if y == 0:
            print("Division by 0!")
        else:
            print(x % y)
    elif op == "div":
        if y == 0:
            print("Division by 0!")
        else:
            print(x // y)
    elif op == "pow":
        print(x ** y)


def determine_strange_quark(spin, charge):
    if spin == '1/2':
        if charge == '-1/3':
            print("Strange Quark")
        elif charge == '2/3':
            print("Charm Quark")
        elif charge == '-1':
            print("Electron Lepton")
        elif charge == '0':
            print("Muon Lepton")
    elif spin == '1':
        print("Photon Boson")
    elif spin == '0':
        print("Higgs boson Boson")


def buy_animal(money):
    if money >= 6769:
        print(str(money // 6769) + " sheep")
    elif money >= 3848:
        print("1 cow")
    elif money >= 1296:
        if money // 1296 == 1:
            print("1 pig")
        else:
            print("2 pigs")
    elif money >= 678:
        print("1 goat")
    elif money >= 137:
        if money // 137 == 1:
            print("1 dog")
        else:
            print(str(money // 137) + " dogs")
    elif money >= 23:
        if money // 23 == 1:
            print("1 chicken")
        else:
            print(str(money // 23) + " chickens")
    else:
        print("None")


def fun_with_complex_logic(a, b, c):
    d = 0
    if a > 10:
        d = 30
    elif a < 100:
        d = 50
    elif a == 300 and b == 40:
        for i in range(9):
            a += i
    elif a == 200:
        if b > 300 and c < 50:
            d = 400
        else:
            d = 800
    elif a == 2400:
        if b > 500 and c < 50:
            d = 400
        else:
            d = 800
    elif a == 1000:
        if b == 900:
            if c == 1000:
                d = 10000
            else:
                d = 900
        elif c == 300:
            d = 1000
        elif a + b == 400:
            d = 400
    print(d)
    return d
