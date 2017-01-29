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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['movieflixter.to']
        self.base_link = 'http://movieflixter.to'
        self.search_link = '/js/suggest/?query=%s+%s'


    def movie(self, imdb, title, localtitle, year):
        try:
            t = cleantitle.get(title)

            q = self.search_link % (urllib.quote_plus(title) , year)
            q = urlparse.urljoin(self.base_link, q)

            r = proxy.request(q, 'url', error=True)
            r = json.loads(r)

            r = [(i['url'], i['value'], i['group']) for i in r if 'url' in i and 'value' in i and 'group' in i]
            r = [(i[0], re.findall('(.+?)\((\d{4})', i[1])) for i in r if i[2] == 'movie']
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i for i in r if t == cleantitle.get(i[1]) and str(year) == i[2]]

            url = urlparse.urlparse(r[0][0]).path

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

            links = client.parseDOM(r, 'tr')

            for i in links:
                try:
                    host = client.parseDOM(i, 'td', attrs = {'class': '.+?'})[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    url = client.parseDOM(i, 'a', ret='href')[0]
                    url = proxy.parse(url)
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


