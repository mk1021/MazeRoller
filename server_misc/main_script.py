import boto3
import math
from dataclasses import dataclass
from initialise_database import create_tables  # see if these causes problems since only the main function is here
import line_bounding_path_generation as bound_lines
from line_bounding_path_generation import Coords
from coin_coordinate_correction import correct_coords
import dual_angle_triangulation as dat


@dataclass
class DataEntry:
    """shadows the structure of a tuple for the database, not sure why...
        PathSquares won't be stored in here, simply because they don't really need to be"""
    entry_type: str
    item_id: int
    coords: Coords
    heading: float
    locNum: int
    dist_to_goal: float
    followLWall: bool

    def distance_from(self, point: Coords) -> float:  # dk how to ensure that point is of type Coords
        return math.sqrt((point.x - self.coords.x) ** 2 + (point.y - self.coords.y) ** 2)

    def __init__(self, entry_type: str, item_number: int, x_coord: int, y_coord: int,
                 heading: float = 0, localisation_num: int = 0,
                 distance_to_goal: float = 420, following_left_wall: bool = True):
        self.entry_type = entry_type    # TODO: maybe swap this out for bool (is_movement or sth)
        self.item_id = item_number
        self.coords = Coords(x_coord, y_coord)
        self.heading = heading
        self.locNum = localisation_num
        self.dist_to_goal = distance_to_goal
        self.followLWall = following_left_wall


def update_table(dynamodb_obj, data_things, is_mvmnt: str):
    # for m: movement, r: rotation, p: path
    print("hi")
    # TODO: write the up to data thing, idk
    #       input heading to be stored with the previous set of coords (new set yet to be calculated)


# also a function to retrieve data after a website dropout

def handle_initial_datapoint(idk):
    # TODO: handle the initial case with (5, 5), heading = 0,
    #       maybe just handle whole initiation process
    return -1


def merge_double_rotation(datapoint_ls):
    # TODO: make the last two into one
    return -1


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


def unpack(input_data, is_localisation: bool = False):
    if is_localisation:
        # TODO: unpack data as (theta, phi)
        return 2, 3

    # TODO: take the file format received from node.js and turn it into a DataEntry object
    # types: F, B, C, A; L will trigger a special event, overwriting previous item_id's values
    return DataEntry("misc", -1, 0, 0)


def main():  # think this would be better handled in node.js
    dynamodb_obj = create_tables()
    prev_heading = 0
    buffered_mvmnt_data = []
    buffered_rotation_data = []
    active_mvmnt_data = []
    active_rotation_data = []
    print("hi")

    db_obj = create_tables()

    # to be looped inside server thing
    # -----------------------regular data buffering--------------------------

    mvmnt_data = [5, math.pi / 2]
    """
    receive as parameter from node.js call, I'd assume
    but crucially, the new coord calculations will be handled by the node.js
    everything is python's responsibility, but node.js will hold the prev_heading and idek bruh, I'm tired    
    """

    new_entry = unpack(mvmnt_data)

    if new_entry.entry_type == "r":
        buffered_rotation_data.append(new_entry)
        if buffered_rotation_data[-2].item_id == buffered_rotation_data[-2].item_id:
            merge_double_rotation(buffered_rotation_data)
    else:
        buffered_mvmnt_data.append(new_entry)
        # number_of_moves += 1  # TODO: uncomment later, this is a global variable

    # simple processing, then buffer collected data until new_localisation_data

    # -----------------------on localisation event--------------------------

    buffered_coord_data = [datapoint.coords for datapoint in buffered_mvmnt_data]

    active_mvmnt_data = buffered_mvmnt_data

    buffered_mvmnt_data.clear()   # buffered_data list can now continue to receive new data

    localisation_data = dat.triangulate_coords(unpack(mvmnt_data, True))

    # -----------------------data correction stage--------------------------

    corrected_coord_data = correct_coords(buffered_coord_data, localisation_data)

    for i in range(len(corrected_coord_data)):
        active_mvmnt_data[i].coords = corrected_coord_data[i]

    update_table(db_obj, active_mvmnt_data, 'm')

    # TODO: correct rotation data first, too, somehow
    update_table(db_obj, active_rotation_data, 'r')

    # -----------------------path generation stage--------------------------

    path_bitmap = bound_lines.generate_path(active_mvmnt_data)

    update_table(db_obj, active_rotation_data, 'p')

    # I believe that is all


if __name__ == '__main__':
    number_of_moves = 0  # only update on movement, not on rotation
    localisations_thus_far = 0  # increment with each new localisation event
    map_length, map_width = 343, 225
    main()
