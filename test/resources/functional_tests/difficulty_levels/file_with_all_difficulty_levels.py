from math import sqrt

MUTABLE_CONSTANT = {"1": 1, "2": 2}

class BadClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def Length(x: int, y: int) -> float:
        return sqrt(x ** 2 + y ** 2)

    @staticmethod
    def dot(self_x: int, self_y: int, other_x: int, other_y: int) -> int:
        return self_x * other_x + self_y * other_y

    @staticmethod
    def plus(self_x: int, self_y: int, other_x: int, other_y: int) -> 'BadClass':
        return BadClass(self_x + other_x, self_y + other_y)

    @staticmethod
    def minus(self_x: int, self_y: int, other_x: int, other_y: int) -> 'BadClass':
        return BadClass(self_x - other_x, self_y - other_y)