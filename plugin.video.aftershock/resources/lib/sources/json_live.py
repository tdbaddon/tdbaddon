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
from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import logger
from resources.lib.libraries import cleantitle
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import  *

class source:
    def __init__(self):
        self.fileName = 'static.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)
        self.list = []

    def removeJSON(self, name):
        control.delete(self.fileName)
        return 0

    def getLiveSource(self, generateJSON=False):
        try :
            retValue = 0
            generateJSON = cache.get(self.removeJSON, 168, __name__, table='live_cache')
            if not os.path.exists(self.filePath):
                generateJSON = 1

            if generateJSON:
                fileFetcher = FileFetcher(self.fileName, control.addon)
                if control.setting('livelocal') == 'true':
                    retValue = 1
                else :
                    retValue = fileFetcher.fetchFile()
                if retValue < 0 :
                    raise Exception()

                liveParser = LiveParser(self.fileName, control.addon)
                self.list = liveParser.parseFile()
            return (retValue, self.list)
        except :
            import traceback
            traceback.print_exc()
            pass

    def resolve(self, url, resolverList):
        return url