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


import urlparse, re, os, binascii, base64, time, urllib
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
        self.headers={'User-Agent':base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w')}

    def getLiveSource(self, generateJSON=False):
        try :
            if generateJSON:
                url = self.live_link
                result = client.request(url, headers=self.headers)
                result = json.loads(result)
                channelList = {}
                for channel in result:
                    title = channel['Title']
                    icon = channel['ThumbnailURL']
                    #if not channel['HLSURL'] == '' :
                    #    cUrl = channel['HLSURL']
                    #else :
                    cUrl = channel['ContentId']
                    channelList[title] ={'icon':icon,'url':cUrl,'provider':'cinefun','source':'cinefun','direct':False, 'quality':'HD', 'content':'live'}

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
            import traceback
            traceback.print_exc()
            pass

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        u = None

        try :
            #headers = {'User-agent': 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'}
            agent = cache.get(client.randomagent, 1)
            headers = {'User-agent': agent}
            result = client.request('https://cinefuntv.com/watchnow.php?content=%s' % url, headers=headers, redirect=False)
            u =  re.findall('var cms_url = [\'"](.*?)[\'"]', result)[0]
            u += '|%s' % urllib.urlencode({'User-agent': agent})
            url = u
        except:
            u = None

        if u == None:
            try :
                headers = {'User-agent': 'CFUNTV/3.1 CFNetwork/758.0.2 Darwin/15.0.0'}
                result = client.request('https://cinefuntv.com/smtalnc/content.php?cmd=details&@&device=ios&version=0&contentid=%s&sid=&u=c3281930@trbvn.com' % url, headers=headers)
                links = json.loads(result)
                u = links[0]['HLSURL']
                if u == '' :
                    u = links[0]['SamsungURL']
                if u == '' :
                    u = links[0]['PanasonicURL']
                u += "|%s" % urllib.urlencode({'User-Agent':'AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'})
                url = u
            except:
                u = None
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url
