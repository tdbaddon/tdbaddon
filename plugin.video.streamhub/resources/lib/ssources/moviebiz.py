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

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client
from resources.lib.smodules import proxy


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['movie25.biz']
        self.base_link = 'http://movie25.biz'
        self.search_link = '/advanced-search.php?q=%s&year_from=%s&year_to=%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)
            y = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            q = self.search_link % (urllib.quote_plus(cleantitle.query(title)), str(int(year)-1), str(int(year)+1))
            q = urlparse.urljoin(self.base_link, q)

            r = proxy.request(q, 'movie_table')

            r = client.parseDOM(r, 'div', attrs = {'class': 'movie_table'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h1')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            r = [(i[0], client.parseDOM(i[1], 'a')) for i in r]
            r = [(i[0], i[1][0]) for i in r if i[1]]
            r = [i for i in r if any(x in i[1] for x in y)]

            r = [(proxy.parse(i[0]), i[1]) for i in r]

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if match: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'movie25')
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
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = proxy.request(url, 'movie25')
            r = r.replace('\n','')

            quality = re.findall('>Links - Quality(.+?)<', r)
            quality = quality[0].strip() if quality else 'SD'
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = client.parseDOM(r, 'a', ret='href')
            links = [x for y,x in enumerate(links) if x not in links[:y]]

            for i in links:
                try:
                    url = i
                    url = proxy.parse(url)
                    url = url.strip('/').split('/')[-1]
                    url = url.decode('base64')
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


