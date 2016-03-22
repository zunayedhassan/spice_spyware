#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import time
import pyperclip
from CommonTools import *
from Settings import *


"""
CLASS NAME: ClipboardCopier

PURPOSE:    To keep an eye on clipboard continiously and save that content to a text file.
"""
class ClipboardCopier(threading.Thread):
    # Thread related settings
    _clipboardCheckingInterval = 1
    _lastTime                  = 0
    _currentTime               = 0
    _lastClipboardText         = ""

    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Check clipboard
                    2. If there is anything new, grab that text and save it to a file along with time
                    3. Continue the whole process from step 1 to step 2.
    """
    def run(self):
        self._lastTime = time.time()

        while RUN_CLIPBOARD_COPIER:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= self._clipboardCheckingInterval:
                currentContent = pyperclip.winGetClipboard()

                if (currentContent != self._lastClipboardText) and (currentContent != None):
                    SaveContent(CLIPBOARD_COPIER_FILE_NAME, "\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ":\n")
                    SaveContent(CLIPBOARD_COPIER_FILE_NAME, str(currentContent))
                    self._lastClipboardText = currentContent

                self._lastTime = time.time()

            time.sleep(self._clipboardCheckingInterval)
