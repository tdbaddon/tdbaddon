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

import re
import urllib
import urlparse

from ashock.modules import client
from ashock.modules import debrid
from ashock.modules import logger
from ashock.modules import cleantitle


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['300mbmoviesdl.com', 'hevcbluray.com']
        self.base_link = 'http://300mbmovies4u.co'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            sources = []

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            posts = client.parseDOM(r, 'item')

            items = []

            for post in posts:
                try:
                    t = client.parseDOM(post, 'title')[0]

                    try: s = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)(?:GB|GiB|MB|MiB|mb|gb))', t)[0]
                    except: s = '0'

                    i = client.parseDOM(post, 'link')[0]

                    items += [{'name':t, 'url':i, 'size':s}]
                except:
                    pass

            for item in items:
                try:
                    name = item.get('name')
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                    if not y == hdlr: raise Exception()

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
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)(?:GB|GiB|MB|MiB|mb))', item.get('size'))[-1]
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
                    links = client.parseDOM(result, 'a',attrs={'target':'_blank'}, ret='href')
                    for link in links:
                        try :
                            if link.startswith(self.base_link) or link.endswith('exe'): raise Exception()
                            if 'http' in link:
                                host = client.host(link)
                                sources.append({'provider':'hevcfilm','source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})
                        except:
                            pass
                except:
                    pass

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check: sources = check
            logger.debug('SOURCES URL %s' % url, __name__)
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        return url


