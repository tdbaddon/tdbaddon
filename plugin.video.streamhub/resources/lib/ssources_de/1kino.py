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

import re, urllib, urlparse

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['1kino.in']
        self.base_link = 'http://1kino.in'
        self.search_link = '/?s=%s'
        self.drop_link = '/drop.php'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(imdb, title, year)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(imdb, title, year)
            if url:
                return urllib.urlencode({'url': url})
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            return self.movie(imdb, tvshowtitle, year)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'season': season, 'episode': episode})
            return urllib.urlencode(data)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = urlparse.urljoin(self.base_link, data['url'])
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False

            r = client.request(url)

            if season and episode:
                r = client.parseDOM(r, 'div', attrs={'id': 'footer'})
                r = re.findall('var postID="([^\'"]+)"', r[0])[0]
                r = {'ceck': 'sec', 'option': 's%s_e%s' % (episode,episode), 'pid': r}
                r = urllib.urlencode(r)
                r = client.request(urlparse.urljoin(self.base_link, self.drop_link), post=r)
            else:
                r = client.parseDOM(r, 'div', attrs={'id': 'stream-container'})[0]

            r = re.compile('<div id="stream-h">.*?</li>.*?</div>\s*</div>', re.IGNORECASE | re.DOTALL).findall(r)
            r = [(client.parseDOM(i, 'div', attrs={'id': 'mirror-head'}),
                  client.parseDOM(i, 'div', attrs={'id': 'stream-links'})
                  ) for i in r]
            r = [(i[0][0], i[1]) for i in r if len(i[0]) > 0]
            r = [(re.findall('.+\|(.+)', i[0]), i[1]) for i in r]
            r = [(i[0][0].strip(), i[1]) for i in r if len(i[0]) > 0]

            for name, links in r:
                fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                fmt = [i.lower() for i in fmt]

                if '1080p' in fmt: quality = '1080p'
                elif '720p' in fmt: quality = 'HD'
                else: quality = 'SD'
                if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt):  quality = 'SCR'
                elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                links = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in links]
                links = [(i[0][0], i[1][0].lower().strip()) for i in links if len(i[0]) > 0 and len(i[1]) > 0]
                links = [(i[0], i[1]) for i in links if i[1] in hostDict]

                for link, hoster in links:
                    sources.append({'source': hoster, 'quality': quality,
                                    'provider': '1Kino',
                                    'language': 'de',
                                    'url': link,
                                    'direct': False,
                                    'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        url = client.request(url, output='geturl')
        if self.base_link not in url:
            return url

    def __search(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'main-area'})
            r = client.parseDOM(r, 'li')
            r = client.parseDOM(r, 'div', attrs={'class': 'table-ui1'})
            r = [(client.parseDOM(i, 'a', attrs={'title': ''}, ret='href'),
                  client.parseDOM(i, 'a', attrs={'title': ''}),
                  client.parseDOM(i, 'a', attrs={'href': '[^\'"]+/tt\d+[^\'"]+'}, ret='href')
                  ) for i in r]
            r = [(i[0][0], i[1][0].lower(), re.findall('.+?(tt\d+).*?', i[2][0])) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            r = [(i[0], i[1], re.findall('(.+?) \((\d{4})\)?', i[1]), i[2]) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0', i[3]) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y and i[3] == imdb][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
