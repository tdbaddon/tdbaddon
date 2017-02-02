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

import datetime
import json
import random
import re
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import logger
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.base_link_1 = 'http://%s.hotstar.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/AVS/besc?action=SearchContents&channel=PCTV&maxResult=34&query=%s&startIndex=0&type=MOVIE,SERIES,SPORT,SPORT_LIVE'
        self.cdn_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id=%s&type=VOD'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.theaters_link = '/category/%s/feed' % (self.now.year)
        self.added_link = '/category/hindi-movies/feed'
        self.HD_link = '/category/hindi-blurays/feed'
        self.res_map = {"1080": "1080p", "900": "HD", "720": "HD", "404": "SD", "360": "SCR"}
        self.srcs = []
        if not (control.setting('hotstar_ip') == '') :
            self.ip = control.setting('hotstar_ip')
        else :
            ips = ['118.94.0.%s' % str(i) for i in range(0,100)]
            self.ip = random.choice(ips)
        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch', 'Connection':'keep-alive', 'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)', 'X-Forwarded-For': self.ip}

    def movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = urllib.quote_plus(query)
            query = self.search_link % (query)
            query = urlparse.urljoin(self.base_link % 'search', query)

            result = client.request(query, headers=self.headers)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = json.loads(result)

            result = result['resultObj']['response']['docs']

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = cleantitle.movie(item['contentTitle'])
                if title == searchTitle:
                    url = self.cdn_link % item['contentId']
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except Exception as e:
            logger.error('[%s] Exception : %s' % (self.__class__, e))
            return

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            srcs = []

            if url == None: return srcs

            try: result = client.request(url, headers=self.headers)
            except: result = ''

            result = json.loads(result)

            try :
                url = result['resultObj']['src']
                url = url.replace('http://','https://').replace('/z/','/i/').replace('manifest.f4m', 'master.m3u8').replace('2000,_STAR.','2000,3000,4500,_STAR.')
                cookie = client.request(url, headers=self.headers, output='cookie')
                result = client.request(url, headers=self.headers, cookie=cookie)

                abc = client.request(url, headers=self.headers, output='extended', close=False)

                match = re.compile("BANDWIDTH=[0-9]+,RESOLUTION=[0-9]+x(.+?),[^\n]*\n([^\n]*)\n").findall(result)
                if match:
                    for (res, url) in match:
                        try :
                            host = 'hotstar'
                            quality = self.res_map[res]
                            url = '%s|Cookie=%s' % (url, cookie)
                            srcs.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'Hotstar', 'url': url, 'direct':True})
                        except Exception as e:
                            logger.error('[%s] Exception : %s' % (self.__class__, e))
                            pass
            except Exception as e:
                logger.error('[%s] Exception : %s' % (self.__class__, e))
                pass
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        try:
            url = '%s&X-Forwarded-For=%s' % (url, self.ip)
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False