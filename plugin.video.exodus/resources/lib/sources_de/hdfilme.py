# -*- coding: utf-8 -*-

"""
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
"""

import base64
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['hdfilme.tv']
        self.base_link = 'http://hdfilme.tv'
        self.search_link = '/movie-search?key=%s'
        self.get_link = '/movie/getlink/%s/%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(localtitle, year)
            if not url and title != localtitle: url = self.__search(title, year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = self.__search(data['localtvshowtitle'], data['year'], season)
            if not url and data['tvshowtitle'] is not data['localtvshowtitle']: url = self.__search(data['tvshowtitle'], data['year'], season)
            if not url: return

            r = client.request(urlparse.urljoin(self.base_link, url))

            r = dom_parser.parse_dom(r, 'ul', attrs={'class': ['list-inline', 'list-film']})
            r = dom_parser.parse_dom(r, 'li')
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content) for i in r if i]
            r = [(i[0], i[1] if re.compile("^(\d+)$").match(i[1]) else '0') for i in r]
            r = [i[0] for i in r if int(i[1]) == int(episode)][0]

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = re.findall('(\d+)-stream(?:\?episode=(\d+))?', url)
            r = [(i[0], i[1] if i[1] else '1') for i in r][0]
            r = client.request(urlparse.urljoin(self.base_link, self.get_link % r))
            r += '=' * (-len(r) % 4)
            r = base64.b64decode(r)
            r = re.findall('file"?\s*:\s*"(.+?)"', r)

            for i in r:
                try:
                    i = i.replace('\/', '/')
                    i = client.replaceHTMLCodes(i).encode('utf-8')

                    sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'de', 'url': i, 'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, title, year, season='0'):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            tq = cleantitle.query(title).lower()
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'ul', attrs={'class': ['products', 'row']})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': ['box-product', 'clearfix']})
            r = dom_parser.parse_dom(r, 'h3', attrs={'class': 'title-product'})
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content.lower()) for i in r if i]
            r = [(i[0], i[1], re.findall('(.+?) \(*(\d{4})', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = [(i[0], i[1], i[2], re.findall('(.+?)\s+(?:staf+el|s)\s+(\d+)', i[1])) for i in r]
            r = [(i[0], i[3][0][0] if len(i[3]) > 0 else i[1], i[2], i[3][0][1] if len(i[3]) > 0 else '0') for i in r]
            r = [(i[0], i[1].replace(' hd', ''), i[2], i[3]) for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [(i[0], i[1]) for i in r if i[2] in y and int(i[3]) == int(season)]

            url = [i[0] for i in r if t == cleantitle.get(i[1])]
            url = url[0] if len(url) > 0 else [i[0] for i in r if tq == cleantitle.query(i[1])][0]

            url = source_utils.strip_domain(url)
            url = url.replace('-info', '-stream')
            return url
        except:
            return