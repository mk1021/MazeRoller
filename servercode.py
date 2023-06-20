# libraries
import socket
import boto3
from boto3.dynamodb.conditions import Key
import math
import cmath
import time

port = 5555
current_angle = 0
current_coordinates = 0, 0
movement_increment = 0.8


# ---------------------------- DATABASE FUNCTIONS ----------------------------------------

def write_to_database(identifier, data_type):
    # Write to database with the specified data type and current timestamp
    timestamp = datetime.now().isoformat()
    item = {'Id': identifier, 'Coordinates': coords, 'timestamp': timestamp}  # to edit
    table.put_item(Item=item)


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Create the DynamoDB table
    table = dynamodb.create_table(
        TableName='MazeRoverData',
        KeySchema=[
            {
                'AttributeName': 'coordid',
                'KeyType': 'RANGE'  # Partition Key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'coordid',
                'AttributeType': 'N'  # timestamp is numeric
            },
            {
                'AttributeName': 'coordinates',
                'AttributeType': 'L'  # list/array of coordinates [x, y]
            },
            {
                'AttributeName': 'datatype',
                'AttributeType': 'S'  # string (letters) indicating datatype
            }
        ],
        ProvisionedThroughput={
            # the table can handle upto 5 read and writes per second
            'ReadCapacityUnits': 5,
            # represents the desired capacity for read operations
            'WriteCapacityUnits': 5
            # represents the desired capacity for write operations
        }
    )
    return table


# ------------------------- LOCALISATION FUNCTIONS ---------------------------------------

# Using FPGA to calulcate the centre angles between beacons
def timeToAngle(timetaken):
    degrees = (timetaken / "REPLACE WITH CONSTANT") * 360
    angle = degrees * (math.pi / 180)
    return angle


# Using Image Processing to find the distance between the rover and each sensor
def distance(pixels):
    # 1.4 micrometers in meters
    pixel_width = 0.0000014
    # 3.85 mm in metres
    focal_length = 0.00385
    # _____________ (i've just added in a random value of 4.5cm for the height of the sensor)
    realheight = 0.045

    D = (realheight * focal_length) / (pixels * pixel_width)
    return D


# Using Trigonometric Principles (like Sine Rule) to find other angles in the triangles
def findCoordinates(yellow_d, red_d, blue_d, yr_a, rb_a):
    # Using Sine Rule to find other necessary angles (why are these named like this?)
    angle_y = math.asin((red_d * math.sin(yr_a)) / "REPLACE WITH YR DIST")
    angle_r = math.asin((yellow_d * math.sin(yr_a)) / "REPLACE WITH YR DIST")
    angle_b = math.asin((red_d * math.sin(rb_a)) / "REPLACE WITH RB DIST")

    angle_x = 90 - angle_y
    angle_s = 90 - angle_r
    angle_a = 90 - angle_b

    # Using SOHCAHTOA to find x,y co-ordinates
    x_coordinate = yellow_d * math.sin(angle_x)
    y_coordinate = blue_d * math.sin(angle_a)

    return x_coordinate, y_coordinate


# --------------------------------------------------------------------------------------------------

# SETUP: dynamoDB table

data_table = create_table()
print("Status:", data_table.table_status)

# SETUP: Server and Client Connection
tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpserver.bind(('0.0.0.0', port))

tcpserver.settimeout(0)

tcpserver.listen(1)

client_connected = False

while client_connected == False:

    try:
        rover, address = tcpserver.accept()
        print("Rover connected from {address}")
    except:
        continue

# main server loop
while True:

    try:
        countID = 0
        data_from_esp = rover.recv(1024)
        data_from_esp = data_from_esp.decode()
        if data_from_esp[0] == "M":
            movement_decision = data_from_esp[1]
            if movement_decision == "L":
                current_angle += "SOMETHING"
                if current_angle >= 180:
                    current_angle = -360 + current_angle
            elif movement_decision == "R":
                current_angle -= "SOMETHING"
                if current_angle <= -180:
                    current_angle = 360 + current_angle
            elif movement_decision == "F":
                # figure out x and y components of movement, and save to new_movement_component variable
                if 0 <= current_angle < 90:
                    x_component = movement_increment * math.cos(current_angle)
                    y_component = movement_increment * math.sin(current_angle)
                    new_movement_components = x_component, y_component
                elif 90 <= current_angle:
                    current_angle = current_angle - 90
                    x_component = -(movement_increment * math.sin(current_angle))
                    y_component = movement_increment * math.cos(current_angle)
                    new_movement_components = x_component, y_component
                elif 0 > current_angle >= -90:
                    x_component = movement_increment * math.cos(current_angle)
                    y_component = -(movement_increment * math.sin(current_angle))
                    new_movement_components = x_component, y_component
                elif -90 > current_angle:
                    current_angle = current_angle + 90
                    x_component = -(movement_increment * math.sin(current_angle))
                    y_component = -(movement_increment * math.cos(current_angle))
                    new_movement_components = x_component, y_component

                # update current coordinates with new movement
                current_coordinates = current_coordinates + new_movement_components
                # WRITE THIS TO DATABASE
                countID += 1
                item = {
                    'coordid': countID,
                    'datatype': 'D',
                    'coordinates': current_coordinates
                }
                table.put_item(Item=item)


        elif data_from_esp[0] == "L":
            dataparts = data_from_esp.split("|")
            mid, yellow_height, red_height, blue_height, yr_time, rb_time = dataparts
            # plug these variables into functions which convert to correct format, e.g. distance and angle
            dist_to_yellow = distance(yellow_height)
            dist_to_red = distance(red_height)
            dist_to_blue = distance(blue_height)
            yr_angle = timeToAngle(yr_time)
            rb_angle = timeToAngle(rb_time)
            # plug these newly formatted variables into the function which calculates coordinates using trig
            x, y = findCoordinates(yellow_height, red_height, blue_height, yr_angle, rb_angle)
            # WRITE THIS TO DATABASE
            countID += 1
            item = {
                'coordid': countID,
                'datatype': 'L',
                'coordinates': current_coordinates
            }
            table.put_item(Item=item)

    except:
        continue
