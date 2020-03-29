'''
    Background subtraction technique on still images which are taken from webcam
    NOTE: do not change the position/angle of webcam while the code is running

'''

# imports
from functions import *
import cv2
import matplotlib.pyplot as plt


video = cv2.VideoCapture(0)

while True:

    success, frame = video.read()
    if not success:
        # Frame not successfully read from video capture
        break

    # Display result
    cv2.imshow("frame", frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:  # escape pressed
        cv2.imwrite('background.jpg',bg)
        cv2.imwrite('foreground.jpg', fg)
        break
    elif k == 98:  # b pressed
        bg = frame
        print('background captured')
    elif k == 102:  # f pressed
        fg = frame
        print('foreground captured')

# taking absolute difference
diff = cv2.absdiff(fg , bg)

diff = bgrtorgb(diff)   # just to use plt
plt.imshow(diff)
plt.show()