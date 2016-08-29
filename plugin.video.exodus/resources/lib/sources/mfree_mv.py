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


import re,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['m4ufree.info']
        self.base_link = 'http://m4ufree.info'
        self.include_link = '/include/autocomplete.php?q='
        self.search_link = '/tag/%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            r = cache.get(self.mfree_mvcache, 170)

            r = [i for i in r if t == i[0] and year == i[1]][0]


            q = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
            q = urlparse.urljoin(self.base_link, self.search_link % q)

            r = client.request(q)

            r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'top-item'}), client.parseDOM(r, 'a', attrs = {'class': 'top-item'}))
            r = [(i[0], re.sub('^Watch\s*|<.+?>|</.+?>', '', i[1])) for i in r]
            r = [(i[0], re.findall('(.+?) (?:\(|)(\d{4})(?:\)|)$', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def mfree_mvcache(self):
        try:
            u = urlparse.urljoin(self.base_link, self.include_link)

            r = client.request(u).splitlines()
            r = [re.findall('(.+?) (?:\(|)(\d{4})(?:\)|)$', i.strip()) for i in r]
            r = [(cleantitle.get(i[0][0]), i[0][1]) for i in r if len(i) > 0]

            return r
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            quality = client.parseDOM(r, 'h3', attrs = {'title': 'Quality.+?'})[0]
            quality = client.parseDOM(quality, 'span')[0]
            if quality.lower() in ['ts', 'tc', 'cam']: raise Exception()

            url = client.parseDOM(r, 'a', ret='href')
            url = [i for i in url if '-full-movie-' in i][0]

            r = client.request(url)

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

            servers = client.parseDOM(r, 'span', ret='link', attrs = {'class': '[^"]*btn-eps(?:\s+|)'})

            for server in servers:
                try:
                    url = '/demo.php?v=%s' % server
                    url = urlparse.urljoin(self.base_link, url)

                    r += str(client.request(url, headers=headers))
                except:
                    pass

            links = client.parseDOM(r, 'source', ret='src', attrs = {'type': 'video/mp4'})
            links += client.parseDOM(r, 'iframe', ret='src')

            for link in links:
                try:
                    if not link.startswith('http'): link = urlparse.urljoin(self.base_link, link)

                    if not self.base_link in link: raise Exception()

                    url = client.request(link, output='geturl')

                    quality = directstream.googletag(url)[0]['quality']

                    sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'MFree', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


