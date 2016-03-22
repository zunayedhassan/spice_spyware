#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import os
import sys
import time
from os.path import expanduser
from Settings import *
from pysqlite2 import dbapi2 as sqlite3
from CommonTools import *


"""
CLASS NAME:     MozillaFirefoxDigger

PURPOSE:        To get bookmarks and history from Mozilla Firefox
"""
class MozillaFirefoxDigger:
    """
    METHOD NAME:    DigMozillaFirefox
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Check if Mozilla Firefox folder exist
                    2. If so, then follow step 3 and 4, otherwise do nothing

                    3. For bookmarks:
                        (a) Open "places.sqlite" and search for url, title, time etc from  bookmarks
                        (b) Save them

                    4. For history:
                        (a) Open "places.sqlite" and search for url, title, time etc from  history
                        (b) Save them
    """
    def DigMozillaFirefox(self):
        firefoxProfileFolder = None

        # Check if Mozilla Firefox profile folder exists
        if os.path.exists(expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"):
            firefoxProfileFolder = expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\" + list(os.walk(expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"))[0][1][0] + "\\"

        # If profile folder exists then, search for Bookmarks and History
        if firefoxProfileFolder != None:
            # Bookmarks
            # Adding header
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n<-------[ MOZILLA FIREFOX BOOKMARKS ]------->\n")
            self.connection = None

            try:
                self.connection = sqlite3.connect(firefoxProfileFolder + "places.sqlite")
                cursor = self.connection.cursor()
                cursor.execute("SELECT moz_bookmarks.title, moz_places.url, moz_places.visit_count FROM moz_bookmarks, moz_places WHERE moz_bookmarks.fk = moz_places.id")
                data = cursor.fetchall()

                # Extracting page title, url, visits count and at the end add footer
                for info in data:
                    try:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "TITLE:\t\t\t" + str(info[0]))

                    except UnicodeError as error:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "TITLE:\t\t\tNone")

                    finally:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nURL:\t\t\t" + str(info[1]) + "\nVISITS COUNT:\t" + str(info[2]) + "\n----------------------------------------------------\n")

            except sqlite3.Error as error:
                sys.exit(1)

            finally:
                self.connection.close()

            # History
            # Adding header
            SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\n\n<-------[ MOZILLA FIREFOX HISTORY ]------->\n")

            try:
                connection = sqlite3.connect(firefoxProfileFolder + "places.sqlite")
                cursor = connection.cursor()
                cursor.execute("SELECT moz_places.title, moz_places.url, moz_historyvisits.visit_date, moz_places.visit_count FROM moz_places, moz_historyvisits WHERE moz_historyvisits.place_id = moz_places.id ORDER BY moz_historyvisits.visit_date")
                data = cursor.fetchall()

                # Extracting history and saving them
                for info in data:
                    try:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "TITLE:\t\t\t" + str(info[0]))

                    except UnicodeError as error:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "TITLE:\t\t\tNone")

                    finally:
                        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "\nURL:\t\t\t" + str(info[1]) + "\nVISIT DATE:\t\t" + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(float(info[2] / 1000000))) + "\nVISIT COUNT:\t" + str(info[3]) + "\n----------------------------------------------------\n")

            except sqlite3.Error as error:
                sys.exit(1)

            finally:
                connection.close()