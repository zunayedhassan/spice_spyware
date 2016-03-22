#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

from AESCipher import *


if __name__ == "__main__":
    print("\nSPICE REPORT DECRYPTER")
    print("----------------------\n")
    reportPath = raw_input("-> Please type a path:\t")
    saveLocation = raw_input("-> Save location:\t")

    encryptedFile = open(reportPath, "rb")
    key = encryptedFile.read()
    encryptedFile.close()
    reportDecrypted = (AESCipher("black_flag")).Decrypt(key)

    unlockedReportFile = open(saveLocation, "w")
    unlockedReportFile.write(reportDecrypted)
    unlockedReportFile.close()

    print("[i] MESSAGE: Report saved at " + saveLocation)
