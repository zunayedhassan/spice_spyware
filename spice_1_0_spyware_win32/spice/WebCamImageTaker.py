#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import cv
import time
import threading
import numpy
from Settings import *


"""
CLASS NAME:     WebCamImageTaker

PURPOSE:        To take image from webcam
"""
class WebCamImageTaker(threading.Thread):
    _lastTime    = 0
    _currentTime = 0


    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Take an image from webcam
                    2. Keep continue
    """
    def run(self):
        self._lastTime = time.time()

        while RUN_WEBCAM_IMAGE_TAKER:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= WEBCAM_IMAGE_TAKING_INTERVAL:
                self.takeImage()
                self._lastTime = time.time()

            time.sleep(WEBCAM_IMAGE_TAKING_INTERVAL)

    """
    METHOD NAME: takeImage
    PARAMETER:   None
    RETURN:      None

    PURPOSE:     1. Take image from webcam
                 2. Save that
    """
    def takeImage(self):
        cameraCapture = cv.CreateCameraCapture(0)
        image = cv.QueryFrame(cameraCapture)
        cv.SaveImage(AGENT_LOCATION + "Report\\" + "webcam_image_" + time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time())) + WEBCAM_IMAGE_TAKER_IMAGE_FORMAT, image)