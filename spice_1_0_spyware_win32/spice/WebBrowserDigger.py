#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import time
from MozillaFirefoxDigger import *
from OperaDigger import *
from GoogleChromeDigger import *
from Settings import *


"""
CLASS NAME:     WebBrowserDigger

PURPOSE:        To get bookmarks and history from Mozilla Firefox, Opera and Google Chrome
"""
class WebBrowserDigger(threading.Thread):
    _lastTime = 0
    _currentTime = 0

    mozillaFirefoxDigger = MozillaFirefoxDigger()
    googleChromeDigger = GoogleChromeDigger()
    operaDigger = OperaDigger()


    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Call getEverythingFromWebBrowser
                    2. Continue the whole process regularly
    """
    def run(self):
        self._lastTime =time.time()

        self.getEverythingFromWebBrowser()

        while RUN_WEB_BROWSER_DIGGER:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= WEB_BROWSER_DIGGER_INTERVAL:
                self.getEverythingFromWebBrowser()
                self._lastTime = time.time()

            time.sleep(WEB_BROWSER_DIGGER_INTERVAL)


    """
    METHOD NAME:    getEverythingFromWebBrowser
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Call Mozilla Firefox Digger
                    2. Call Opera Digger
                    3. Call Google Chrome Digger
    """
    def getEverythingFromWebBrowser(self):
        SaveContent(WEB_BROWSER_DIGGER_FILE_NAME, "", FileMode["WRITE"])

        self.mozillaFirefoxDigger.DigMozillaFirefox()
        self.googleChromeDigger.DigGoogleChrome()
        self.operaDigger.DigOpera()