# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 IDev

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


import urllib,urlparse,random, json, re

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import logger
from resources.lib import resolvers
from resources.lib.libraries import jsunpack

from BeautifulSoup import BeautifulSoup, SoupStrainer

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.tamilgun.pro'
        self.base_link_2 = self.base_link_1
        self.search_link = '/feed/?search=Search&s=%s'
        self.list = []

    def get_movie(self, imdb, title, year):
        try:
            url = None
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            #query = '%s %s' % (title, year)
            query = title
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link,query)

            result = client.request(query, error=True)

            items = client.parseDOM(result, "item")

            title = cleantitle.movie(title)
            for item in items:
                searchTitle = client.parseDOM(item, "title")[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title in searchTitle:
                    url = client.parseDOM(item, "a", attrs={"rel":"nofollow"}, ret="href")[0]
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            import traceback
            traceback.print_exc()
            return

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try :
            sources = []

            if url == None: return sources

            if 'hd' in url.lower():
                quality = 'HD'
            else:
                quality = 'SD'

            html = client.request(url)

            try:
                linkcode = jsunpack.unpack(html).replace('\\','')
                sources = json.loads(re.findall('sources:(.*?)\}\)',linkcode)[0])
                for source in sources:
                    url = source['file']
                    host = client.host(url)
                    sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'tamilgun', 'url': url, 'direct':False})
            except:
                pass

            mlink = SoupStrainer('div', {'id':'videoframe'})
            videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

            try:
                links = videoclass.findAll('iframe')
                for link in links:
                    url = link.get('src')
                    host = client.host(url)
                    sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'tamilgun', 'url': url, 'direct':False})
            except:
                pass


            mlink = SoupStrainer('div', {'class':'entry-excerpt'})
            videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

            try:
                links = videoclass.findAll('iframe')
                for link in links:
                    if 'http' in str(link):
                        url = link.get('src')
                        host = client.host(url)
                        sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'tamilgun', 'url': url, 'direct':False})
            except:
                pass

            try:
                sources = json.loads(re.findall('vdf-data-json">(.*?)<',html)[0])
                url = 'https://www.youtube.com/watch?v=%s'%sources['videos'][0]['youtubeID']
                host = client.host(url)
                sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'tamilgun', 'url': url, 'direct':False})
            except:
                pass

            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        try:
            r = resolvers.request(url, resolverList)
            if not r :
                raise Exception()
            url = r
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False