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
import base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['1kino.in']
        self.base_link = 'http://1kino.in'
        self.search_link = '/?s=%s'
        self.drop_link = '/drop.php'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(imdb, title, year)
            if not url and title != localtitle: url = self.__search(imdb, localtitle, year)
            return urllib.urlencode({'url': url}) if url else None
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            return self.movie(imdb, tvshowtitle, localtvshowtitle, year)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
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
            if not url:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = urlparse.urljoin(self.base_link, data.get('url'))
            season = data.get('season')
            episode = data.get('episode')

            r = client.request(url)

            if season and episode:
                r = dom_parser.parse_dom(r, 'div', attrs={'id': 'footer'})[0].content
                r = re.findall('var postID="([^\'"]+)"', r)[0]
                r = urllib.urlencode({'ceck': 'sec', 'option': 's%s_e%s' % (season, episode), 'pid': r})
                r = client.request(urlparse.urljoin(self.base_link, self.drop_link), post=r)
            else:
                r = dom_parser.parse_dom(r, 'div', attrs={'id': 'stream-container'})[0].content

            r = re.compile('<div id="stream-h">.*?</li>.*?</div>\s*</div>', re.IGNORECASE | re.DOTALL).findall(r)
            r = [(dom_parser.parse_dom(i, 'div', attrs={'id': 'mirror-head'}), dom_parser.parse_dom(i, 'div', attrs={'id': 'stream-links'})) for i in r]
            r = [(i[0][0].content, i[1]) for i in r if i[0]]
            r = [(re.findall('.+\|(.+)', i[0]), i[1]) for i in r]
            r = [(i[0][0].strip(), i[1]) for i in r if len(i[0]) > 0]

            for name, links in r:
                quality, info = source_utils.get_release_quality(name)

                links = [dom_parser.parse_dom(i.content, 'a', req='href') for i in links]
                links = [(i[0].attrs.get('href'), i[0].content) for i in links]

                info = ' | '.join(info)

                for link, hoster in links:
                    valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                    if not valid: continue

                    sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': link, 'info': info, 'direct': False, 'debridonly': False, 'checkquality': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            match = re.findall('go/([a-zA-Z0-9+/]+={0,2})', url)
            if match:
                match = base64.b64decode(match[0])
                if match.startswith('http'):
                    url = match.strip()

            if self.base_link in url:
                url = client.request(url, output='geturl')

            if self.base_link not in url:
                return url
        except:
            return

    def __search(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'main-area'})
            r = dom_parser.parse_dom(r, 'li')
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'table-ui1'})
            r = [(dom_parser.parse_dom(i.content, 'a', req=['href', 'title']), dom_parser.parse_dom(i.content, 'a', attrs={'href': re.compile('.*/%s.*' % imdb)})) for i in r]
            r = [(i[0][0].attrs['href'], i[0][0].content) for i in r if i[0]]
            r = [(i[0], i[1], re.findall('(.+?) \((\d{4})\)?', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y][0]

            url = urlparse.urlparse(r).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
