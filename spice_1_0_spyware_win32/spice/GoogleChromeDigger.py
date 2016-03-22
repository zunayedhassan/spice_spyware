#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import os
import sys
import time
import shutil
from os.path import expanduser
from pysqlite2 import dbapi2 as sqlite3
from CommonTools import *
from Settings import *


"""
CLASS NAME:     GoogleChromeDigger

PURPOSE:        To find out browser history and bookmarks from Google Chrome
"""
class GoogleChromeDigger:
    """
    METHOD NAME:    DigGoogleChrome
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        To find out browser history and bookmarks from Google Chrome

    ALGORITHM:      1. Check if Google Chrome folder exists
                    2. If so, then follow step 3 and 4, otherwise do nothing

                    3. For Bookmarks:
                        (a) Open "Bookmarks" file from Google Chrome folder
                        (b) Read lines from that file.
                        (c) From every line, separate page title, url, visiting time
                        (d) Save required field which are extracted from every lines of "Bookmarks" file

                    4. For History:
                        (a) Check if google chrome browser folders' existence
                        (b) If exists, copy "History" folder to a separate location
                        (c) Open "History" file from that location and search for url, title and visiting time.
                        (d) Convert those filed to string
                        (e) Save them
    """
    def DigGoogleChrome(self):
        googleChromeProfileFolder = expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"

        # Checking about Google Chrome folders' existence
        if os.path.exists(googleChromeProfileFolder):
            # Bookmark
            # Writing header for bookmark
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n<------[ GOOGLE CHROME BOOKMARK ]------>\n")
            googleChromeBookmarkFile = open(googleChromeProfileFolder + "Bookmarks")
            lines = googleChromeBookmarkFile.readlines()
            googleChromeBookmarkFile.close()

            # Extracting line for filtering page title, url, date added etc
            for line in lines:
                if "\"name\":" in line:
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nTITLE:\t\t\t" + ((line.split(":", 1))[1].split("\""))[1])

                elif "\"url\":" in line:
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nURL:\t\t\t" + ((line.split(":", 1))[1].split("\""))[1])

                elif "\"date_added\":" in line:
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n--------------------------------------------")
                    dateAdded = float((((line.split(":", 1))[1]).split("\""))[1]) / 1000000
                    dateAddedSplitted = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dateAdded))).split("-", 1)
                    SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nDATE ADDED:\t\t" + str(int(dateAddedSplitted[0]) - 369) + "-" + dateAddedSplitted[1])

            # Adding footer
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "--------------------------------------------")


            # History
            # Copying "History" file to a separate location. Because, in case Google Chrome browser is already open
            # then the system won't allow to access "History" file.
            shutil.copy(googleChromeProfileFolder + "History", AGENT_LOCATION + "\\History")

            # Adding header
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n\n<------[ GOOGLE CHROME HISTORY ]------>\n")

            connection = None
            lastVisitTime = ""
            lastVisitTimeSplitted = ""


            try:
                # Opening "History" file from a separate location, not from Google Chrome folder
                connection = sqlite3.connect(AGENT_LOCATION + "History")
                cursor = connection.cursor()
                cursor.execute("SELECT urls.title, urls.url, urls.visit_count, urls.last_visit_time FROM urls")
                data = cursor.fetchall()

                # Extracting page title, url, visit count, time etc
                for info in data:
                    try:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nTITLE:\t\t\t\t" + str(info[0]))

                    except UnicodeError as error:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nTITLE:")

                    finally:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nURL:\t\t\t\t" + str(info[1]))
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nVISIT COUNT:\t\t" + str(info[2]))

                        lastVisitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(info[3] / 1000000)))
                        lastVisitTimeSplitted = lastVisitTime.split("-", 1)

                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nLAST VISIT TIME:\t" + str(int(lastVisitTimeSplitted[0]) - 369) + "-" + lastVisitTimeSplitted[1])

                        # Adding footer
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n----------------------------------------------------\n")

            except sqlite3.Error as error:
                sys.exit(1)

            finally:
                connection.close()