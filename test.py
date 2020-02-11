import cv2
import numpy as np

"""
# now that we have the dimensions of the new image, construct
# the set of destination points to obtain a "birds eye view",
# (i.e. top-down view) of the image, again specifying points
# in the top-left, top-right, bottom-right, and bottom-left
# order

# compute the perspective transform matrix and then apply it

"""


def show_full_frame(frame):
    """
    Given a frame, display the image in full screen
    :param frame: image to display full screen
    """
    cv2.namedWindow('Full Screen', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Full Screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Full Screen', frame)


img = cv2.imread("square.png")

h, w, _ = img.shape

print(w, " ", h)

# Y, x
dst = np.array([
    [0, 0],  # Top left
    [10, 0],  # Top right
    [40, 15],  # Bottom right
    [10, 20]], dtype="float32")  # Bottom left

rect = np.array([
    [0, 0],
    [w - 1, 0],
    [w - 1, h - 1],
    [0, h - 1]], dtype="float32")

M = cv2.getPerspectiveTransform(rect, dst)
warped = cv2.warpPerspective(img, M, (w, h))

show_full_frame(img)
cv2.waitKey(0)
