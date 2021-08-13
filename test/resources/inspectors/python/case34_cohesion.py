from math import sqrt


class BadClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def length(x: int, y: int) -> float:
        return sqrt(x ** 2 + y ** 2)

    @staticmethod
    def dot(self_x: int, self_y: int, other_x: int, other_y: int) -> int:
        return self_x * other_x + self_y * other_y


class GoodClass(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def length(self) -> float:
        return sqrt(self.dot(self.x, self.y))

    def dot(self, other_x: int, other_y: int) -> int:
        return self.x * other_x + self.y * other_y
