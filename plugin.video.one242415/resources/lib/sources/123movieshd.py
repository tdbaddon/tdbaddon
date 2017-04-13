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

import re,urllib,urlparse,base64,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movieshd.tv']
        self.base_link = 'https://123movieshd.tv'
        self.search_link = '/movie/search/%s'

    def getImdbTitle(self, imdb):
        try:
            t = 'http://www.omdbapi.com/?i=%s' % imdb
            t = client.request(t)
            t = json.loads(t)
            t = cleantitle.normalize(t['Title'])
            return t
        except:
            return

    def movie(self, imdb, title, localtitle, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return        

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %01d' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'h2'))
            r = [i[0] for i in r if cleantitle.get(search) == cleantitle.get(i[1])][0]
            url = urlparse.urljoin(self.base_link, '%s/watching.html' % r)
            return url
        except:
            return

    def searchMovie(self, title):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'h2'))
            r = [i[0] for i in r if cleantitle.get(title) == cleantitle.get(i[1])][0]
            url = urlparse.urljoin(self.base_link, '%s/watching.html' % r)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                if 'tvshowtitle' in data:
                    url = '%s/film/%s-season-%01d/watching.html' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']))
                    url = client.request(url, timeout='10', output='geturl')

                    if url == None:
                        url = self.searchShow(data['tvshowtitle'], data['season'])

                    if url == None:
                        t = cache.get(self.getImdbTitle, 900, data['imdb'])
                        if data['tvshowtitle'] != t:
                            url = self.searchShow(t, data['season'])

                else:
                    url = '%s/film/%s/watching.html' % (self.base_link, cleantitle.geturl(data['title']))
                    url = client.request(url, timeout='10', output='geturl')

                    if url == None:
                        url = self.searchMovie(data['title'])

                    if url == None:
                        t = cache.get(self.getImdbTitle, 900, data['imdb'])
                        if data['title'] != t:
                            url = self.searchMovie(t)

                if url == None: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
            if 'tvshowtitle' in data:
                ep = data['episode']
                links = client.parseDOM(r, 'a', attrs = {'episode-data': ep }, ret = 'player-data')
            else:
                links = client.parseDOM(r, 'a', ret = 'player-data')


            for link in links:
                if '123movieshd' in link or 'seriesonline' in link:
                    r = client.request(link, timeout='10')
                    r = re.findall('(https:.*?redirector.*?)[\'\"]', r)

                    for i in r:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                else:
                    try:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                        if not host in hostDict: raise Exception()
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                    except:
                        pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url


