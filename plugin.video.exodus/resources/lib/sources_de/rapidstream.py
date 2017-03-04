# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper2k4

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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import jsunpack
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['rapidstream.to']
        self.base_link = 'https://rapidstream.to'
        self.search_link = '/wp-admin/admin-ajax.php?s=%s&post_type=%s&action=dwls_search'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(title, 'movies')
            if not url and title != localtitle: url = self.__search(localtitle, 'movies')
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(tvshowtitle, 'tvshows')
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(localtvshowtitle, 'tvshows')
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')

            if season == 1 and episode == 1:
                season = episode = ''

            u = re.findall('/([^/]+)', url)[-1]
            u += '-%sx%s' % (season, episode)

            r = client.request(url)

            r = client.parseDOM(r, 'a', attrs={'href': '[^\'"]*%s[^\'"]*' % u.replace('-', '\-')}, ret='href')[0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')

            r = client.request(url)

            r = client.parseDOM(r, 'iframe', attrs={'class': '[^\'"]*metaframe[^\'"]*'}, ret='src')

            for i in r:
                try:
                    if 'player.rapidstream.to' in i:
                        if i.endswith('.mp4'): raise Exception()

                        i = client.request(i, referer=url)

                        s = re.compile('(eval\(function.*?)</script>', re.DOTALL).findall(i)

                        for i in s:
                            try: i += jsunpack.unpack(i)
                            except: pass

                        i = re.findall('file"?\s*:\s*"(.+?)"', i)

                        for u in i:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(u)[0]['quality'], 'language': 'de', 'url': u, 'direct': True, 'debridonly': False})
                            except: pass
                    else:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i.strip().lower()).netloc)[0]
                        if not host in hostDict: raise Exception()

                        sources.append({'source': host, 'quality': 'SD', 'language': 'de', 'url': i, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, title, post_type):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)), post_type)
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query, XHR=True)

            r = json.loads(r)
            r = r.get('results', [])
            r = [(i['permalink'], i['post_title']) for i in r if 'permalink' in i and 'post_title' in i]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return