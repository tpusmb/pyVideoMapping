#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2
import imutils
import numpy as np
import screeninfo
from screeninfo import Monitor
from .screen_relation import ScreenRelation


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

TEST_IMAGE = os.path.join(FOLDER_ABSOLUTE_PATH, "test_image.jpg")


class PyVideoMapping:
    def __init__(self, screen, ui_screen: Monitor = None):
        self.screen = screen
        self.ui_screen = ui_screen
        self.screen_relation = None
        self.wall_paper = self.creat_blank_image()
        self.test_image = cv2.imread(TEST_IMAGE)

        if self.ui_screen is not None:
            self.screen_relation = ScreenRelation(ui_screen, self.scree)

    @staticmethod
    def get_image_size(frame):
        """

        :param frame:
        :return: (tuple) height, width
        """
        return frame.shape

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

    def change_ui_screen(self, ui_screen : Monitor):
        self.ui_screen = ui_screen
        self.screen_relation = ScreenRelation(self.ui_screen, self.scree)

    def creat_blank_image(self):
        return np.zeros((self.screen.height, self.screen.width, 3), np.uint8)

    def show_to_projector(self, frame, blocking=True):
        window_name = 'projector'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, self.screen.x - 1, self.screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        if blocking:
            cv2.waitKey()
            cv2.destroyAllWindows()
        else:
            cv2.waitKey(1)

    def mapping_calibration(self, ui_images):
        """

        :param ui_images: (list) All test image to display into the projector
                                    Image 1
            [ [ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left], ... ]
        :return:
        """
        if self.screen_relation is None:
            raise ValueError("Need to provide ui screen in the constructor")
        h, w = self.get_image_size(self.test_image)
        output_frame = self.wall_paper.copy()
        # Get all image tuple (tuple) x, y
        for ui_top_left, ui_top_right, ui_bottom_right, ui_bottom_left in ui_images:
            projector_top_left = self.screen_relation.to_projector_screen(*ui_top_left)
            projector_top_right = self.screen_relation.to_projector_screen(*ui_top_right)
            projector_bottom_right = self.screen_relation.to_projector_screen(*ui_bottom_right)
            projector_bottom_left = self.screen_relation.to_projector_screen(*ui_bottom_left)

            new_width = max(abs(projector_top_left[0] - projector_top_right[0]),
                            abs(projector_bottom_left[0] - projector_bottom_right[0]))
            new_height = max(abs(projector_top_left[1] - projector_bottom_left[1]),
                             abs(projector_top_right[1] - projector_bottom_right[1]))
            wrap = self.transform_image(self.test_image, projector_bottom_left, projector_bottom_right,
                                        projector_bottom_right, projector_bottom_left,
                                        new_width, new_height)

            output_frame = self.add_sub_image(output_frame, wrap, *projector_top_left)

        self.show_to_projector(output_frame, blocking=False)
