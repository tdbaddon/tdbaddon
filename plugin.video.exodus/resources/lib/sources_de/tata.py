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

import json
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['tata.to']
        self.base_link = 'http://tata.to'
        self.search_link = '/filme?suche=%s&type=alle'
        self.ajax_link = '/ajax/stream/%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search_movie(imdb, year)
            return url if url else None
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

            year = re.findall('(\d{4})', premiered)
            year = year[0] if year else data['year']

            url = self.__search(data['localtvshowtitle'], year, season, episode)
            if not url and data['tvshowtitle'] != data['localtvshowtitle']:
                url = self.__search(data['tvshowtitle'], year, season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)
            a = urlparse.urljoin(self.base_link, self.ajax_link % re.findall('-([\w\d]+)$', url)[0])
            result = client.request(a, referer=url)
            result = json.loads(result)
            result = [i['link_mp4'] for i in result['url'] if isinstance(result["url"], list)]
            for i in result:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'de', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return

    def resolve(self, url):
        return url

    def __search_movie(self, imdb, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % imdb)

            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'container'})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'ml-item-content'})
            r = [(dom_parser.parse_dom(i, 'a', attrs={'class': 'ml-image'}, req='href'), dom_parser.parse_dom(i, 'ul', attrs={'class': 'item-params'})) for i in r]
            r = [(i[0][0].attrs['href'], re.findall('calendar.+?>.+?(\d{4})', ''.join([x.content for x in i[1]]))) for i in r if i[0] and i[1]]
            r = [(i[0], i[1][0] if len(i[1]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[1]), reverse=True)  # with year > no year
            r = [i[0] for i in r if i[1] in y][0]

            url = urlparse.urlparse(r).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def __search(self, title, year, season=0, episode=False):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'container'})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'ml-item-content'})

            f = []
            for i in r:
                _url = dom_parser.parse_dom(i, 'a', attrs={'class': 'ml-image'}, req='href')[0].attrs['href']

                _title = re.sub('<.+?>|</.+?>', '', dom_parser.parse_dom(i, 'h6')[0].content).strip()
                try: _title = re.search('(.*?)\s(?:staf+el|s)\s*(\d+)', _title, re.I).group(1)
                except: pass

                _season = '0'

                _year = re.findall('calendar.+?>.+?(\d{4})', ''.join([x.content for x in dom_parser.parse_dom(i, 'ul', attrs={'class': 'item-params'})]))
                _year = _year[0] if len(_year) > 0 else '0'

                if season > 0:
                    s = dom_parser.parse_dom(i, 'span', attrs={'class': 'season-label'})
                    s = dom_parser.parse_dom(s, 'span', attrs={'class': 'el-num'})
                    if s: _season = s[0].content.strip()

                if t == cleantitle.get(_title) and _year in y and int(_season) == int(season):
                    f.append((_url, _year))
            r = f
            r = sorted(r, key=lambda i: int(i[1]), reverse=True)  # with year > no year
            r = [i[0] for i in r if r[0]][0]

            url = source_utils.strip_domain(r)
            if episode:
                r = client.request(urlparse.urljoin(self.base_link, url))
                r = dom_parser.parse_dom(r, 'div', attrs={'class': 'season-list'})
                r = dom_parser.parse_dom(r, 'li')
                r = dom_parser.parse_dom(r, 'a', req='href')
                r = [(i.attrs['href'], i.content) for i in r]
                r = [i[0] for i in r if i[1] and int(i[1]) == int(episode)][0]
                url = source_utils.strip_domain(r)
            return url
        except:
            return
