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


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['moviewatcher.io']
        self.base_link = 'http://moviewatcher.io'
        self.search_link = '/search?query=%s&type=movies'
        self.search_link_2 = '/ajax?query=%s'


    def movie(self, imdb, title, localtitle, year):
        try:
            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1), '0']

            q = self.search_link_2 % urllib.quote_plus(title)
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q, XHR=True)
            r = str(r).replace('\\', '')
            r = re.findall('\[\s*"(.+?)".+?\((\d{4})\)"\s*,\s*".+?","(.+?)"\s*\]', r)
            r = [i[2] for i in r if t == cleantitle.get(i[0]) and year == i[1]]

            if r: return re.findall('(?://.+?|)(/.+)', r[0])[0]

            q = self.search_link % urllib.quote_plus(cleantitle.query(title))
            q = urlparse.urljoin(self.base_link, q)

            r = proxy.request(q, 'movies')

            r = client.parseDOM(r, 'div', attrs = {'class': 'one_movie.+?'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs = {'class': 'movie.+?'})) for i in r]
            r = [(proxy.parse(i[0][0]), i[1][0]) for i in r if i[0] and i[1]]
            r = [(i[0], i[1], re.findall('(\d{4})', i[0])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if i[2]]
            r = [i for i in r if i[2] in y]

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if match: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'movies')
                    r = re.findall('(tt\d+)', r)
                    if imdb in r: url = i ; break
                except:
                    pass

            url = urlparse.urljoin(self.base_link, url)

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = proxy.request(url, 'movies')

            links = client.parseDOM(r, 'a', attrs = {'class': 'full-tor.+?'})

            for i in links:
                try:
                    host = client.parseDOM(i, 'div', attrs = {'class': 'small_server'})[0]
                    host = host.strip().lower().split()[-1]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    url = re.findall("'(/redirect/[^']+)", i)[0]
                    url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return proxy.geturl(url)


