from math import sqrt

MUTABLE_CONSTANT = {"1": 1, "2": 2}

class BadClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def Length(x: int, y: int) -> float:
        return sqrt(x ** 2 + y ** 2)
