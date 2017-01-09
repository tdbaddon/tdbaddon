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

import re
from resources.lib.libraries import client
from resources.lib.libraries import logger
from resources.lib.libraries import cache
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_link = 'http://swiftstreamz.com'
        self.live_link = base64.b64decode('aHR0cDovL3N3aWZ0c3RyZWFtei5jb20vU3dpZnRTdHJlYW0vc3dpZnRkYXRhLnBocA==')
        self.list = []
        self.fileName = 'swift.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)
        self.headers={'Authorization':base64.b64decode('QmFzaWMgVTNkcFpuUlVaV002UUZOM2FXWjBWR1ZqUUE9PQ==')}

    def removeJSON(self, name):
        control.delete(self.fileName)
        return 0

    def getLiveSource(self):
        try :
            generateJSON = cache.get(self.removeJSON, 168, __name__, table='live_cache')
            if not os.path.exists(self.filePath):
                generateJSON = 1

            if generateJSON:
                logger.debug('Generating %s JSON' % __name__, __name__)

                #result = cache.get(self.getSwiftCache, 600000, table='live_cache')

                #password = base64.b64encode(result["DATA"][0]["Password"])
                #headers = {'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)',
                #           'Authorization': 'Basic %s' % password}

                headers = {'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)'}

                category_url = 'http://swiftstreamz.com/SwiftStream/api.php'

                result = client.request(category_url, headers=headers)
                items = json.loads(result)['LIVETV']

                self.channelList = {}
                categories = ['INDIAN TV']
                for item in items:
                    if item['category_name'] in categories:
                        url = '%s?cat_id=%s' % (category_url, item['cid'])
                        #channelList = self.getSwiftChannels(url, headers)
                        channelList = self.getSwiftChannels(url, headers)

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(self.channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.list = liveParser.parseFile(decode=False)
            return (generateJSON, self.list)
        except:
            import traceback
            traceback.print_exc()
            pass

    def getSwiftChannels(self, url, headers):
        result = client.request(url, headers=headers)

        try :
            tResult = re.compile("{\"LIVETV\":(.+?)}{\"LIVETV\"").findall(result)
            tResult = json.loads(tResult[0])
            result = tResult
        except:
            result = json.loads(result)["LIVETV"]
        for channel in result:
            title = channel['channel_title']
            from resources.lib.libraries import livemeta
            names = cache.get(livemeta.source().getLiveNames, 200, table='live_cache')
            title = cleantitle.live(title, names)
            if title == 'SKIP':
                continue
            icon = channel['channel_thumbnail']
            if not icon.startswith('http'):
                icon = 'http://swiftstreamz.com/SwiftStream/images/thumbs/%s' % icon
            cUrl = channel['channel_url']
            self.channelList[title] ={'icon':icon,'url':cUrl,'provider':'swift','source':'swift','direct':False, 'quality':'HD'}
        return self.channelList
    def getSwiftUserAgent(self):
        import random,string
        s=eval(base64.b64decode("Wyc0LjQnLCc0LjQuNCcsJzUuMCcsJzUuMS4xJywnNi4wJywnNi4wLjEnLCc3LjAnLCc3LjEuMSdd"))

        usagents=base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCAlczsgJXMgQnVpbGQvJXM=)')%(random.choice(s),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(8)),''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(6)) )
        return usagents

    def getSwiftPlayUserAgent(self):
        result = cache.get(self.getSwiftCache, 600000, table='live_cache')
        usagents = result["DATA"][0]["Agent"]
        return usagents

    def getSwiftAuth(self, url):
        stripping=True
        result = cache.get(self.getSwiftCache, 600000, table='live_cache')
        if result["DATA"][0]["HelloUrl"] in url or result["DATA"][0]["HelloUrl1"] in url:
            postUrl=result["DATA"][0]["HelloLogin"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["PasswordHello"])
            stripping=False
        elif result["DATA"][0]["LiveTvUrl"] in url:
            postUrl=result["DATA"][0]["LiveTvLogin"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["PasswordLiveTv"])
        elif result["DATA"][0]["nexgtvUrl"] in url:
            postUrl=result["DATA"][0]["nexgtvToken"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["nexgtvPass"])
            stripping=False
        elif '.m3u8' not in url:
            print 'skip auth'
        else:
            postUrl=result["DATA"][0]["loginUrl"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["Password"])

        if postUrl:
            return self.getSwiftAuthToken(postUrl, auth, stripping)
        return url

    def getSwiftAuthToken(self, postUrl, auth, stripping):
        logger.debug("Generating new token", __name__)
        headers={'User-Agent':self.getSwiftUserAgent(),'Authorization':auth}
        res=client.request(postUrl,headers=headers, redirect=False)
        s=list(res)
        if stripping:
            for i in range( (len(s)-59)/12):
                ind=len(s)-59 + (12*(i))
                if ind<len(s):
                    print ind
                    s[ind]=''
        ret= ''.join(s)
        return '?'+ret.split('?')[1]

    def getSwiftCache(self):
        url = self.live_link
        self.headers['User-Agent'] = self.getSwiftUserAgent()
        result = client.request(url, headers=self.headers)
        result = json.loads(result.replace('\x0a',''))
        return result

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = '%s%s|User-Agent=%s' % (url, self.getSwiftAuth(url),self.getSwiftPlayUserAgent())
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url
