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

import re

from resources.lib.modules.liveParser import *

from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import logger
from resources.lib.modules.fileFetcher import *


class source:
    def __init__(self):
        self.base_link = ''
        self.live_link = base64.b64decode('aHR0cDovL3NvbGlkc3RyZWFtei5jb20vc29saWRkYXRhLnBocA==')
        self.srcs = []
        self.channelList = {}
        self.fileName = 'solid.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)
        self.headers={'Authorization':'Basic U29saWRTdHJlYW16OkAhU29saWRTdHJlYW16IUA='}

    def removeJSON(self, name):
        control.delete(self.fileName)
        return 0

    def livetv(self):
        try :
            generateJSON = cache.get(self.removeJSON, 168, __name__, table='live_cache')
            if not os.path.exists(self.filePath):
                generateJSON = 1

            if generateJSON:
                logger.debug('Generating %s JSON' % __name__, __name__)

                result = cache.get(self.getSolidCache, 48, table='live_cache')

                mainUrl = result["DATA"][0]["MainURL"]
                username = result["DATA"][0]["Username"]
                password = result["DATA"][0]["Password"]

                category_url = base64.b64decode('JXMvcGFuZWxfYXBpLnBocD9tb2RlPWxpdmUmdXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXM=') % (mainUrl, username, password)

                result = client.request(category_url, headers=self.headers)
                result = json.loads(result)

                categories = ['HINDI', 'PUNJABI','TAMIL LIVE', 'SOUTH INDIAN','NORTH INDIAN']
                liveCategories = result['categories']['live']
                liveChannels = result['available_channels']
                serverInfo = result['server_info']
                userInfo = result['user_info']

                categoryId = []
                for category in liveCategories:
                    if category['category_name'] in categories:
                        categoryId.append(category['category_id'])

                for i in range(0, len(categoryId)):
                    for channelKey in liveChannels:
                        channel = liveChannels[channelKey]
                        print channel
                        if channel['category_id'] == categoryId[i] and channel['live'] == '1' :
                            url = base64.b64decode('aHR0cDovLyVzOiVzL2xpdmUvJXMvJXMvJXMudHM=') % (serverInfo['url'], serverInfo['port'], userInfo['username'], userInfo['password'], channel['stream_id'])
                            title = channel['name']
                            title = re.compile('.*: ([\w\s]*)').findall(title)[0].strip()
                            icon = channel['stream_icon']
                            self.channelList[title] ={'icon':icon,'url':url,'provider':'solid','source':'solid','direct':False, 'quality':'HD'}


                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(self.channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.srcs = liveParser.parseFile(decode=False)
            return (generateJSON, self.srcs)
        except:
            import traceback
            traceback.print_exc()
            pass

    def getSolidUserAgent(self):
        import random,string
        s=eval(base64.b64decode("Wyc0LjQnLCc0LjQuNCcsJzUuMCcsJzUuMS4xJywnNi4wJywnNi4wLjEnLCc3LjAnLCc3LjEuMSdd"))

        usagents=base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCAlczsgJXMgQnVpbGQvJXM=)')%(random.choice(s),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(8)),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(6)) )
        return usagents

    def getSolidPlayUserAgent(self):
        result = cache.get(self.getSolidCache, 600000, table='live_cache')
        usagents = result["DATA"][0]["UserAgent"]
        return usagents

    def getSolidCache(self):
        url = self.live_link
        self.headers['User-Agent'] = self.getSolidUserAgent()
        result = client.request(url, headers=self.headers, post='')
        newResult = result[:2] + result[3:]
        result = base64.b64decode(newResult)
        result = json.loads(result)
        return result

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = '%s|User-Agent=%s' % (url, self.getSolidPlayUserAgent())
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        #result = client.validateUrl(url)
        logger.debug('VALID RESOLVED URL [%s]' % url, __name__)
        return url
