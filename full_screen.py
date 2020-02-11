import numpy as np
import cv2
import screeninfo
import imutils


def show_to_projector(frame, screen):

    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, frame)
    cv2.waitKey()
    cv2.destroyAllWindows()


def resize(frame, width, height):
    """

    :param frame:
    :param width:
    :param height:
    :return:
    """
    return imutils.resize(frame, width=width, height=height)


def creat_blank_image(screen):

    return np.zeros((screen.height, screen.width, 3), np.uint8)


def add_image(wall_paper, frame, x_offset, y_offset):

    wall_paper[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
    return wall_paper


if __name__ == '__main__':
    screen_id = 1
    is_color = True

    screen = screeninfo.get_monitors()[screen_id]
    wall_paper = creat_blank_image(screen)
    image = cv2.imread("square.png")
    small = resize(image, 10, 20)
    wall_paper = add_image(wall_paper, image, 200, 300)
    show_to_projector(wall_paper, screen)
