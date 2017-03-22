# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['movie4k.to', 'movie4k.tv', 'movie.to', 'movie4k.me', 'movie4k.org', 'movie4k.pe', 'movie4k.am']
        self._base_link = None
        self.search_link = '/movies.php?list=search&search=%s'

    @property
    def base_link(self):
        if not self._base_link:
            self._base_link = cache.get(self.__get_base_url, 120, self.domains[0])
        return self._base_link

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(imdb, title, year)
            if not url and title != localtitle: url = self.__search(imdb, localtitle, year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = r.replace('\\"', '"')

            links = client.parseDOM(r, 'tr', attrs={'id': 'tablemoviesindex2'})

            locDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]

            for i in links:
                try:
                    host = client.parseDOM(i, 'img', ret='alt')[0]
                    host = host.split()[0].rsplit('.', 1)[0].strip().lower()
                    host = [x[1] for x in locDict if host == x[0]][0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    url = client.parseDOM(i, 'a', ret='href')[0]
                    url = client.replaceHTMLCodes(url)
                    url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'language': 'de', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            h = urlparse.urlparse(url.strip().lower()).netloc

            r = client.request(url)
            r = r.rsplit('"underplayer"')[0].rsplit("'underplayer'")[0]

            u = re.findall('\'(.+?)\'', r) + re.findall('\"(.+?)\"', r)
            u = [client.replaceHTMLCodes(i) for i in u]
            u = [i for i in u if i.startswith('http') and not h in i]

            url = u[-1].encode('utf-8')
            return url
        except:
            return

    def __search(self, imdb, title, year):
        try:
            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            q = self.search_link % urllib.quote_plus(cleantitle.query(title))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)

            r = client.parseDOM(r, 'TR', attrs={'id': 'coverPreview.+?'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'div', attrs={'style': '.+?'}), client.parseDOM(i, 'img', ret='src')) for i in r]
            r = [(i[0][0].strip(), i[1][0].strip(), i[2], i[3]) for i in r if i[0] and i[1] and i[3]]
            r = [(i[0], i[1], [x for x in i[2] if x.isdigit() and len(x) == 4], i[3]) for i in r]
            r = [(i[0], i[1], i[2][0] if i[2] else '0', i[3]) for i in r]
            r = [i for i in r if any('us_ger_' in x for x in i[3])]
            r = [(i[0], i[1], i[2], [re.findall('(\d+)', x) for x in i[3] if 'smileys' in x]) for i in r]
            r = [(i[0], i[1], i[2], [x[0] for x in i[3] if x]) for i in r]
            r = [(i[0], i[1], i[2], int(i[3][0]) if i[3] else 0) for i in r]
            r = sorted(r, key=lambda x: x[3])[::-1]
            r = [(i[0], i[1], i[2], re.findall('\((.+?)\)$', i[1])) for i in r]
            r = [(i[0], i[1], i[2]) for i in r if not i[3]]
            r = [i for i in r if i[2] in y]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year

            r = [(client.replaceHTMLCodes(i[0]), i[1], i[2]) for i in r]

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]]

            match2 = [i[0] for i in r]
            match2 = [x for y, x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if match: url = match[0]; break
                    r = client.request(urlparse.urljoin(self.base_link, i))
                    r = re.findall('(tt\d+)', r)
                    if imdb in r: url = i; break
                except:
                    pass

            url = urlparse.urljoin(self.base_link, url)

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'http://%s' % domain
                    r = client.request(url, limit=1, timeout='10')
                    r = client.parseDOM(r, 'meta', attrs={'name': 'author'}, ret='content')
                    if r and 'movie4k.to' in r[0].lower():
                        return url
                except:
                    pass
        except:
            pass

        return fallback
