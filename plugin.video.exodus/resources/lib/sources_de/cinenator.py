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

import re
import urllib
import urlparse
import json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze
from resources.lib.modules import anilist
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['cinenator.com']
        self.base_link = 'http://www.cinenator.com'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(localtitle, year)
            if not url and title != localtitle: url = self.__search(title, year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(localtvshowtitle, year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(tvshowtitle, year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')

            if season == 1 and episode == 1:
                season = episode = ''

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'ul', attrs={'class': 'episodios'})
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('[^\'"]*%s' % ('-%sx%s' % (season, episode)))})[0].attrs['href']

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            rel = dom_parser.parse_dom(r, 'div', attrs={'id': 'info'})
            rel = dom_parser.parse_dom(rel, 'div', attrs={'itemprop': 'description'})
            rel = dom_parser.parse_dom(rel, 'p')
            rel = [re.sub('<.+?>|</.+?>', '', i.content) for i in rel]
            rel = [re.findall('release:\s*(.*)', i, re.I) for i in rel]
            rel = [source_utils.get_release_quality(i[0]) for i in rel if i]
            quality, info = (rel[0]) if rel else ('SD', [])

            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'links'})
            r = dom_parser.parse_dom(r, 'table')
            r = dom_parser.parse_dom(r, 'tr', attrs={'id': re.compile('\d+')})
            r = [dom_parser.parse_dom(i, 'td') for i in r]
            r = [(i[0], re.sub('<.+?>|</.+?>', '', i[1].content).strip()) for i in r if len(r) >= 1]
            r = [(dom_parser.parse_dom(i[0], 'a', req='href'), i[1]) for i in r]
            r = [(i[0][0].attrs['href'], i[1]) for i in r if i[0]]

            info = ' | '.join(info)

            for link, hoster in r:
                valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                if not valid: continue

                sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': link, 'info': info, 'direct': False, 'debridonly': False, 'checkquality': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if self.base_link in url:
                r = client.request(url)
                r = dom_parser.parse_dom(r, 'div', attrs={'class': 'cupe'})
                r = dom_parser.parse_dom(r, 'div', attrs={'class': 'reloading'})
                url = dom_parser.parse_dom(r, 'a', req='href')[0].attrs['href']

            return url
        except:
            return

    def __search(self, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'article')
            r = [(dom_parser.parse_dom(i, 'div', attrs={'class': 'title'}), dom_parser.parse_dom(i, 'span', attrs={'class': 'year'})) for i in r]
            r = [(dom_parser.parse_dom(i[0][0], 'a', req='href'), i[1][0].content) for i in r if i[0] and i[1]]
            r = [(i[0][0].attrs['href'], i[0][0].content, i[1]) for i in r if i[0]]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return
