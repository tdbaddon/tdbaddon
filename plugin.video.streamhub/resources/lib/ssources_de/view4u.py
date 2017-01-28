# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper4k

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

import re
import urllib
import urlparse

from resources.lib.smodules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['view4u.cc']
        self.base_link = 'http://view4u.cc'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(imdb)
            if url:
                return urllib.urlencode({'url': url})
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            return self.movie(imdb, tvshowtitle, year)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'season': season, 'episode': episode})
            return urllib.urlencode(data)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = urlparse.urljoin(self.base_link, data['url'])
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False

            data = client.request(url)

            if not season and not episode:
                data = client.parseDOM(data, 'div', attrs={'id': 'film_links'})
                data = [i.splitlines() for i in data][0]
            else:
                data = client.parseDOM(data, 'div', attrs={'id': 'seral_links'})
                data = re.compile('(\d+)\.(\d+)\s+(.*?)(?=\d+\.\d+\s+|$)', re.IGNORECASE | re.DOTALL).findall(data[0])
                data = [(i[2]) for i in data if int(i[0]) == int(season) and int(i[1]) == int(episode)]
                data = [i.splitlines() for i in data][0]

            for url in data:
                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                if not host in hostDict: continue

                sources.append({'source': host, 'quality': 'SD',
                                'provider': 'View4u',
                                'language': 'de',
                                'url': url,
                                'direct': False,
                                'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, imdb):
        try:
            r = {'story': imdb, 'do': 'search', 'subaction': 'search'}
            r = urllib.urlencode(r)
            r = client.request(self.base_link, post=r)

            r = client.parseDOM(r, 'div', attrs={'class': 'film-table'})
            r = [client.parseDOM(i, 'a', attrs={'class': ''}, ret='href') for i in r]
            r = [i[0] for i in r if len(i[0]) > 0]

            if len(r) > 1:
                for i in r:
                    data = client.request(i)
                    data = client.parseDOM(data, 'span', attrs={'class': 'imdb-rate'}, ret='onclick')
                    data = [d for d in data if imdb in ("'%s'" % imdb) in d]

                    if len(data) >= 1:
                        url = i
            else:
                url = r[0]

            if url:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                return url
        except:
            return
