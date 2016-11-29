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

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['blackcinema.org']
        self.base_link = 'http://blackcinema.org'
        self.moviesearch_link = '/movies/%s/'
        self.tvsearch_link = 'tvshows/page/%s/'


    def movie(self, imdb, title, year):
        try:
            url = self.moviesearch_link % cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, url)

            url = client.request(url, output='geturl')
            if url == None: raise Exception()

            r = client.request(url, limit='1')
            r = client.parseDOM(r, 'title')[0]
            if not year in r: raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            t = cleantitle.get(tvshowtitle)
            r = cache.get(self.bcinema_tvcache, 120)
            r = [i for i in r if t == i[1] and year == i[2]]
            url = r[0][0]
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = '/episodes/%s-%01dx%01d/' % (url.strip('/').split('/')[-1], int(season), int(episode))
            return url 
        except:
            return


    def bcinema_tvcache(self):
        try:
            r = ''
            for i in range(1, 3):
                u = urlparse.urljoin(self.base_link, self.tvsearch_link % str(i))
                r += str(client.request(u))
            r = client.parseDOM(r, 'article', attrs = {'id': 'post-.+?'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), client.parseDOM(i, 'span')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1] and i[2]]
            r = [(urlparse.urlparse(i[0]).path, cleantitle.get(i[1]), i[2]) for i in r]
            return r
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = client.parseDOM(r, 'iframe', ret='src')

            for u in r:
                try:
                    u = 'http://' + u.split('//', 1)[-1]
                    if not self.base_link in u: raise Exception()

                    u = client.request(u)
                    u = re.findall('file\s*:\s*"(.+?)"', u)

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Bcinema', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
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


