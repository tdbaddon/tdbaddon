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
from resources.lib.smodules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['hdfilme.tv']
        self.base_link = 'http://hdfilme.tv'
        self.search_link = '/movie-search?key=%s'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(title, year)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(title, year)
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
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            url = self.__search(title, data['year'], season, episode)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(title, data['year'], season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            url = urlparse.urljoin(self.base_link, url)
            result = client.request(url)
            result = re.compile('(\[{".*?}\])').findall(result)[0]
            result = json.loads(result)
            result = [i['file'] for i in result if 'file' in i]

            for i in result:
                try:
                    sources.append(
                        {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'HDFilme',
                         'language': 'de', 'url': i, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)

    def __search(self, title, year, season='0', episode=False):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = client.parseDOM(r, 'ul', attrs={'class': 'products row'})
            r = client.parseDOM(r, 'div', attrs={'class': 'box-product clearfix'})
            r = client.parseDOM(r, 'h3', attrs={'class': 'title-product'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(.+?) \(*(\d{4})', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = [(i[0], i[1], i[2], re.findall('(.+?)\s+(?:staf+el|s)\s+(\d+)', i[1])) for i in r]
            r = [(i[0], i[3][0][0] if len(i[3]) > 0 else i[1], i[2], i[3][0][1] if len(i[3]) > 0 else '0') for i in r]
            r = [(i[0], i[1].replace(' hd', ''), i[2], i[3]) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y and int(i[3]) == int(season)][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            url = url.replace('-info', '-stream')
            if episode: url = urlparse.urlparse(url).path + '?episode=%s' % int(episode)
            return url
        except:
            return
