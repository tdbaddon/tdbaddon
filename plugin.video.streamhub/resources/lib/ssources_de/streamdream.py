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

import re, urllib, urlparse, json

from resources.lib.smodules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['streamdream.ws']
        self.base_link = 'http://streamdream.ws'
        self.search_link = '/searchy.php?ser=%s'
        self.hoster_link = '/episodeholen2.php'

    def movie(self, imdb, title, year):
        try:
            imdb = re.sub('[^0-9]', '', imdb)
            url = self.__search(imdb)
            if url:
                return urllib.urlencode({'url': url, 'imdb': imdb})
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

            if season and episode:
                header = {'X-Requested-With': 'XMLHttpRequest',
                          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                r = {'imdbid': data['imdb'], 'language': 'de', 'season': season, 'episode': episode}
                r = urllib.urlencode(r)
                r = client.request(urlparse.urljoin(self.base_link, self.hoster_link), headers=header, post=r)
            else:
                r = client.request(url)

            r = client.parseDOM(r, 'div', attrs={'class': 'linkbox'})[0]
            r = re.compile('(<a.+?/a>)', re.DOTALL).findall(r)
            r = [(client.parseDOM(i, 'a', ret='href'),
                  client.parseDOM(i, 'img', attrs={'class': '.*linkbutton'}, ret='class')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], 'HD' if i[1].startswith('hd') else 'SD') for i in r]

            for url, quli in r:
                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                if not host in hostDict: continue

                sources.append({'source': host, 'quality': quli,
                                'provider': 'StreamDream',
                                'language': 'de',
                                'url': url, 'direct': False,
                                'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, imdb):
        try:
            r = client.request(urlparse.urljoin(self.base_link, self.search_link % imdb))
            r = client.parseDOM(r, 'a', ret='href')
            r = [i for i in r if len(i[0]) > 0]

            if len(r) > 1:
                for i in r:
                    data = client.request(urlparse.urljoin(self.base_link, i))
                    data = re.compile('(imdbid\s*[=|:]\s*"%s"\s*,)' % imdb, re.DOTALL).findall(data)

                    if len(data) >= 1:
                        url = i
            else:
                url = r[0]

            if url:
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                return url
        except:
            return
