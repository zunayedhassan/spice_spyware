#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import os
import time


"""
CLASS NAME:     FolderContent

PURPOSE:        To get the list of subdirectories and files from given path
"""
class FolderContent:
    def __init__(self):
        self.FileOrFolderName = None
        self.Type             = "       "
        self.Size             = ""
        self.Created          = ""
        self.Modified         = ""
        self.Accessed         = ""


    """
    METHOD NAME:    GetDirectoryContent
    PARAMETER:      (string) currentPath
    RETURN:         (string) result

    PURPOSE:    To get the list of subdirectories and files from given path
    """
    def GetDirectoryContent(self, currentPath):
        currentPath += "\\"
        directoryContentList = []

        result = ""

        # If given path is actually exist and is a directory (not file)
        if os.path.exists(currentPath) and os.path.isdir(currentPath):
            # Adding header, like Name, Type, Size, Created, Modified, Accessed
            folderContent = FolderContent()
            folderContent.FileOrFolderName = "NAME"
            folderContent.Type = "TYPE"
            folderContent.Size = "SIZE"
            folderContent.Created = "CREATED\t\t\t"
            folderContent.Modified = "MODIFIED\t\t"
            folderContent.Accessed = "ACCESSED"

            directoryContentList.append(folderContent)

            # For every file or folder name from the list, create a folder content class that can store name, type, size
            # date etc.
            for content in os.listdir(currentPath):
                currentFolderContent = FolderContent()
                currentFolderContent.FileOrFolderName = content

                # Checking if the current content is file or folder
                if os.path.isfile(currentPath + content):
                    currentFolderContent.Size = str(round(os.path.getsize(currentPath + content) / 1024.00, 2)) + " KB"
                else:
                    currentFolderContent.Type = "< DIR >"

                # Converting date (float) to string format
                try:
                    currentFolderContent.Created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(currentPath + content)))
                except WindowsError:
                    currentFolderContent.Created = ""

                try:
                    currentFolderContent.Modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(currentPath + content)))
                except WindowsError:
                    currentFolderContent.Modified = ""

                try:
                    currentFolderContent.Accessed = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getatime(currentPath + content)))
                except WindowsError:
                    currentFolderContent.Accessed = ""

                # Adding current content to directoryList
                directoryContentList.append(currentFolderContent)

        # Otherwise the whole path is invalid
        else:
            result = "[!] WARNING:\t\"" + currentPath + "\" doesn't exist."


        # We want to arrange file/folder name and their other properties on every row and column. So, to do that, first
        # we need to identify which file name and size length are long to get an idea of maximum space for every column
        longestFileOrFolderNameLength = 0
        longestSizeLength = 0

        for content in directoryContentList:
            if len(content.FileOrFolderName) > longestFileOrFolderNameLength:
                longestFileOrFolderNameLength = len(content.FileOrFolderName)

            if len(content.Size) > longestSizeLength:
                longestSizeLength = len(content.Size)

        # If directory list is not empty then, first show the path of that directory.
        if len(directoryContentList) > 1:
            result = ("PATH:\t" + currentPath + "\n\n")

        # Giving space (" ") for every column to arrange content nicely
        for content in directoryContentList:
            if len(content.FileOrFolderName) < longestFileOrFolderNameLength:
                for i in range(longestFileOrFolderNameLength - len(content.FileOrFolderName)):
                    content.FileOrFolderName += " "

            if len(content.Size) < longestSizeLength:
                for i in range(longestSizeLength - len(content.Size)):
                    content.Size += " "

            # Saving every folder content to a string
            result += (str(content) + "\n")

        return result

    def __str__(self):
        return self.FileOrFolderName + "\t" + self.Type + "\t" + self.Size + "\t" + self.Created + "\t\t" + self.Modified + "\t\t" + self.Accessed

