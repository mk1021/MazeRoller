import math
from main_script import DataEntry

class Coords:
    """only a single pair of values, but to be paired up with another pair :D"""
    x: int
    y: int

    def __init__(self, x_coord: int = 0, y_coord: int = 0):
        self.x, self.y = x_coord, y_coord


class CoordPair:
    """a pair of a pair of values, to be paired and used with another pair, in a pair :)"""
    L: Coords
    R: Coords

    def absolute_value(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __init__(self, left_coords: Coords, right_coords: Coords):
        if not left_coords or not right_coords:
            raise ValueError("One of these coordinates is NULL")
        self.L = left_coords
        self.R = right_coords


class Quadrilateral:
    """The Quads, this is the class that does the heavy-lifting"""
    Top: CoordPair
    Bottom: CoordPair

    def absolute_value(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __init__(self, left_coords: Coords, right_coords: Coords):
        if not left_coords or not right_coords:
            raise ValueError("One of these coordinates is NULL")
        self.L = left_coords    # TODO: implement this class
        self.R = right_coords


def generate_path(coordinates):



if __name__ == '__main__':
    generate_path({})
