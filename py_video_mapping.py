#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2
import imutils
import numpy as np
import screeninfo
from imutils.perspective import four_point_transform

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/py_video_mapping.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class PyVideoMapping:
    def __init__(self, screen):
        self.screen = screen

    @staticmethod
    def get_all_screens():
        return screeninfo.get_monitors()

    @staticmethod
    def resize(frame, width, height):
        return imutils.resize(frame, width=width, height=height)

    @staticmethod
    def add_sub_image(wall_paper, frame, x_offset, y_offset):
        wall_paper_copy = wall_paper.copy()
        wall_paper_copy[y_offset:y_offset + frame.shape[0], x_offset:x_offset + frame.shape[1]] = frame
        return wall_paper_copy

    @staticmethod
    def transform_image(frame, top_left, top_right, bottom_right, bottom_left, output_width, output_height):
        """

        :param frame:
        :param top_left: (tuple) x, y
        :param top_right: (tuple) x, y
        :param bottom_right: (tuple) x, y
        :param bottom_left: (tuple) x, y
        :param output_width:
        :param output_height:
        :return:
        """
        h, w, _ = frame.shape
        rect = np.array([
            [0, 0],
            [w - 1, 0],
            [w - 1, h - 1],
            [0, h - 1]], dtype="float32")

        dst = np.array([
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, M, (output_width, output_height))
        return warped

    def creat_blank_image(self):
        return np.zeros((self.screen.height, self.screen.width, 3), np.uint8)

    def show_to_projector(self, frame):
        window_name = 'projector'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        cv2.waitKey()
        cv2.destroyAllWindows()
