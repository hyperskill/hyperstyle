from math import sqrt


class BadClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def length(x: int, y: int) -> float:
        return sqrt(x ** 2 + y ** 2)


if __name__ == "__main__":
    print("Hello, World!")
