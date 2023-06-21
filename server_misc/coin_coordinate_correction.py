import math
from dataclasses import dataclass


@dataclass
class Coin:
    """like a regular coin, but in 2D and in decimals..."""
    x: float
    y: float

    def absolute_value(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __init__(self, a: float = 0, b: float = 0):
        self.x, self.y = a, b


def correct_coords(data, reliable_coords):
    if data.empty():
        return data

    error = Coin()
    error.x = reliable_coords[0] - data[-1].x
    error.y = reliable_coords[1] - data[-1].y

    if error.absolute_value() < 0.5 or len(data) == 1:
        data[-1] = reliable_coords
        return data

    nodes = len(data)
    coins_total = (nodes * (nodes+1) * (nodes+2)) / 6  # quantitative easing right here
    value = Coin(error.x / coins_total, error.y / coins_total)

    carry = Coin(0, 0)
    node_wealth = Coin()
    rounded = Coin()
    for i in range(nodes):
        coins_per_node = i*(i+1) / 2
        node_wealth.x = coins_per_node*value.x + carry.x
        node_wealth.y = coins_per_node * value.y + carry.y
        # TODO: Finish writing up the implementation of this algorithm


if __name__ == '__main__':
    correct_coords({}, ())
