#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import time
import os
import threading
import smtplib
from email.mime.multipart import *
from email.utils import *
from email.utils import COMMASPACE
from email.mime.text import *
from email.mime.base import *
from email.encoders import *
from Settings import *


"""
CLASS NAME:     SendEmail

PURPOSE:        To send email. If email can't be sent successfully, then keep sending until it is successful
"""
class SendEmail(threading.Thread):
    # Email related properties
    SendFrom = ""
    Password = ""
    SendTo   = []
    Subject  = ""
    Text     = ""
    Files    = []
    Server   = "localhost"

    # Threading related properties
    _lastTime = 0
    _currentTime = 0
    _emailSendingFailed = True

    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Send email
                    2. If sending email is not successful, then keep sending again. Stop otherwise, if successful.
    """
    def run(self):
        self._lastTime = time.time()

        while self._emailSendingFailed:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= EMAIL_SENDING_INTERVAL:
                self._emailSendingFailed = not self.SendEmail()
                self._lastTime = time.time()

            time.sleep(EMAIL_SENDING_INTERVAL)


    """
    METHOD NAME:    SendEmail
    PARAMETER:      None
    RETURN:         Boolean

    PURPOSE:        To send email according to its email related properties
    """
    def SendEmail(self):
        assert type(self.SendTo) == list
        assert type(self.Files) == list

        msg = MIMEMultipart()
        msg['From'] = self.SendFrom
        msg['To'] = COMMASPACE.join(self.SendTo)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.Subject

        msg.attach(MIMEText(self.Text))

        if self.Files != []:
            for f in self.Files:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(f, "rb").read())
                encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)

        smtp = smtplib.SMTP(self.Server)
        smtp.starttls()
        smtp.login(self.SendFrom, self.Password)
        problem = smtp.sendmail(self.SendFrom, self.SendTo, msg.as_string())
        smtp.close()

        if problem == {}:
            return True

        return False