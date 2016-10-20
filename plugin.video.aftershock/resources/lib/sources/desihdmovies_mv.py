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


import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link = 'http://www.movieonline365.com'
        self.search_link = '?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = self.base_link
            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(result, "div", attrs={"class":"item"})
            title = cleantitle.movie(title)

            for item in result:
                searchTitle = client.parseDOM(item, "span", attrs={"class":"tt"})[0]
                try : searchTitle = re.compile('(.+?) \d{4} ').findall(searchTitle)[0]
                except: pass
                searchTitle = cleantitle.movie(searchTitle)
                if title in searchTitle:
                    url = client.parseDOM(item, "a", ret="href")[0]
                    url = re.compile(".+/(.+?)/").findall(url)[0]
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except Exception as e:
            logger.error('[%s] Exception : %s' % (self.__class__, e))
            return

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            try: result = client.source(url, referer=self.base_link)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','').replace('\t','')

            try:quality = client.parseDOM(result, "span", attrs={"class":"calidad2"})[0]
            except:quality=""

            parts = client.parseDOM(result, "div", attrs={"class":"player_nav"})[0]
            parts = client.parseDOM(parts, "a")

            items = client.parseDOM(result, "div", attrs={"id":"player2"})[0]
            items = client.parseDOM(items, "div", attrs={"class":"movieplay"})

            for i in range(0, len(items)):
                try :
                    part = parts[i]
                    part = cleantitle.movie(part)
                    if not "full" in part or "option" in part :
                        continue

                    url = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(items[i])[0][1]

                    host = client.host(url)
                    sources.append({'source': host, 'parts' : '1', 'quality': quality, 'provider': 'DesiHDMovies', 'url': url, 'direct':False})
                except :
                    pass
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except Exception as e:
            logger.error('[%s] Exception : %s' % (self.__class__, e))
            return sources


    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = resolvers.request(url, resolverList)
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url