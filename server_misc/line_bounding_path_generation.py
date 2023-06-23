import math
from main_script import DataEntry

class Coords:
    """only a single pair of values, but to be paired up with another pair :D"""
    x: int
    y: int

    def __init__(self, x_coord: int = 0, y_coord: int = 0):
        self.x, self.y = x_coord, y_coord


class Quadrilateral:
    """The Quads, this is the class that does the heavy-lifting"""
    TopL: Coords
	   TopR: Coords
			 BottomL: Coords
    BottomR: Coords

    def absolute_value(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __init__(self, top_left: Coords, top_right: Coords, bottom_left: Coords, bottom_right: Coords):
        if not top_left or not top_left or not bottom_left or not bottom_right:
            raise ValueError("One of these coordinates is NULL")
        self.TopL = top_left
        self.TopR = top_right
					  self.BottomL = bottom_left
		     self.BottomR = bottom_right


def calculate_LR(datapoint: DataEntry):
    return [Coords(), Coords()]


def generate_path(coordinates):
    coord_quad = [Coords(), Coords(), Coords(), Coords()]
    main_quad = Quadrilateral()
    box_width, box_length = 0, 0
    for i in range(len(coordinates) - 1):
        coord_quad[:2] = calculateLR(coordinates[i])
					  coord_quad[2:] = calculateLR(coordinates[i+1])
		     coord_quad.sort(key=(lambda pair: math.sqrt(pair[0]**2 + pair[1]**2)))
        main_quad.BottomL = coord_quad[0]
        main_quad.TopR = coord_quad[3]
        if coord_quad[1][0] < coord_quad[2][0]:
            main_quad.TopL = coord_quad[1]
								  main_quad.BottomR = coord_quad[2]
        else:
            main_quad.TopL = coord_quad[2]
								  main_quad.BottomR = coord_quad[1]
        
        return main_quad.bound_lines()


if __name__ == '__main__':
    generate_path({})


