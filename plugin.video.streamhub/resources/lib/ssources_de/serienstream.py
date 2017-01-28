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

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['serienstream.to']
        self.base_link = 'http://serienstream.to'
        self.search_link = '/ajax/search'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(title)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(title)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = self.__search(tvshowtitle)
            if not url:
                title = cleantitle.local(tvshowtitle, imdb, 'de-DE')
                url = self.__search(title)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            url = url[:-1] if url.endswith('/') else url
            url += '/staffel-%d/episode-%d/' % (int(season), int(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            hostDict = [i[0] for i in hostDict]

            r = client.request(urlparse.urljoin(self.base_link, url))

            r = client.parseDOM(r, 'div', attrs={'class': 'hosterSiteVideo'})
            r = client.parseDOM(r, 'li', attrs={'data-lang-key': '[1|3]'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h4')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(.+?)\s*<br\s*/?>(.+?)$', i[1], re.DOTALL)) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '') for i in r]
            r = [(i[0], i[1], 'HD' if 'hosterhdvideo' in i[2] else 'SD') for i in r if i[1] in hostDict]

            for link, hoster, quality in r:
                sources.append({'source': hoster, 'quality': quality,
                                'provider': 'Serienstream',
                                'language': 'de',
                                'url': link,
                                'direct': False,
                                'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        url = client.request(urlparse.urljoin(self.base_link, url), output='geturl')
        if self.base_link not in url:
            return url

    def __search(self, title):
        try:
            r = {'keyword': cleantitle.getsearch(title)}
            r = urllib.urlencode(r)
            r = client.request(urlparse.urljoin(self.base_link, self.search_link), post=r)

            t = cleantitle.get(title)

            r = json.loads(r)
            r = [(i['link'], re.sub('<.+?>|</.+?>', '', i['title'])) for i in r if 'title' in i and 'link' in i]
            r = [(i[0], i[1], re.findall('(.+?)\s*Movie \d+:.+?$', i[1], re.DOTALL)) for i in r]
            r = [(i[0], i[2][0] if len(i[2]) > 0 else i[1]) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
