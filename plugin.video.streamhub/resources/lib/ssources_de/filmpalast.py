# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper4k

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

import re, urllib, urlparse, json

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['filmpalast.to']
        self.base_link = 'http://filmpalast.to'
        self.search_link = '/search/title/%s'
        self.stream_link = 'stream/%s/1'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(title)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(title)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle']
            title += ' S%02dE%02d' % (int(season), int(episode))

            url = self.__search(title)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                title += ' S%02dE%02d' % (int(season), int(episode))
                url = self.__search(title)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            hostDict.append('openload hd')

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)

            quality = client.parseDOM(r, 'span', attrs={'id': 'release_text'})[0].split('&nbsp;')[0]
            fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', quality.upper())
            fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
            fmt = [i.lower() for i in fmt]

            if '1080p' in fmt: quality = '1080p'
            elif '720p' in fmt: quality = 'HD'
            else: quality = 'SD'
            if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
            elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

            r = client.parseDOM(r, 'ul', attrs={'class': 'currentStreamLinks'})
            r = [(client.parseDOM(i, 'p', attrs={'class': 'hostName'}),
                  client.parseDOM(i, 'a', attrs={'class': '[^\'"]*stream-src[^\'"]*'}, ret='data-id')) for i in r]
            r = [(i[0][0].lower(), i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1]) for i in r if i[0] in hostDict]

            for hoster, id in r:
                sources.append({'source': hoster, 'quality': quality,
                                'provider': 'Filmpalast',
                                'language': 'de',
                                'url': id,
                                'direct': False,
                                'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            query = urlparse.urljoin(self.base_link, self.stream_link % url)
            header = {'X-Requested-With': 'XMLHttpRequest'}
            r = client.request(query, headers=header, post=urllib.urlencode({'streamID': url}))
            r = json.loads(r)
            return r['url'] if 'error' in r and r['error'] == '0' and 'url' in r else None
        except:
            return

    def __search(self, title):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'article')
            r = [(client.parseDOM(i, 'a', attrs={'class': 'rb'}, ret='href'),
                  client.parseDOM(i, 'a', attrs={'class': 'rb'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
