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


import json, urlparse, re, urllib
from resources.lib.libraries import client
from resources.lib.libraries import cleantitle
from resources.lib.libraries import logger
from resources.lib.libraries import pyaes

class source:
    def __init__(self):
        self.base_link = 'http://www.dittotv.com'
        self.live_link = '/livetv'
        self.channel_link = 'http://origin.dittotv.com/livetv/%s'
        self.poster_link = 'http://dittotv2.streamark.netdna-cdn.com/vod_images/optimized/livetv/%s.jpg'
        self.headers = {'Accept':'text/html,application/xhtml+xml,q=0.9,image/jxr,*/*',
                        'Accept-Language':'en-US,en;q=0.5',
                        'Accept-Encoding':'gzip, deflate',
                        'Connection':'keep-alive',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0' ,
                        'Referer':'http://www.dittotv.com/livetv'}
        self.list = []

    def getLiveSource(self):
        try :
            url = urlparse.urljoin(self.base_link,self.live_link)

            result = client.source(url, headers=self.headers)
            result = client.parseDOM(result, "select", attrs={"class":"select_rerun_buttons "})[0]
            channels = re.compile('<option value="(\d+)">(.+?)</option>').findall(result)

            for logo, channel in channels:
                channelUrl = channel.replace('&', 'and-')
                channel = cleantitle.live(channel)
                channel = channel.title()
                channelUrl = self.channel_link % urllib.quote_plus(channelUrl).replace('+','-')
                channelUrl = channelUrl.lower()
                poster = self.poster_link % str(logo)
                self.list.append({'name':client.replaceHTMLCodes(channel), 'poster':poster,'url':channelUrl,'provider':'ditto','source':'ditto','direct':False, 'quality':'HD'})
            return self.list
        except:
            pass

    def resolve(self, url, resolverList):

        try :
            logger.debug('%s ORIGINAL URL [%s]' % (__name__, url))
            result = client.source(url, headers=self.headers)
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
            url = '%s|Referer=%s' % (link, url)
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return url
        except :
            return False