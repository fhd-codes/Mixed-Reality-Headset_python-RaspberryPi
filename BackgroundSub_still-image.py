'''
    Background subtraction technique on still images which are taken from webcam
    NOTE: do not change the position/angle of webcam while the code is running

'''

# imports
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
        break
    elif k == 115:  # s pressed
        background = frame
        print('frame captured')

'''
bkgnd = cv2.imread(background)
bkGnd = cv2.cvtColor(bkgnd, cv2.COLOR_BGR2RGB)
plt.imshow(bkGnd)
'''