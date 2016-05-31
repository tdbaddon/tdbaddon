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


import re,urllib,urlparse,random, datetime, json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://%s.hotstar.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/AVS/besc?action=GetSuggestionsStar&query=%s&type=vod'
        self.cdn_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id=%s&type=VOD'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.theaters_link = '/category/%s/feed' % (self.now.year)
        self.added_link = '/category/hindi-movies/feed'
        self.HD_link = '/category/hindi-blurays/feed'
        self.res_map = {"1080": "1080p", "900": "HD", "720": "HD", "404": "SD", "360": "SCR"}
        self.list = []
        if not (control.setting('hotstar_ip') == '') :
            self.ip = control.setting('hotstar_ip')
        else :
            ips = ['118.94.0.%s' % str(i) for i in range(0,100)]
            self.ip = random.choice(ips)

        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Connection':'keep-alive', 'X-Forwarded-For': self.ip}

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link % 'search', query)

            result = client.source(query, headers=self.headers,safe=True)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = json.loads(result)

            result = result['resultObj']['suggestion']

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = cleantitle.movie(item['title'])
                if title == searchTitle:
                    url = self.cdn_link % item['contentId']
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('%s SOURCES URL %s' % (self.__class__, url))
        try:
            quality = ''
            sources = []

            if url == None: return sources

            try: result = client.source(url, headers=self.headers)
            except: result = ''

            result = json.loads(result)

            try :
                url = result['resultObj']['src']
                url = url.replace('http://','https://').replace('/z/','/i/').replace('manifest.f4m', 'master.m3u8').replace('2000,_STAR.','2000,3000,4500,_STAR.')
                cookie = client.source(url, headers=self.headers, output='cookie')
                result = client.source(url, headers=self.headers)

                match = re.compile("BANDWIDTH=[0-9]+,RESOLUTION=[0-9]+x(.+?),[^\n]*\n([^\n]*)\n").findall(result)
                if match:
                    for (res, url) in match:
                        try :
                            host = 'hotstar'
                            quality = self.res_map[res]
                            url = '%s|Cookie=%s' % (url, cookie)
                            sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'Hotstar', 'url': url, 'direct':True})
                        except:
                            pass
            except:
                pass
            logger.debug('%s SOURCES [%s]' % (__name__,sources))
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        logger.debug('%s ORIGINAL URL [%s]' % (__name__, url))
        try:
            cookie = url.split("|")[1]
            url = '%s|Cookie=%s&%s' % (url, cookie,urllib.urlencode(self.headers))
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return [url]
        except:
            return False