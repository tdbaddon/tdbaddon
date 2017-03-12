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
import random
import re
import urllib
import urlparse

from resources.lib import resolvers
from ashock.modules import client
from ashock.modules import logger
from ashock.modules import metacache
from ashock.modules import cleantitle


class source:
    def __init__(self):
        self.base_link_1 = 'http://hdbuffer.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/?s=%s&feed=rss'
        self.movie_link = '%s/%s/'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.HD_link = '/category/%s/dvdbluraymovies-%sonline'
        self.list = []

    def movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "item")

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "title")[0]
                searchTitle = re.compile('(.+?) [(]\d{4}[)]').findall(searchTitle)[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "link")[0]
                    url = url.replace(self.base_link, '')
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            srcs = []

            if url == None: return srcs

            try: result = client.request(self.movie_link % (self.base_link_1, url))
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            categories = client.parseDOM(result, "div", attrs={"id": "extras"})
            categories = client.parseDOM(categories, "a", attrs={"rel": "category tag"})

            for category in categories:
                category = category.lower()
                if "scr" in category:
                    quality = "SCR"
                    break
                elif "bluray" in category:
                    quality = "HD"
                    break

            links = client.parseDOM(result, "div", attrs={"class": "GTTabs_divs GTTabs_curr_div"})
            links += client.parseDOM(result, "div", attrs={"class": "GTTabs_divs"})
            for link in links:
                try :
                    url = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(link)[0][1]
                    host = client.host(url)
                    srcs.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'HDBuffer', 'url': url, 'direct':False})
                except :
                    pass
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = resolvers.request(url, resolverList)
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url



