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


import re,urllib,urlparse,json,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['xmovies8.tv', 'xmovies8.ru']
        self.base_link = 'https://xmovies8.ru'
        self.moviesearch_link = '/movies/search?s=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.searchMovie(title, year)

            if url == None:
                t = cache.get(self.getImdbTitle, 900, imdb)
                if t != title:
                    url = self.searchMovie(t, year)

            return url
        except:
            return

    def getImdbTitle(self, imdb):
        try:
            t = 'http://www.omdbapi.com/?i=%s' % imdb
            t = client.request(t)
            t = json.loads(t)
            t = cleantitle.normalize(t['Title'])
            return t
        except:
            return

    def searchMovie(self, title, year):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.moviesearch_link % (cleantitle.geturl(title.replace('\'', '-'))))
            r = client.request(url)
            t = cleantitle.get(title)
            r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t in cleantitle.get(i[1]) and year == i[2]][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url.encode('utf-8')
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
            url = urlparse.urljoin(self.base_link, url)
            url = path = re.sub('/watching.html$', '', url.strip('/'))
            url = referer = url + '/watching.html'
            p = client.request(url)
            p = re.findall('load_player\(.+?(\d+)', p)
            p = urllib.urlencode({'id': p[0]})
            headers = {
            'Accept-Formating': 'application/json, text/javascript',
            'Server': 'cloudflare-nginx',
            'Referer': referer}
            r = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v3')
            r = client.request(r, post=p, headers=headers, XHR=True)
            url = json.loads(r)['value']
            url = client.request(url, headers=headers, XHR=True, output='geturl')

            if 'openload.io' in url or 'openload.co' in url or 'oload.tv' in url:
                sources.append({'source': 'openload.co', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,'debridonly': False})
                raise Exception()

            r = client.request(url, headers=headers, XHR=True)
            try:
                src = json.loads(r)['playlist'][0]['sources']
                links = [i['file'] for i in src if 'file' in i]
                for i in links:
                    try:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en',
                             'url': i, 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            for i in range(3):
                u = directstream.googlepass(url)
                if not u == None: break

            return u
        except:
            return