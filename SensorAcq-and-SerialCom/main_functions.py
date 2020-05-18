import sys
sys.path.insert(1,'/home/pi/GY-85_Raspberry-Pi/i2clibraries')
from i2c_adxl345 import *
from i2c_itg3205 import *

sys.path.insert(1,'/home/pi/py-qmc5883l')
from py_qmc5883l import *

import time
import math
from math import *

adxl345 = i2c_adxl345(1)
itg3205 = i2c_itg3205(1)
qmc5883 = QMC5883L(1)

gyro_scale = 131.0
accel_scale = 16384.0

K = 0.98 # hpv lpv values
K1 = 1 - K
time_diff = 0.1

declination = 0.036  #2.0667 # 2 degrees and 4 mins
pi = 3.14159265359


    
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
    
def Acc_scaled():
    accRaw = adxl345.Acc_rawData()
    
    acc_x = twos_compliment((accRaw[0] << 8) + accRaw[1]) / accel_scale
    acc_y = twos_compliment((accRaw[2] << 8) + accRaw[3]) / accel_scale
    acc_z = twos_compliment((accRaw[4] << 8) + accRaw[5]) / accel_scale
    
    return (acc_x, acc_y, acc_z)

def Gyro_scaled():
    gyroRaw = itg3205.Gyro_rawData()
    
    gyro_x = twos_compliment((gyroRaw[0] << 8) + gyroRaw[1]) / gyro_scale
    gyro_y = twos_compliment((gyroRaw[2] << 8) + gyroRaw[3]) / gyro_scale
    gyro_z = twos_compliment((gyroRaw[4] << 8) + gyroRaw[5]) / gyro_scale

    return (gyro_x, gyro_x, gyro_x)


# -----------------------------------------------------------------------------
def dist(a, b):
    return math.sqrt((a * a) + (b * b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def get_RollPitch():
    now = time.time()

    # calculating offsets for adxl and itg
    (Ax, Ay, Az) = Acc_scaled()
    (Gx, Gy, Gz) = Gyro_scaled()


    last_x = get_x_rotation(Ax, Ay, Az)
    last_y = get_y_rotation(Ax, Ay, Az)

    gyro_offset_x = Gx
    gyro_offset_y = Gy

    gyro_total_x = (last_x) - gyro_offset_x
    gyro_total_y = (last_y) - gyro_offset_y


    time.sleep(time_diff - 0.005)
    
    # reading all data
    (Ax, Ay, Az) = Acc_scaled()
    (Gx, Gy, Gz) = Gyro_scaled()
    
    # adjusting offset from gyro data
    Gx -= gyro_offset_x
    Gy -= gyro_offset_y
    
    # calculating how much sensor has rotated since the last taken sample
    gyro_x_delta = (Gx * time_diff)
    gyro_y_delta = (Gy * time_diff)
    
    # adding the delta change in the total
    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    # reading rotation data from adxl sensor
    rotation_x = get_x_rotation(Ax, Ay, Az)
    rotation_y = get_y_rotation(Ax, Ay, Az)
    
    # implementing complementary filter
    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
    
    roll = rotation_x
    pitch = rotation_y
    
    return roll, pitch    
    
    
def Mag_rawData():
    
    xMag, yMag, zMag = qmc5883.get_magnet_raw()
    return xMag, yMag, zMag
    
    
def get_yaw():
    
    R, P = get_RollPitch() # used in tilt compenstation
    
    x, y, z = Mag_rawData()
    R = -R
    
    Xh = x*cos(P *pi/180) + y*sin(R *pi/180)*sin(P *pi/180) + z*cos(R *pi/180)*sin(P *pi/180)
    Yh = y*cos(R *pi/180) + z*sin(R *pi/180)
    
    heading = atan2(-Yh, Xh) + declination
    
    if(heading > 2*pi):
        heading = heading - 2*pi
        
    if(heading < 0):
        heading = heading + 2*pi
    
    # converting to angle    
    heading_angle = int(heading*180/pi)
    
    return heading_angle



'''    
 
            Xh = ( x*cos(P*(pi/180)) + z*sin(P*(pi/180)) )
    
    Yh = ( x*sin(R*(pi/180))*cos(P*(pi/180)) + y*cos(R*(pi/180)) -
           z*sin(R*(pi/180))*cos(P*(pi/180)) )
           
           '''
