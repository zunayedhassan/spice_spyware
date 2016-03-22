#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'


import threading
import os
import time
from CommonTools import *
from Settings import *
from os.path import expanduser


"""
CLASS NAME:     OperaDigger

PURPOSE:        To find out Bookmarks and History from Opera browser
"""
class OperaDigger(threading.Thread):
    """
    METHOD NAME:    DigOpera
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Check if opera profile folder exists
                    2. If so, then follow step 3 and 4, otherwise do nothing

                    3. For bookmarks:
                        (a) Open "bookmarks.adr" file
                        (b) Read every line
                        (c) From every line, extract bookmarks
                        (d) Save them all

                    4. For history:
                        (a) Open "global_history.dat"
                        (b) Read every line
                        (c) From every line, extract history
                        (d) Save them all
    """
    def DigOpera(self):
        operaProfileDirectory = expanduser("~") + "\\AppData\\Roaming\\Opera\\Opera\\"

        # Checking if Opera profile folder exists
        if os.path.exists(operaProfileDirectory):
            # Bookmark
            # Adding header
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n<-------[ OPERA BOOKMARK ]------->\n")
            operaBookmarkFile = open(operaProfileDirectory + "bookmarks.adr", "r")
            lines = operaBookmarkFile.readlines()
            operaBookmarkFile.close()

            # Extracting bookmarks and saving them all
            for line in lines:
                if "CREATED=" in line:
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n\tCREATED=" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(line.split("CREATED=")[1]))) + "\n")
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n------------------------------------------\n")

                elif (("NAME=" in line) or ("URL=" in line)) and (line != "\n"):
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n" + line)

            # History
            # Adding header
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n\n\n<-------[ OPERA HISTORY ]------->\n")
            operaHistoryFile = open(operaProfileDirectory + "global_history.dat", "r")
            lines = operaHistoryFile.readlines()
            operaHistoryFile.close()

            # Extracting history and saving them all
            for line in lines:
                if (line.split("\n")[0]).isdigit() and (len(line) >= 9):
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME,  "\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int((line.split("\n"))[0]))))

                elif (not (line.split("\n")[0]).isdigit()) and (line != "-1\n"):
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n" + (line.split("\n"))[0])