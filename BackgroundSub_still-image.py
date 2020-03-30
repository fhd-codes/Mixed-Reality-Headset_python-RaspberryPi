'''
    Background subtraction technique on still images which are taken from webcam
    NOTE: do not change the position/angle of webcam while the code is running

'''

# imports
from functions import *



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

#   **********************************************************
#   This point needs changing (issue updated on github)
# taking absolute difference
diff = cv2.absdiff(fg , bg)
#   **********************************************************

# converting to greyscale and applying threshold
mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
th, mask_thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)

# applying filters
mask_blur = cv2.GaussianBlur(mask_thresh, (3, 3), 10)
plt.subplot(131)
plt.imshow(mask_blur)

dilate_img = cv2.dilate(mask_blur, np.ones((10,10), dtype=np.uint8), iterations=1)
plt.subplot(132)
plt.imshow(dilate_img)

mask_erosion = cv2.erode(dilate_img, np.ones((10,10), dtype=np.uint8), iterations=1)
plt.subplot(133)
plt.imshow(mask_erosion)
plt.show()


#   multiplying mask with the current frame 
mask_indexes = mask_erosion > 0

foreground = np.zeros_like(fg, dtype=np.uint8)
for i, row in enumerate(mask_indexes):
    foreground[i, row] = fg[i, row]


plt.imshow(foreground)
plt.show()