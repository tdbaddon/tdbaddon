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


from resources.lib.libraries import client
from resources.lib.libraries import logger
from resources.lib.libraries import cache
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_link = 'http://swiftstreamz.com'
        self.live_link = 'http://swiftstreamz.com/SwiftStream/swiftdata.php'
        self.list = []
        self.fileName = 'swift.json'
        self.headers={'User-Agent':base64.b64decode('RGFsdmlrLzEuNi4wIChMaW51eDsgVTsgQW5kcm9pZCA0LjQuMjsgU00tRzkwMEYgQnVpbGQvS09UNDlIKQ=='),
                      'Authorization':base64.b64decode('QmFzaWMgVTNkcFpuUlVaV002UUZOM2FXWjBWR1ZqUUE9PQ==')}

    def getLiveSource(self, generateJSON=False):
        try :
            if generateJSON:
                result = cache.get(self.getSwiftCache, 600000)

                password = base64.b64encode(result["DATA"][0]["Password"])
                headers = {'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)',
                           'Authorization': 'Basic %s' % password}

                url = 'http://swiftstreamz.com/SwiftStream/api.php?cat_id=2' #2,8

                result = client.request(url, headers=headers)
                result = json.loads(result)['LIVETV']
                channelList = {}
                for channel in result:
                    title = channel['channel_title']
                    icon = channel['channel_thumbnail']
                    if not icon.startswith('http'):
                        icon = 'http://swiftstreamz.com/SwiftStream/images/thumbs/%s' % icon
                    cUrl = channel['channel_url']
                    channelList[title] ={'icon':icon,'url':cUrl,'provider':'swift','source':'swift','direct':False, 'quality':'HD'}

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile, sort_keys=True, indent=2)

            fileFetcher = FileFetcher(self.fileName,control.addon)
            if control.setting('livelocal') == 'true':
                retValue = 1
            else :
                retValue = fileFetcher.fetchFile()
            if retValue < 0 :
                raise Exception()

            liveParser = LiveParser(self.fileName, control.addon)
            self.list = liveParser.parseFile()
            return (retValue, self.list)
        except:
            pass

    def getSwiftAuth(self, url):
        result = cache.get(self.getSwiftCache, 600000)
        if result["DATA"][0]["HelloUrl"] in url or  result["DATA"][0]["HelloUrl1"]  in url:
            postUrl=result["DATA"][0]["HelloLogin"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["PasswordHello"])
        elif result["DATA"][0]["LiveTvUrl"] in url:
            postUrl=result["DATA"][0]["LiveTvLogin"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["PasswordLiveTv"])
        elif result["DATA"][0]["nexgtvUrl"] in url:
            postUrl=result["DATA"][0]["nexgtvToken"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["nexgtvPass"])
        elif '.m3u8' not in url:
            print 'skip auth'
        else:
            postUrl=result["DATA"][0]["loginUrl"]
            auth='Basic %s'%base64.b64encode(result["DATA"][0]["Password"])

        if postUrl:
            return cache.get(self.getSwiftAuthToken, 1, postUrl, auth)
        return url

    def getSwiftAuthToken(self, postUrl, auth):
        logger.debug("Generating new token", __name__)
        headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SM-G900F Build/KOT49H)','Authorization':auth}
        res=client.request(postUrl,headers=headers)
        s=list(res)
        for i in range( (len(s)-59)/12):
            ind=len(s)-59 + (12*(i))
            if ind<len(s):
                print ind
                s[ind]=''
        return ''.join(s)

    def getSwiftCache(self):
        url = self.live_link
        result = client.request(url, headers=self.headers)
        result = json.loads(result.replace('\x0a',''))
        return result

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = '%s%s|%s' % (url, self.getSwiftAuth(url),'User-Agent=eMedia/1.0.0.')
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url
