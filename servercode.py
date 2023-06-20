import socket
import boto3
from boto3.dynamodb.conditions import Key
import math
import cmath
import time

# ---------------------------- S E R V E R   &   D A T A B A S E   C O D E ----------------------------------------

def write_to_database(data_type):
    # Write to database with the specified data type and current timestamp
    timestamp = datetime.now().isoformat()
    item = {'Movement Instruction': data_type, 'timestamp': timestamp}
    table.put_item(Item=item)


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    primary_key = 'timestamp'

    # Create the DynamoDB table
    table = dynamodb.create_table(
        TableName='MazeRoverData',
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'data_type',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            # the table can handle upto 5 read and writes per second
            'ReadCapacityUnits': 5,
            # represents the desired capacity for read operations
            'WriteCapacityUnits': 5
            # represents the desired capacity for write operations
        }

        # do we need a GSI
        # GSI = useful for enabling efficient querying of data based on attributes other than primary key
    )
    return table


print("We're in tcp server...")
server_port = 12000

welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_socket.bind(('0.0.0.0', server_port))
welcome_socket.listen(1)

print('Server running on port', server_port)

# Connect to the DynamoDB service
dynamodb = session.resource('dynamodb', region_name='us-east-1')

# Specify and get the DynamoDB table
table = dynamodb.Table('MazeRoverData')
create_table(dynamodb)  # is this how i call this function?

while True:
    # Check for data
    if check_for_data():
        # Retrieve the data
        data = get_data()

        # Check data type

        # MOVEMENT INSTRUCTIONS
        if data[0] == "M":
            # Write to database
            if data[1] ==
            write_to_database(data[0])

        if data[0] == "L":
            # Write to database
            write_to_database(data[0])

        if data[0] == "F":
            # Write to database
            write_to_database(data[0])

        # LOCALISATION
        elif data[0] == "L":

            # Call localization functions
            coordinates = call_localization_functions()

            # Write coordinates to the database
            table.put_item(Item={
                'coordinates': coordinates
            })


#---------------------------------------------------------------------------------------------------------------




# ------------------------- L O C A L I S A T I O N    F U N C T I O N S ---------------------------------------

# Using FPGA to calulcate the centre angles between beacons
def usingfpga(timetaken, totaltime):
    degrees = (timetaken / totaltime) * 360
    angle = degrees * (math.pi/180)
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
def usingtrig(yr, rb):

    # Calculate angles at centre between beacons based on timings sent
    angle_yor = usingfpga(t1, total)
    angle_rob = usingfpga(t2, total)

    # Calculate distances from rover to each beacon based on pixels
    dy = distance(yellowpixels)
    dr = distance(redpixels)
    db = distance(bluepixels)

    # Using Sine Rule to find other necessary angles
    angle_y = math.asin((dr*math.sin(angle_yor)) / yr)
    angle_r = math.asin((dy*math.sin(angle_yor)) / yr)
    angle_b = math.asin((dr * math.sin(angle_rob)) / rb)

    angle_x = 90 - angle_y
    angle_s = 90 - angle_r
    angle_a = 90 - angle_b

    # Using SOHCAHTOA to find x,y co-ordinates
    x_coordinate = dy*math.sin(angle_x)
    y_coordinate = db*math.sin(angle_a)

    return x_coordinate, y_coordinate

# --------------------------------------------------------------------------------------------------