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
        self.domains = ['tata.to']
        self.base_link = 'http://tata.to'
        self.search_link = '/filme?suche=%s&type=alle'
        self.ajax_link = '/ajax/stream/%s'

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

            return self.__search(cleantitle.local(title, imdb, 'de-DE'), data['year'], season, episode)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None:
                return sources

            url = urlparse.urljoin(self.base_link, url)
            a = urlparse.urljoin(self.base_link, self.ajax_link % re.findall('-([\w\d]+)$', url)[0])
            result = client.request(a, referer=url)
            result = json.loads(result)
            result = [i['link_mp4'] for i in result['url'] if isinstance(result["url"], list)]
            for i in result:
                try:
                    sources.append(
                        {'source': 'gvideo',
                         'quality': directstream.googletag(i)[0]['quality'],
                         'provider': 'Tata',
                         'language': 'de',
                         'url': i,
                         'direct': True,
                         'debridonly': False})
                except:
                    pass

            return sources
        except:
            return

    def resolve(self, url):
        return directstream.googlepass(url)

    def __search(self, title, year, season=0, episode=False):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'container'})
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item-content'})

            f = []
            for i in r:
                _url = client.parseDOM(i, 'a', attrs={'class': 'ml-image'}, ret='href')[0]

                _title = re.sub('<.+?>|</.+?>', '', client.parseDOM(i, 'h6')[0]).strip()
                try: _title = re.search('(.*?)\s(?:staf+el|s)\s*(\d+)', _title, re.I).group(1)
                except: pass

                _season = '0'

                _year = re.findall('calendar.+?>.+?(\d{4})', str(client.parseDOM(i, 'ul', attrs={'class': 'item-params'})))
                _year = _year[0] if len(_year) > 0 else '0'

                if season > 0:
                    s = client.parseDOM(i, 'span', attrs={'class': 'season-label'})
                    s = client.parseDOM(s, 'span', attrs={'class': 'el-num'})
                    if s: _season = s[0].strip()

                if t == cleantitle.get(_title) and _year in y and int(_season) == int(season):
                    f.append(_url)
            r = f

            url = re.findall('(?://.+?|)(/.+)', r[0])[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            if episode:
                r = client.request(urlparse.urljoin(self.base_link, url))
                r = client.parseDOM(r, 'div', attrs={'class': 'season-list'})
                r = client.parseDOM(r, 'li')
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[1]) > 0 and int(i[1][0]) == int(episode)]
                url = re.findall('(?://.+?|)(/.+)', r[0][0])[0]
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
            return url
        except:
            return
