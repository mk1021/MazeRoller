#libraries
import socket
import cv2
import numpy as np


#STEP 0 - SETUP

port = 5555
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

reqnewframe = "Y"

#MAIN LOOP

while True:

    #STEP 1 - RECIEVE GRAYSCALE MAPPING FRAME

    foundFrame = False
    while found_frame == False:
        try:
            frame_data = rover.recv(1024)
            frame_data = frame_data.decode()
            found_frame = True
        except:
            continue

    #STEP 2 - DECODE FRAME AND CONVERT INTO BIRDS EYE VIEW

    #2a - perform any necessary decoding and conversions into a suitable file format


    #2b - perspective conversion using opencv
     
    frame = cv2.imread("nameofimagefile")


    #STEP 3 - DETECT WALLS AND PATHS AND TURN INTO A SET OF CHOICES

    #3a - detect walls and paths using opencv (findcontours)

    #3b - generate selection of next possible choices


    #STEP 4 - MAKE A CHOICE (EITHER RANDOMLY, OR SMARTLY)


    #STEP 5 - CONVERT CHOICE INTO A SET OF MOVEMENT ACTIONS BASED ON IRL DIMENSIONS OF BIRDS EYE VIEW IMAGE


    #STEP 6 - SEND MOVEMENT ACTIONS SEQUENTIALLY TO ROVER (could do this less exactly and instead combine with proximity sensor?)


    #STEP 7 - SEPERATELY CONVERT MOVEMENT ACTIONS INTO A PATH AND APPEND ONTO ROVER'S PATH SO FAR, STARTING FROM 'CUR START POS'


    #STEP 8 - SEND LOCATING REQUEST TO ROVER, WHO SPINS, PERFORMS LOCATION LOCALLY AND SENDS BACK COORDINATES

    #8a - send locating request to rover for latest starting position

    #8b - recieve coordinates into variable called lateststartingpos

    #STEP 9 - UPDATES CURRENT STARTING POSITION TO MINIMISE DEAD RECKONING ERROR AND KEEP BOTH THINGS CLOSELY TIED

    currentstartingpos = lateststartingpos