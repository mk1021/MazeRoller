import boto3
import math
from dataclasses import dataclass
from initialise_database import create_tables  # see if these causes problems since only the main function is here
import line_bounding_path_generation as bound_lines
from coin_coordinate_correction import correct_coords
import dual_angle_triangulation as dat


@dataclass
class DataEntry:
    """shadows the structure of a tuple for the database, not sure why..."""
    entry_type: str
    x: int
    y: int
    heading: float
    locaNum: int
    dist_to_goal: float
    followLWall: bool

    def distance_from(self, point) -> float:  # dk how to ensure that point is of type Coords
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def __init__(self, entry_type: str = "", x_coord: int = 0, y_coord: int = 0,
                 heading: float = 0, localisation_num: int = 0,
                 distance_to_goal: float = 420, following_left_wall: bool = True):
        self.entry_type = entry_type
        self.x, self.y = x_coord, y_coord
        self.heading = heading
        self.locNum = localisation_num
        self.dist_to_goal = distance_to_goal
        self.followLWall = following_left_wall


def update_table(dynamodb_obj, data_things):
    print("hi")
    # TODO: write the up to data thing, idk
    #       input heading to be stored with the previous set of coords (new set yet to be calculated)


# also a function to retrieve data after a website dropout


def recover_path_data(dynamodb_obj):
    # TODO: recover and organise path data into a 0
    return dynamodb_obj.get_path_data


def data_to_distance(sth):  # TODO: add relevant conversion calculation
    return sth


def how_far_from_goal(point):
    return math.sqrt((map_length - point.x) ** 2 + (map_width - point.y) ** 2)


def new_coord(prev_coord, data):
    cur_coord = [0, 0]
    # assuming movement data (preferably with heading/bearing) is sent as a list, assume [steps_moved, bearing]

    distance_moved = data_to_distance(data[0])

    cur_coord[0] = prev_coord[0] + round(distance_moved * math.sin(data[1]))
    cur_coord[1] = prev_coord[1] + round(distance_moved * math.cos(data[1]))

    # TODO: any other information we can pull from the coord and heading now?
    #       sth to help build the map, preferably

    return cur_coord


def main():
    dynamodb_obj = create_tables()
    prev_heading = 0
    coord = [0, 0]
    print("hi")

    db_obj = create_tables()

    # to be looped inside server thing
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # when receive new coords
    mvmnt_data = [5, math.pi / 2]  # tcp.receive() or sth

    buffered_data.append(mvmnt_data)

    # simple processing, then buffer collected data until new_localisation_data

    dat.triangulate_coords("RB 0.9823123 BY 1.5678123")

    active_data.stuff = buffered_data.stuff

    active_data.coords = correct_coords(buffered_data.coords, localisation_data)

    buffered_data.clear()

    coord = new_coord(coord, mvmnt_data)

    prev_heading = mvmnt_data[1]

    path_bitmap = bound_lines.generate_path(active_data)

    update_table(db_obj, active_data)  # before calc new coord, since old heading is only now available

    # TODO: add other things to update table with

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # not sure if there even needs to be more code outside the loop, but here we are


if __name__ == '__main__':
    new_localisation_data = False
    map_length = 343
    map_width = 225
    main()
