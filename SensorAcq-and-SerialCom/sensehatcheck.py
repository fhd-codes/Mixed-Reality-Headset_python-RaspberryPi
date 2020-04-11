from sense_emu import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
while True:
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    print("y {0}\t p {1}\t r {2}".format( round(yaw,4), round(pitch,4), round(roll,4) ))
    sleep(1)