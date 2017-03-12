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

import base64
import os
import urllib

from ashock.modules.fileFetcher import *
from ashock.modules.liveParser import *

from ashock.modules import cache
from ashock.modules import client
from ashock.modules import control
from ashock.modules import logger


class source:
    def __init__(self):
        self.base_link = 'https://cinefuntv.com'
        self.live_link = 'https://cinefuntv.com/smtalnc/content.php?cmd=content&categoryid=6&device=ios&version=0&key=CYxPIVE9ae'
        self.channel_link = 'https://cinefuntv.com/watchnow.php?content=%s'
        self.srcs = []
        self.fileName = 'cinefun.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)
        self.headers={'User-Agent':base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w')}

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
                url = self.live_link
                result = client.request(url, headers=self.headers)
                result = json.loads(result)
                channelList = {}
                for channel in result:
                    title = channel['Title']
                    #title = cleantitle.live(title)
                    #if title == 'SKIP':
                    #    continue
                    icon = channel['ThumbnailURL']
                    cUrl = channel['ContentId']
                    channelList[title] ={'icon':icon,'url':cUrl,'provider':'cinefun','source':'cinefun','direct':False, 'quality':'HD', 'content':'live'}

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.srcs = liveParser.parseFile(decode=False)
            return (generateJSON, self.srcs)
        except:
            import traceback
            traceback.print_exc()
            pass

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        u = None

        '''
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
        '''

        if u == None:
            try :
                headers = {'User-agent': base64.b64decode('Q0ZVTlRWLzMuMSBDRk5ldHdvcmsvNzU4LjAuMiBEYXJ3aW4vMTUuMC4w')}
                result = client.request(base64.b64decode('aHR0cHM6Ly9jaW5lZnVudHYuY29tL3NtdGFsbmMvY29udGVudC5waHA/Y21kPWRldGFpbHMmQCZkZXZpY2U9aW9zJnZlcnNpb249MCZjb250ZW50aWQ9JXMmc2lkPSZ1PWMzMjgxOTMwQHRyYnZuLmNvbQ==') % url, headers=headers, redirect=False)
                links = json.loads(result)
                u = links[0]['HLSURL']
                if u == '' :
                    u = links[0]['SamsungURL']
                if u == '' :
                    u = links[0]['PanasonicURL']
                u += "|%s" % urllib.urlencode({'User-Agent':'AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)'})
                url = u
            except:
                url = None
        result = client.validateUrl(url)
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url
