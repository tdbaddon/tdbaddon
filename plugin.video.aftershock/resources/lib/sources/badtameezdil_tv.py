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
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse, datetime
import BeautifulSoup

from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://badtameezdil.net'
        self.base_link_2 = 'http://badtameezdil.net'
        self.base_link_3 = 'http://badtameezdil.net'

        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = 'http://www.desiplex.net/watch/?id=%s'
        self.now = datetime.datetime.now()

        self.list = []

    def get_show(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:

            return tvshowtitle

    def get_episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        query = '%s %s' % (imdb, title)
        query = self.search_link % (urllib.quote_plus(query))
        result = ''

        links = [self.base_link_1, self.base_link_2, self.base_link_3]
        for base_link in links:
            try: result = client.request(base_link + query)
            except: result = ''
            if 'item' in result: break

        result = result.decode('iso-8859-1').encode('utf-8')

        result = result.replace('\n','').replace('\t','')

        result = client.parseDOM(result, 'content:encoded')[0]

        ep_url = client.parseDOM(result, "a", attrs={"rel":"nofollow"}, ret="href")[0]

        if ep_url :
            return ep_url

    def get_sources(self, url):
        try:
            logger.debug('SOURCES URL %s' % url, __name__)
            quality = 'HD'
            sources = []

            result = ''

            try: result = client.request(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','').replace('\t','')

            result = client.parseDOM(result, "div", attrs={"class":"single-post-video"})[0]

            url = re.compile('(data-config)=[\'|\"](.+?)[\'|\"]').findall(result)[0][1]

            if url.startswith('//'):
                url='http:%s'%url
            host = client.host(url)

            sources.append({'source':host, 'parts': '1', 'quality':quality,'provider':'BadtameezDil','url':url, 'direct':False})
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        try:
            logger.debug('ORIGINAL URL [%s]' % url, __name__)

            r = resolvers.request(url, resolverList)
            if not r :
                raise Exception()
            url = r
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False