# -*- coding: utf-8 -*-
#
# USTVnow Guide
# Developed by mhancoc7
# Forked from FTV Guide:
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcaddon
import xbmcvfs
import os
import urllib2
import datetime
import zlib
import client

import control, logger

MAIN_URL = 'https://offshoregit.com/vineegu/aftershock-repo/'

class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1

    TYPE_DEFAULT = 1
    TYPE_REMOTE = 2

    basePath = control.dataPath
    filePath = ''
    fileUrl = ''
    fileStat = None
    fileType = TYPE_DEFAULT

    def __init__(self, fileName, addon):

        if fileName.startswith("http://") or fileName.startswith("sftp://") or fileName.startswith("ftp://") or \
                fileName.startswith("https://") or fileName.startswith("ftps://") or fileName.startswith("smb://") or \
                fileName.startswith("nfs://"):
            self.fileType = self.TYPE_REMOTE
            self.fileUrl = fileName
            self.filePath = os.path.join(self.basePath, fileName.split('/')[-1])
        else:
            self.fileType = self.TYPE_DEFAULT
            self.fileUrl = MAIN_URL + fileName
            self.filePath = os.path.join(self.basePath, fileName)
            self.fileName = fileName

        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        retVal = self.FETCH_NOT_NEEDED
        fetch = False
        logger.debug('Remote File : [%s] LocalFile : [%s]' %  (self.fileUrl, self.filePath), __name__)
        try :
            if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
                fetch = True
            else:
                self.fileStat = xbmcvfs.Stat(self.fileUrl)
                remoteModTime = self.fileStat.st_mtime()
                modTime = os.path.getmtime(self.filePath)
                logger.debug('Mod Time : Remote File [%s] Local File [%s]' % (datetime.datetime.fromtimestamp(remoteModTime), datetime.datetime.fromtimestamp(modTime)), __name__)
                if (remoteModTime > modTime):
                    fetch = True
                else:
                    fetch = False

            if fetch:
                tmpFile = os.path.join(self.basePath, self.fileName + '_tmp')
                if self.fileType == self.TYPE_REMOTE:
                    logger.debug('file is in remote location: %s' % self.fileUrl,__name__)
                    if not xbmcvfs.copy(self.fileUrl, tmpFile):
                        logger.error('Remote file couldn\'t be copied: %s' % self.fileUrl)
                else:
                    f = open(tmpFile, 'wb')
                    logger.debug('file is on the internet: %s' % self.fileUrl, __name__)
                    data = client.request(self.fileUrl)
                    #logger.debug(data, __name__)
                    #tmpData = urllib2.urlopen(self.fileUrl)
                    #data = tmpData.read()
                    #if tmpData.info().get('content-encoding') == 'gzip':
                    #    data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                    f.write(data)
                    f.close()
                logger.debug('file %s size %s' % (self.fileName, os.path.getsize(tmpFile)), __name__)
                if os.path.getsize(tmpFile) > 10:
                    if os.path.exists(self.filePath):
                        os.remove(self.filePath)
                    os.rename(tmpFile, self.filePath)
                    retVal = self.FETCH_OK
                    logger.debug('file %s was downloaded' % self.filePath, __name__)
                else:
                    retVal = self.FETCH_ERROR
        except:
            import traceback
            traceback.print_exc()
            pass
        return retVal
