#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import PIL.Image
import PIL.ImageGrab
import time
import os
from Settings import *


"""
CLASS NAME:     ScreenshotTaker

PURPOSE:        To take screenshot from user
"""
class ScreenshotTaker(threading.Thread):
    _lastTime    = 0
    _currentTime = 0


    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Take screenshot from user
                    2. Save them
                    3. Continue the whole process from step 1 to step 2
    """
    def run(self):
        self._lastTime = time.time()

        os.chdir(REPORT_LOCATION)

        while RUN_SCREENSHOT_TAKER:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= SCREENSHOT_TAKER_INTERVAL:
                screenshot = PIL.ImageGrab.grab()
                screenshot.save("snapshot_" + time.strftime("%Y-%m-%d %H %M %S", time.localtime(time.time())) + SCREENSHOT_TAKER_IMAGE_FORMAT)

                self._lastTime = time.time()

            time.sleep(SCREENSHOT_TAKER_INTERVAL)