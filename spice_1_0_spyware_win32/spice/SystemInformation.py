#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import sys
import ctypes
import _winreg
import threading
from Settings import *
from CommonTools import *


"""
CLASS NAME:     SystemInformation

PURPOSE:        To get system information from user and save them to a file
"""
class SystemInformation(threading.Thread):
    def run(self):
        # Gathering system information
        self.OS = self.getOSVersion()
        self.CPU = self.getCPU()
        self.TotalRAM, self.AvailableRAM = self.getRAM()
        self.TotalRAM = self.TotalRAM / (1024*1024)
        self.AvailableRAM = self.AvailableRAM / (1024*1024)
        self.IEVersion = self.getInternetExplorerVersion()

        # Saving to a file
        if RUN_SYSTEM_INFORMATION:
            SaveContent(SYSTEM_INFORMATION_FILE_NAME, "Operation System:\t" + self.OS + "\nCPU:\t\t\t\t" + self.CPU + "\nTotal RAM:\t\t\t" + str(self.TotalRAM) + " MB\nAvailable RAM:\t\t" + str(self.AvailableRAM) + " MB\nInternet Explorer:\t" + self.IEVersion, FileMode["WRITE"])


    """
    METHOD NAME:    getRegistryValue
    PARAMETER:      (string) key, (string) subkey, (string) value
    RETURN:         (string) value

    PURPOSE:        To get registry information from Windows
    """
    def getRegistryValue(self, key, subkey, value):
        if sys.platform != "win32":
            raise OSError("get_registry_value is only supported on Windows")

        key = getattr(_winreg, key)
        handle = _winreg.OpenKey(key, subkey)
        (value, type) = _winreg.QueryValueEx(handle, value)

        return value


    """
    METHOD NAME:    getOSVersion
    PARAMETER:      None
    RETURN:         string

    PURPOSE:        Get information about operating system
    """
    def getOSVersion(self):
        osProductName = self.getRegistryValue("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductName")
        osBuildNumber = self.getRegistryValue("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "CurrentBuildNumber")

        return "%s (build %s)" % (osProductName, osBuildNumber)


    """
    METHOD NAME:    getCPU
    PARAMETER:      None
    RETURN:         string

    PURPOSE:        Get information about CPU
    """
    def getCPU(self):
        return self.getRegistryValue("HKEY_LOCAL_MACHINE", "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0", "ProcessorNameString")


    """
    METHOD NAME:    getRAM
    PARAMETER:      None
    RETURN:         string

    PURPOSE:        Get information about RAM
    """
    def getRAM(self):
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong

        class MemoryStatus(ctypes.Structure):
            _fields_ = [
                ('dwLength', c_ulong),
                ('dwMemoryLoad', c_ulong),
                ('dwTotalPhys', c_ulong),
                ('dwAvailPhys', c_ulong),
                ('dwTotalPageFile', c_ulong),
                ('dwAvailPageFile', c_ulong),
                ('dwTotalVirtual', c_ulong),
                ('dwAvailVirtual', c_ulong)
            ]

        memoryStatus = MemoryStatus()
        memoryStatus.dwLength = ctypes.sizeof(MemoryStatus)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))

        return (memoryStatus.dwTotalPhys, memoryStatus.dwAvailPhys)


    """
    METHOD NAME:    getInternetExplorerVersion
    PARAMETER:      None
    RETURN:         string

    PURPOSE:        Get information about Internet Explorer
    """
    def getInternetExplorerVersion(self):
        try:
            version = self.getRegistryValue("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Internet Explorer", "Version")

        except WindowsError:
            return None

        return version