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


import re,urllib,urlparse, random

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.hindilinks4u.to'
        self.base_link_2 = self.base_link_1
        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = ''
        self.list = []

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "item")

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "title")[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "link")[0]
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

            try: result = client.source(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            quality = ''

            result = client.parseDOM(result, name="div", attrs={"class" : "entry-content rich-content"})[0]
            result = client.parseDOM(result, name="p")
            try :
                host = ''
                urls = []
                result = result[1::]
                serversList = result[::2]
                linksList = result[1::2]
                for i in range(0, len(serversList)):
                    try :
                        links = linksList[i]
                        urls = client.parseDOM(links, name="a", ret="href")

                        for j in range(0, len(urls)):
                            try :
                                item = client.source(urls[j], mobile=True)
                                item = client.parseDOM(item, "td")[0]
                                item = re.compile('(SRC|src|data-config)=\"(.+?)\"').findall(item)[0][1]
                                urls[j] = item
                            except:
                                pass
                        if len(urls) > 1:
                            url = "##".join(urls)
                        else:
                            url = urls[0]
                        host = client.host(urls[0])
                        sources.append({'source': host, 'parts': str(len(urls)), 'quality': quality, 'provider': 'HindiLinks4U', 'url': url, 'direct':False})
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
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
            url = links
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return url
        except:
            return False