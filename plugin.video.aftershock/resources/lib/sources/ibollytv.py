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
import re
import urllib
import urlparse

from resources.lib import resolvers
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import logger
from resources.lib.modules import workers
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.base_link = 'http://www.ibollytv.com'
        self.search_link = '/search.php?q=%s'
        self.now = datetime.datetime.now()
        self.theaters_link = '/watch-%s-movies-online?year=%s&' % ('%s', self.now.year)
        self.added_link = '/watch-%s-movies-online?'
        self.sort_link = 'order=desc&sort=latest'
        self.srcs = []
        self.genres = {'Action':'Action',
                       'Adult':'Mature',
                       'Children':'Animation',
                       'Comedy':'Comedy',
                       'Crime':'Crime',
                       'Drama':'Drama',
                       'Family':'Family',
                       'Horror':'Horror',
                       'Romance':'Romance',
                       'Thriller':'Thriller',
                       'Suspense':'Suspense'}
        self.genre_url = '/watch-%s-movies-online?genre=%s'
        self.years_url = '/watch-%s-movies-online?year=%s'

    def movie(self, imdb, title, year):
        try:
            self.base_link = self.base_link
            query = '%s' % (title)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "div", attrs={"class": "tab-content mt20"})[0]
            result = client.parseDOM(result, "div", attrs={"id": "movies_tab"})[0]
            result = client.parseDOM(result, "div", attrs={"class": "media-left"})

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "a", ret="title")[0]
                searchTitle = re.compile('(.+?) [(]\d{4}[)]$').findall(searchTitle)[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "a", ret="href")[0]
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
            self.srcs = []

            if url == None: return self.srcs

            try: result = client.request(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "div", attrs={"class": "col-md-12 mt20"})[0]

            try :
                item = client.parseDOM(result, "center")[0]

                url = re.compile('(SRC|src|data-config)=\"(.+?)\"').findall(item)[0][1]
                host = client.host(url)
                self.srcs.append({'source': host, 'parts' : '1', 'quality': quality, 'provider': 'iBollyTV', 'url': url, 'direct':False})
            except:
                pass

            hypermode = False if control.setting('hypermode') == 'false' else True
            threads = []
            try :
                result = client.parseDOM(result, "div", attrs={"class": "table-responsive"})[0]
                result = client.parseDOM(result, "tbody")[0]
                result = client.parseDOM(result, "tr")
                for item in result:
                    if hypermode :
                        threads.append(workers.Thread(self.source, item))
                    else :
                        self.source(item)

                if hypermode:
                    [i.start() for i in threads]

                    stillWorking = True

                    while stillWorking:
                        stillWorking = False
                        stillWorking = [True for x in threads if x.is_alive() == True]

            except:
                pass
            logger.debug('SOURCES [%s]' % self.srcs, __name__)
            return self.srcs
        except:
            return self.srcs

    def source(self, item):
        quality = ''
        try :
            urls = client.parseDOM(item, "td", attrs={"class": "col-md-7"})[0]
            urls = client.parseDOM(urls, "a", ret="href")
            for i in range(0, len(urls)):
                item = client.request(urls[i], mobile=False)
                item = item.replace('\n','').replace('\t','')
                item = client.parseDOM(item, "div", attrs={"class": "embed-responsive embed-responsive-16by9"})[0]
                item = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                urls[i] = item
            host = client.host(urls[0])
            if len(urls) > 1:
                url = "##".join(urls)
            else:
                url = urls[0]
            self.srcs.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'iBollyTV', 'url': url, 'direct':False})
        except:
            pass

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
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
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False