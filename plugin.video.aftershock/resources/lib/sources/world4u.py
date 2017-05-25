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

try :import urlresolver
except:pass


class source:
    def __init__(self):
        self.base_link_1 = 'https://world4ufree.ws'
        self.base_link_2 = self.base_link_1
        self.search_link = '/?s=%s&feed=rss'
        self.movie_link = '%s/%s/'
        self.list = []

    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)

            #result = client.request(query)

            #result = result.decode('iso-8859-1').encode('utf-8')
            #result = client.parseDOM(result, "item")

            #title = cleantitle.movie(title)
            #for item in result:
            #    searchTitle = client.parseDOM(item, "title")[0]
            #    searchTitle = re.compile('(.+?) [(]\d{4}[)]').findall(searchTitle)[0]
            #    searchTitle = cleantitle.movie(searchTitle)
            #    if title == searchTitle:
            #        url = client.parseDOM(item, "link")[0]
            #        url = url.replace(self.base_link, '')
            #        break
            #if url == None or url == '':
            #    raise Exception()
            return url
        except:
            return

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            srcs = []

            if url == None: return srcs

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            imdb, title, year = data.get('imdb'), data.get('title'), data.get('year')

            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.request(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            posts = client.parseDOM(result, "item")

            items = []

            for post in posts:
                try :
                    t = client.parseDOM(post, 'title')[0]
                    if 'trailer' in cleantitle.movie(t):
                        raise Exception()

                    try: s = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)(?:GB|GiB|MB|MiB|mb|gb))', t)[0]
                    except: s = '0'

                    i = client.parseDOM(post, 'link')[0]

                    items += [{'name':t, 'url':i, 'size':s}]
                except:
                    pass

            title = cleantitle.movie(title)
            for item in items:
                try :
                    name = item.get('name')
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)
                    #searchTitle = re.compile('(.+?) \d{4}').findall(searchTitle)[0]
                    #searchTitle = cleantitle.movie(searchTitle)
                    if cleantitle.movie(title) == cleantitle.movie(t):
                        y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                        if not y == year: raise Exception()

                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                        fmt = [i.lower() for i in fmt]

                        if any(i.endswith(('subs', 'sub', 'dubbed', 'dub')) for i in fmt): raise Exception()
                        if any(i in ['extras'] for i in fmt): raise Exception()

                        if '1080p' in fmt: quality = '1080p'
                        elif '720p' in fmt: quality = 'HD'
                        else: quality = 'SD'
                        if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                        info = []

                        if '3d' in fmt: info.append('3D')

                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)(?:GB|GiB|MB|MiB|mb|gb))', item.get('size'))[-1]
                            div = 1 if size.endswith(('GB', 'GiB')) else 1024
                            size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                            size = '%.2f GB' % size
                            info.append(size)
                        except:
                            pass

                        if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

                        info = ' | '.join(info)

                        movieurl = item.get('url')

                        result = client.request(movieurl)
                        result = result.decode('iso-8859-1').encode('utf-8')
                        result = result.replace('\n','').replace('\t','')

                        result = client.parseDOM(result, 'div', attrs={'class':'entry'})[0]
                        #result = client.parseDOM(result, 'div', attrs={'class':'separator'})
                        #result = re.findall('<div class=\"wpz-sc-box(.+?)<div class=\"wpz-sc-box download', result)
                        links = client.parseDOM(result, 'a',attrs={'target':'_blank'}, ret='href')
                        for link in links:
                            if 'http' in link:
                            #if urlresolver.HostedMediaFile(url= link):
                                host = client.host(link)
                                srcs.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'world4u', 'url': link, 'direct':False, 'info':info})
                except:
                    pass
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            import traceback
            traceback.print_exc()
            return srcs

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = resolvers.request(url, resolverList)
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url