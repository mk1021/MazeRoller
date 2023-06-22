import math

# Using FPGA to calulcate the centre angles between beacons
def timeToAngle(timetaken):
    degrees = (timetaken / "REPLACE WITH CONSTANT") * 360
    angle = degrees * (math.pi / 180)
    return angle

def triangulate_coords(angle_yr, angle_rb):
    prev_heading = 0
    coord = [0, 0]
    print("hi")

# ----------------- F O R   F I X E D   V A L U E S   O F   α / β --------------------
# ---- these are functions that draw the upper and right semicircles on the graph ----

def upper_semicircle_fixed_alpha(mapwidth, maplength, theta, alpha):
    mapwidth = 2.4         # not exact but will be edited
    maplength = 3.6         # not exact but will be edited

    discriminant = ((maplength/(2*math.tan(theta)))**2)-alpha(alpha-maplength)
    square_root = math.sqrt(discriminant)
    beta = mapwidth - (maplength/(2*math.tan(theta))) - square_root
    return beta

def right_semicircle_fixed_beta(mapwidth, maplength, phi, beta):
    mapwidth = 2.4         # not exact but will be edited
    maplength = 3.6         # not exact but will be edited

    discriminant = ((mapwidth/(2*math.tan(phi)))**2)-beta(beta-maplength)
    square_root = math.sqrt(discriminant)
    alpha = maplength - (mapwidth/(2*math.tan(phi))) - square_root
    return alpha


# ------------ F I N D I N G   E Q U A T I O N S  I N   T E R M S   O F   X -----------

def tangent_m1(alpha, beta, mapwidth, maplength):
    m1 = (beta - mapwidth)/alpha
    return m1

def tangent_m2(alpha, beta, mapwidth, maplength):
    m2 = (beta - mapwidth)/(alpha - maplength)
    return m2

def tangent_m3(alpha, beta, mapwidth, maplength):
    m3 = beta/(alpha-maplength)
    return m3

def upper_semicircle_in_terms_of_alpha(mapwidth, maplength, alpha, phi):

    discriminant = ((mapwidth/4)**2)-((alpha-maplength)**2)
    beta = 
    return beta



if __name__ == '__main__':
    angle_yr = timeToAngle(data[0])
    angle_rb = timeToAngle(data[1])


# if value is larger than mapwidth/2 

# in order to calculcate where it hits the edge, just do 0