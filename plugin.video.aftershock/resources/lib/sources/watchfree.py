# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import base64
import re
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['watchfree.to']
        self.base_link = 'http://www.watchfree.to'
        self.moviesearch_link = '/?keyword=%s&search_section=1'
        self.tvsearch_link = '/?keyword=%s&search_section=2'


    def movie(self, imdb, title, year):
        try:
            query = self.moviesearch_link % urllib.quote_plus(cleantitle.query(title))
            query = urlparse.urljoin(self.base_link, query)

            result = str(proxy.request(query, 'item'))
            if 'page=2' in result or 'page%3D2' in result: result += str(proxy.request(query + '&page=2', 'item'))

            result = client.parseDOM(result, 'div', attrs = {'class': 'item'})

            title = 'watch' + cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            r = [(proxy.parse(i[0]), i[1]) for i in result]

            match = [i[0] for i in r if title == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'link_ite')
                    r = re.findall('(tt\d+)', r)
                    if imdb in r: url = i ; break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url):
        try:
            srcs = []

            if url == None: return srcs

            url = urlparse.urljoin(self.base_link, url)

            result = proxy.request(url, 'link_ite')

            links = client.parseDOM(result, 'table', attrs = {'class': 'link_ite.+?'})

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')
                    url = [x for x in url if 'gtfo' in x][-1]
                    url = proxy.parse(url)
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['gtfo'][0]
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = host.encode('utf-8')

                    quality = client.parseDOM(i, 'div', attrs = {'class': 'quality'})
                    if any(x in ['[CAM]', '[TS]'] for x in quality): quality = 'CAM'
                    else:  quality = 'SD'
                    quality = quality.encode('utf-8')

                    srcs.append({'source': host, 'quality': quality, 'provider': 'Watchfree', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return srcs
        except:
            return srcs


    def resolve(self, url, resolverList):
        return url


