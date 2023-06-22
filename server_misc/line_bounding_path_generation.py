import math


class Coords:
    """only a single pair of values, but to be paired up with another pair :D"""
    x: int
    y: int

    def __init__(self, x_coord: int = 0, y_coord: int = 0):
        self.x, self.y = x_coord, y_coord


class CoordPairs:
    """a pair of a pair of values, to be paired used with another pair, in pair :)"""
    L: float
    R: Coords

    def absolute_value(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __init__(self, a: float = 0, b: float = 0):
        self.x, self.y = a, b


def generate_path(coordinates):
    prev_heading = 0
    coord = [0, 0]
    print("hi")


if __name__ == '__main__':
    generate_path({})
