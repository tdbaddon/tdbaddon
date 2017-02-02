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

import re, json
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdmovie14.net']
        self.base_link = 'http://hdmovie14.net'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNjkxOTYxOTI2MzYxNzgyMDM4ODpkYmljLTZweGt4cyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.moviesearch_link = '/watch/%s-%s'
        self.tvsearch_link = '/watch/%s-%s-season-%s/%s'

    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = '%s %s' % (title, year)
            q = self.search_link.decode('base64') % urllib.quote_plus(q)

            r = client.request(q)
            r = json.loads(r)['results']
            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0].split('%')[0], re.findall('(?:^Watch |)(.+?)(?:\(|)(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i for i in r if '/watch/' in i[0] and not '-season-' in i[0]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

        try:
            url = re.sub('[^A-Za-z0-9]', '-', title).lower()
            url = self.moviesearch_link % (url, year)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, output='geturl')
            if not year in r: raise Exception()

            return url
        except:
            return

    def sources(self, url):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = client.parseDOM(r, 'div', attrs={'class': 'player_wraper'})
            r = client.parseDOM(r, 'iframe', ret='src')

            for u in r:
                try:
                    m = '"(?:url|src)"\s*:\s*"(.+?)"'

                    d = urlparse.urljoin(self.base_link, u)

                    s = client.request(d, referer=url, timeout='10')

                    j = re.compile('<script>(.+?)</script>', re.DOTALL).findall(s)
                    for i in j:
                        try:
                            s += jsunpack.unpack(i)
                        except:
                            pass

                    u = re.findall(m, s)

                    if not u:
                        p = re.findall('location\.href\s*=\s*"(.+?)"', s)
                        if not p: p = ['/player/%s' % d.strip('/').split('/')[-1]]
                        p = urlparse.urljoin(self.base_link, p[0])
                        s = client.request(p, referer=d, timeout='10')
                        u = re.findall(m, s)

                    for i in u:
                        try:
                            sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'],
                                            'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url:
                url = url.replace('http://', 'https://')
            else:
                url = url.replace('https://', 'http://')
            return url
        except:
            return
