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


import urlparse, re, os, binascii, base64, time
from resources.lib.libraries import client
from resources.lib.libraries import logger
from resources.lib.libraries import cleantitle
from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_link = 'https://app.dynns.com'
        self.live_link = 'https://cinefuntv.com/smtalnc/content.php?cmd=content&categoryid=6&device=ios&version=0&key=CYxPIVE9ae'
        self.channel_link = 'https://cinefuntv.com/watchnow.php?content=%s'
        self.list = []
        self.fileName = 'cinefun.json'
        self.headers=[('User-Agent',base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w'))]

    def getLiveSource(self, generateJSON=False):
        try :
            if generateJSON:
                url = self.live_link
                result = client.source(url, headers=self.headers)
                result = json.loads(result)
                channelList = {}
                for channel in result:
                    title = channel['Title']
                    channelList[title] ={'icon':channel['ThumbnailURL'],'url':channel['ContentId'],'provider':'cinefun','source':'cinefun','direct':'false', 'quality':'HD'}

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile)

            fileFetcher = FileFetcher(self.fileName,control.addon)
            retValue = fileFetcher.fetchFile()
            if retValue < 0 :
                raise Exception()

            liveParser = LiveParser(self.fileName, control.addon)
            self.list = liveParser.parseFile()
            return (retValue, self.list)
        except:
            import traceback
            traceback.print_exc()
            pass

    def resolve(self, url, resolverList):

        try :
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            headers = [('User-agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
            result = client.source('https://cinefuntv.com/smtalnc/content.php?cmd=details&@&device=ios&version=0&contentid=%s&sid=&u=c3281930@trbvn.com' % url, headers=headers)
            links = json.loads(result)
            u = links[0]['HLSURL']
            if u == '' :
                u = links[0]['SamsungURL']
            if u == '' :
                u = links[0]['PanasonicURL']
            url = "%s|%s" % (u, 'User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)')
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return [url]
        except Exception as e:
            logger.error(e)
            return False
