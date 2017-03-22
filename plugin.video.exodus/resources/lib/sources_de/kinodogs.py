# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper2k4

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

from resources.lib.modules import client
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['kinodogs.to']
        self.base_link = 'http://kinodogs.to'
        self.search_link = '/search?q=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(title, year, imdb)
            if not url and title != localtitle: url = self.__search(localtitle, year, imdb)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            return self.movie(imdb, tvshowtitle, localtvshowtitle, year)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = client.parseDOM(r, 'table', attrs={'class': '[^\'"]*episodes[^\'"]*'})
            r = client.parseDOM(r, 'tr', attrs={'class': '[^\'"]*episode season_%s[^\'"]*' % season})
            r = client.parseDOM(r, 'span', attrs={'class': 'normal'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'b')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if i[1].upper() == 'E%s' % episode]

            if len(r) >= 1:
                url = client.replaceHTMLCodes(r[0])
                url = url.encode('utf-8')
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = client.parseDOM(r, 'table', attrs={'class': '[^\'"]*stream_links[^\'"]*'})
            r = client.parseDOM(r, 'tr')
            r = [(client.parseDOM(i, 'td'),
                  client.parseDOM(i, 'td', attrs={'class': 'hide-for-small-only'})) for i in r]
            r = [(client.parseDOM(i[0][0], 'a', ret='href'), i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0][0], i[1]) for i in r if len(i[0]) > 0]
            r = [(i[0], i[1]) for i in r if i[1] in hostDict]

            for link, hoster in r:
                sources.append({'source': hoster, 'quality': 'SD',
                                'language': 'de',
                                'url': link,
                                'direct': False,
                                'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if not url.startswith('http'):
                url = urlparse.urljoin(self.base_link, url)
                url = client.request(url, output='geturl', error=True)

            if self.base_link not in url:
                return url
        except:
            return url


    def __search(self, title, year, imdb):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            tq = cleantitle.query(title).lower()
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'movie_cell'})
            r = [(client.parseDOM(i, 'div', attrs={'class': 'bottom'}), client.parseDOM(i, 'div', attrs={'class': 'year'})) for i in r]
            r = [(client.parseDOM(i[0], 'a', attrs={'title': ''}, ret='href'), client.parseDOM(i[0], 'a', attrs={'title': ''}), re.findall('[(](\d{4})[)]', i[1][0])) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1].lower(), i[2]) for i in r if i[2] in y]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year

            r_t = [i[0] for i in r if t == cleantitle.get(i[1])]
            r_t = r_t if len(r_t) > 0 else [i[0] for i in r if tq == cleantitle.query(i[1])]
            r = r_t

            if len(r) > 1:
                for i in r:
                    data = client.request(urlparse.urljoin(self.base_link, i))
                    data = client.parseDOM(data, 'a', attrs={'name': '[^\'"]+/tt\d+[^\'"]+'}, ret='name')
                    data = [re.findall('.+?(tt\d+).*?', d) for d in data]
                    data = [d[0] for d in data if len(d) > 0 and d[0] == imdb]

                    if len(data) >= 1:
                        url = i
            else:
                url = r[0]

            if url:
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                return url
        except:
            return