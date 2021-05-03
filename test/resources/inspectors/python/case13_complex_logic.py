def max_of_three(a, b, c):
    if a < b:
        if b < c:
            return c
        return b
    if a < c:
        return c
    return a


FEW_UNITS_NUMBER = 9
PACK_UNITS_NUMBER = 49
HORDE_UNITS_NUMBER = 499
SWARM_UNITS_NUMBER = 999


def army_of_units(count):
    if count < 1:
        print("no army")
    elif count <= FEW_UNITS_NUMBER:
        print('few')
    elif count <= PACK_UNITS_NUMBER:
        print('pack')
    elif count <= HORDE_UNITS_NUMBER:
        print("horde")
    elif count <= SWARM_UNITS_NUMBER:
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


SHEEP_PRICE = 6769
COW_PRICE = 3848
PIG_PRICE = 1296
GOAT_PRICE = 678
DOG_PRICE = 137
CHICKEN_PRICE = 23


def buy_animal(money):
    if money >= SHEEP_PRICE:
        number_of_sheep = money // SHEEP_PRICE
        print(f"{number_of_sheep} sheep")
    elif money >= COW_PRICE:
        print("1 cow")
    elif money >= PIG_PRICE:
        if money // PIG_PRICE == 1:
            print("1 pig")
        else:
            print("2 pigs")
    elif money >= GOAT_PRICE:
        print("1 goat")
    elif money >= DOG_PRICE:
        if money // DOG_PRICE == 1:
            print("1 dog")
        else:
            number_of_dogs = money // DOG_PRICE
            print(f"{number_of_dogs} dogs")
    elif money >= CHICKEN_PRICE:
        if money // CHICKEN_PRICE == 1:
            print("1 chicken")
        else:
            number_of_chickens = money // CHICKEN_PRICE
            print(f"{number_of_chickens} chickens")
    else:
        print("None")
