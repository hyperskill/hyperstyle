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


if __name__ == "__main__":
    print("Hello, World!")
