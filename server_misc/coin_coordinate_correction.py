import math


class Coin:
    """like a regular coin, but in 2D and fractional..."""
    x: float
    y: float

    def absolute_value(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __init__(self, a: float = 0, b: float = 0):
        self.x, self.y = a, b


def correct_coords(data, reliable_coords):
    if not data:
        return data

    error = Coin()
    error.x = reliable_coords[0] - data[-1].x
    error.y = reliable_coords[1] - data[-1].y

    if error.absolute_value() < 0.5 or len(data) == 1:
        data[-1] = reliable_coords
        return data

    nodes = len(data)
    coins_total = (nodes * (nodes+1)) / 2  # quantitative easing right here
    value = Coin(error.x / coins_total, error.y / coins_total)

    carry = Coin(0, 0)
    node_wealth = Coin()
    rounded = Coin()
    coins_used = 0
    for i in range(nodes):
        coins_per_node = (i+1)*(i+2) / 2  # since i starts from 0
        coins_used += coins_per_node
        node_wealth.x = coins_per_node*value.x + carry.x
        node_wealth.y = coins_per_node*value.y + carry.y

        rounded.x = round(node_wealth.x)
        rounded.y = round(node_wealth.y)

        carry.x =  node_wealth.x - rounded.x 
        carry.y =  node_wealth.y - rounded.y  # update carry values for next node

        data[i].x += rounded.x
        data[i].y += rounded.y

        # just to check that we don't leave the board, though this should never happen in practice
        data[i].x *= data[i].x > 0
        data[i].x *= data[i].y > 0

        if data[i].x > map_length: 
            data[i].x = map_length
        if data[i].y > map_width:
            data[i].y = map_width

    return data


if __name__ == '__main__':
    map_length = 343
    map_width = 225

    data = []  # nice list of data entries
    data = correct_coords(data, (0, 0))
    print(data)
