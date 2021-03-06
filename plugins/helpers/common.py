'''
   Copyright (c) 2017 Yogesh Khatri 

   This file is part of mac_apt (macOS Artifact Parsing Tool).
   Usage or distribution of this software/code is subject to the 
   terms of the MIT License.
   
'''

from __future__ import unicode_literals

import os
import datetime
import pytz
import logging
from tzlocal import get_localzone

log = logging.getLogger('MAIN.HELPERS.COMMON')

class CommonFunctions:

    @staticmethod
    def GetLocalTimeFromUtcDate(d_utc):
        '''Returns a datetime object converted to local time'''
        local_timezone = get_localzone()
        #local_tz = get_localzone()
        return d_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    #TODO: Provide better implementation that does not restrict to POSIX 1970-2038
    @staticmethod
    def ReadMacAbsoluteTime(mac_abs_time): # Mac Absolute time is time epoch beginning 2001/1/1
        '''Returns datetime object, or empty string upon error'''
        if mac_abs_time not in ( 0, None, ''):
            try:
                if type(mac_abs_time) in (str, unicode):
                    mac_abs_time = float(mac_abs_time)
                return datetime.datetime.utcfromtimestamp(mac_abs_time + 978307200)
            except Exception as ex:
                log.error("ReadMacAbsoluteTime() Failed to convert timestamp from value " + mac_abs_time + " Error was: " + str(ex))
        return ''

    #TODO: Provide better implementation that does not restrict to POSIX 1970-2038 
    @staticmethod
    def ReadMacHFSTime(mac_hfs_time): # Mac HFS+ timestamp is time epoch beginning 1904/1/1
        '''Returns datetime object, or empty string upon error'''
        if mac_hfs_time not in ( 0, None, ''):
            try:
                if type(mac_hfs_time) in (str, unicode):
                    mac_hfs_time = float(mac_hfs_time)
                return datetime.datetime.utcfromtimestamp(mac_hfs_time - 2082844800)
            except Exception as ex:
                log.error("ReadMacHFSTime() Failed to convert timestamp from value " + str(mac_hfs_time) + " Error was: " + str(ex))
        return ''

    @staticmethod
    def ReadUnixTime(unix_time): # Unix timestamp is time epoch beginning 1970/1/1
        '''Returns datetime object, or empty string upon error'''
        if unix_time not in ( 0, None, ''):
            try:
                if type(unix_time) in (str, unicode):
                    unix_time = float(unix_time)
                return datetime.datetime.utcfromtimestamp(unix_time)
            except Exception as ex:
                log.error("ReadUnixTime() Failed to convert timestamp from value " + str(unix_time) + " Error was: " + str(ex))
        return ''

    @staticmethod
    def IntFromStr(str):
        integer = 0
        try:
            integer = int(str)
        except: # Will go here if str is '' or contains non-digit characters
            if str == '' or str == None: pass
            else: log.exception('Could not convert str {} to int'.format(str))
        return integer

    @staticmethod
    def GetNextAvailableFileName(filepath):
        '''
        Checks for existing file and returns next available file name 
        by appending file name with a number. Ex: file01.jpg
        '''
        if os.path.exists(filepath):
            split = os.path.splitext(filepath)
            filepath_without_ext = split[0]
            ext = split[1]
            index = 1
            fullpath = filepath_without_ext + '{0:02d}'.format(index) + ext
            while (os.path.exists(fullpath)):
                index += 1
                fullpath = filepath_without_ext + '{0:02d}'.format(index) + ext
            filepath = fullpath
        return filepath