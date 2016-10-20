# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import datetime, base64, os, json
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import logger
from resources.lib.libraries.fileFetcher import *

class source:
    def __init__(self):
        self.fileName = None
        self.list = {}

    def getLivePosters(self):
        try :
            logger.debug('logos local : %s' % control.setting('livelocal'), __name__)
            artPath = control.logoPath()

            if control.setting('livelocal') == 'true':
                self.fileName = 'live-logos-new.json'
            else :
                self.fileName = 'live-logos-new.json'

            fileFetcher = FileFetcher(self.fileName, control.addon)

            retValue = fileFetcher.fetchFile()
            if retValue < 0 :
                raise Exception()

            filePath = os.path.join(control.dataPath, self.fileName)
            file = open(filePath)
            result = file.read()
            file.close()

            result = base64.urlsafe_b64decode(result)

            channels = json.loads(result)

            channelNames = channels.keys()
            channelNames.sort()

            for channel in channelNames:
                channelObj = channels[channel]
                posterUrl = channelObj['iconimage']
                if not channelObj['enabled'] == 'false' and posterUrl.startswith('http://'):
                    self.list[channel] = posterUrl
                else :
                    self.list[channel] = os.path.join(artPath, posterUrl)
                print self.list[channel]
            return self.list
        except:
            import traceback
            traceback.print_exc()
            pass