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


import urllib,urlparse,random

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.dittotv.com'
        self.base_link_2 = self.base_link_1
        self.search_link = 'search?q=%s'
        self.info_link = '/catalog/movie/%s/cc=US'
        self.list = []

    def get_movie(self, imdb, title, year):
        try:
            url = None
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = title
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link,query)

            result = client.request(query)

            result = result.decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(result, "div", attrs={"class":"result clearfix"})

            title = cleantitle.movie(title)
            for item in result:
                item = client.parseDOM(item, "div", attrs={"class":"details"})[0]
                searchTitle = client.parseDOM(item, "a")[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "a", ret="href")[0]
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            sources = []

            if url == None: return sources

            oUrl = urlparse.urljoin(self.base_link_1, url)
            try: result = client.request(oUrl)
            except: result = ''

            csrf = client.parseDOM(result, "meta", attrs={"name":"csrf-token"}, ret="content")[0]

            url = client.parseDOM(result, "div", attrs={"class":"video-wrapper"})[0]
            url = client.parseDOM(url, "source", ret="src")[0]
            url = '%s|Referer=%s' % (url, oUrl)

            sources.append({'source': "Ditto", 'parts': '1', 'quality': "HD", 'provider': 'Ditto', 'url': url, 'direct':True})
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        try:
            return [url]
        except:
            return False