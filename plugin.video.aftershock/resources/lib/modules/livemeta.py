# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import json

from resources.lib.modules import control
from resources.lib.modules import logger
from resources.lib.modules.fileFetcher import *


class source:
    def __init__(self):
        self.fileName = None
        self.list = {}

    def getLiveMeta(self):
        try :
            self.list = []
            logger.debug('meta local : %s' % control.setting('livelocal'), __name__)
            artPath = control.logoPath()

            if control.setting('livelocal') == 'true':
                self.fileName = 'live-meta.local'
            else :
                self.fileName = 'live-meta.json'
                fileFetcher = FileFetcher(self.fileName, control.addon)

                retValue = fileFetcher.fetchFile()
                if retValue < 0 :
                    raise Exception()

            filePath = os.path.join(control.dataPath, self.fileName)
            file = open(filePath)
            result = file.read()
            file.close()

            meta = json.loads(result)

            for item in meta:
                self.list.append(item)
            return self.list
        except:
            import traceback
            traceback.print_exc()
            pass


    def getLiveNames(self):
        try :
            logger.debug('names local : %s' % control.setting('livelocal'), __name__)

            if control.setting('livelocal') == 'true':
                self.fileName = 'live-chan.local'
            else :
                self.fileName = 'live-chan.json'
                fileFetcher = FileFetcher(self.fileName, control.addon)

                retValue = fileFetcher.fetchFile()
                if retValue < 0 :
                    raise Exception()

            filePath = os.path.join(control.dataPath, self.fileName)
            file = open(filePath)
            result = file.read()
            file.close()

            self.list = json.loads(result)

            return self.list
        except:
            import traceback
            traceback.print_exc()
            pass