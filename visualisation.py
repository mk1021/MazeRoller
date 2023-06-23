# libraries
import turtle
import socket
import math
import cmath
import time

port = 5555
current_angle = 0
current_coordinates = 0, 0
movement_increment = 0.8

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
    # 4cm in metres
    realheight = 0.04

    D = (realheight * focal_length) / (pixels * pixel_width)
    return D


# Using Trigonometric Principles (like Sine Rule) to find other angles in the triangles
def findCoordinates(yellow_d, red_d, blue_d, yr_a, rb_a):
    # Using Sine Rule to find other necessary angles (why are these named like this?)
    angle_y = math.asin((red_d * math.sin(yr_a)) / 2.4)
    angle_r = math.asin((yellow_d * math.sin(yr_a)) / 2.4)
    angle_b = math.asin((red_d * math.sin(rb_a)) / 3.6)

    angle_x = 90 - angle_y
    angle_s = 90 - angle_r
    angle_a = 90 - angle_b

    # Using SOHCAHTOA to find x,y co-ordinates
    x_coordinate = yellow_d * math.sin(angle_x)
    y_coordinate = blue_d * math.sin(angle_a)

    return x_coordinate, y_coordinate


# --------------------------------------------------------------------------------------------------

# ------------------------------- V I S U A L I S A T I O N ----------------------------------------

def visualize_coordinates(coordinates):
    turtle.bgcolor('black')
    turtle.setup(2400, 3600)
    turtle.setworldcoordinates(0, 0, 240, 360)

    turtle.speed(0)
    turtle.penup()

    # Draw grid outline
    turtle.pencolor('white')
    turtle.pensize(2)
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.goto(240, 0)
    turtle.goto(240, 360)
    turtle.goto(0, 360)
    turtle.goto(0, 0)
    turtle.penup()

    prev_coordinate = None
    for coordinate in coordinates:
        if prev_coordinate is not None:
            x1, y1 = prev_coordinate
            x2, y2 = coordinate
            turtle.pencolor('red')
            turtle.goto(x1, y1)
            turtle.pendown()
            turtle.goto(x2, y2)

        turtle.pencolor('white')
        turtle.goto(coordinate)
        turtle.pendown()
        turtle.dot(3)

        prev_coordinate = coordinate

    turtle.penup()
    turtle.home()
    turtle.done()

# --------------------------------------------------------------------------------------------------

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
        client_connected = True
    except:
        print("failed to connect...")
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

                # scale the co-ordinates
                current_coordinates = (current_coordinates*1000)

                # send co-ordinates into visualisation function
                visualize_coordinates(current_coordinates)

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

            # send co-ordinates into visualisation function
            visualize_coordinates(current_coordinates)

            # scale the co-ordinates
            current_coordinates = (current_coordinates * 1000)

            # send co-ordinates into visualisation function
            visualize_coordinates(current_coordinates)

    except:
        continue
