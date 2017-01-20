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


import json, urlparse, re, urllib, os
from resources.lib.libraries import client
from resources.lib.libraries import cleantitle
from resources.lib.libraries import logger
from resources.lib.libraries import pyaes
from resources.lib.libraries import control
from resources.lib.libraries import cache
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_link = 'http://www.dittotv.com'
        self.live_link = 'http://origin.dittotv.com/livetv/all/0'
        self.channel_link = 'http://origin.dittotv.com%s'
        self.headers = {'Accept':'text/html,application/xhtml+xml,q=0.9,image/jxr,*/*',
                        'Accept-Language':'en-US,en;q=0.5',
                        'Accept-Encoding':'gzip, deflate',
                        'Connection':'keep-alive',
                        'User-Agent': cache.get(client.randomagent, 1, table='live_cache') ,
                        'Referer':'http://www.dittotv.com/livetv'}
        self.list = []
        self.fileName = 'ditto.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)

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
                url = self.live_link

                result = client.request(url, headers=self.headers)
                channels=re.findall('<div class="subpattern.*?\s*<a href="(.*?)" title="(.*?)".*?\s*<img src=".*?".*?\s*<img src="(.*?)"',result)

                channelList = {}
                for url, title, icon in channels:
                    title = title.replace("&amp;","And")
                    #from resources.lib.libraries import livemeta
                    #names = cache.get(livemeta.source().getLiveNames, 200, table='live_cache')
                    #title = cleantitle.live(title)
                    #if title == 'SKIP':
                    #    continue
                    if 'temple' in title.lower():
                        continue
                    url = self.channel_link % url
                    channelList[title] ={'icon':icon,'url':url,'provider':'ditto','source':'ditto','direct':False, 'quality':'HD', 'content':'live'}

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.list = liveParser.parseFile(decode=False)
            return (generateJSON, self.list)
        except:
            import traceback
            traceback.print_exc()
            pass

    def resolve(self, url, resolverList):
        try :
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            result = client.request(url, headers=self.headers)
            playdata='window.pl_data = (\{.*?"key":.*?\}\})'
            result=re.findall(playdata, result)[0]
            try :
                result = json.loads(result)
                link = result['live']['channel_list'][0]['file']
                key = result['live']['key']
                link = link.decode('base64')
                key = key.decode('base64')
                de = pyaes.new(key, pyaes.MODE_CBC, IV='\0'*16)
                link = de.decrypt(link).replace('\x00', '').split('\0')[0]
                link = re.sub('[^\s!-~]', '', link)
            except:link = client.parseDOM(result, "source", attrs={"type":"application/x-mpegurl"}, ret="src")[0]
            logger.debug('URL : [%s]' % link, __name__)
            url = '%s|Referer=%s' % (link.strip(), url)
            result = client.validateUrl(url)
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except :
            return False