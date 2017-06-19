# -*- coding: utf-8 -*-

"""
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
"""

import re, urllib, urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['streamay.ws']
        self.base_link = 'http://streamay.ws'
        self.search_link = '/search'

    def movie(self, imdb, title, localtitle, aliases, year):
        return self.__search(title, localtitle, year, 'Film')

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return self.__search(tvshowtitle, localtvshowtitle, year, 'Série')

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = client.parseDOM(r, 'a', attrs={'class': 'item', 'href': '[^\'"]*/saison-%s/episode-%s[^\'"]*' % (season, episode)}, ret='href')[0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            hostDict.append(['okru', 'ok.ru'])
            locDict = [i[0] for i in hostDict]

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = client.parseDOM(r, 'ul', attrs={'class': '[^\'"]*lecteurs nop[^\'"]*'})
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='data-streamer'), client.parseDOM(i, 'a', ret='data-id')) for i in r]
            r = [(i[0][0], i[1][0], re.search('([a-zA-Z]+)(?:_([a-zA-Z]+))?', i[0][0]), ) for i in r if i[0] and i[1]]
            r = [(i[0], i[1], i[2].group(1), i[2].group(2)) for i in r if i[2]]

            for streamer, id, host, info in r:
                if host not in locDict:
                    continue

                host = [x[1] for x in hostDict if x[0] == host][0]
                link = urlparse.urljoin(self.base_link, '/%s/%s/%s' % (('streamerSerie' if '/series/' in url else 'streamer'), id, streamer))

                sources.append({'source': host, 'quality': 'SD', 'url': link, 'language': 'FR', 'info': info if info else '', 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = json.loads(client.request(url)).get('code')
            url = url.replace('\/', '/')
            url = client.replaceHTMLCodes(url).encode('utf-8')
            if url.startswith('/'): url = 'http:%s' % url
            return url
        except:
            return

    def __search(self, title, localtitle, year, content_type):
        try:
            t = cleantitle.get(title)
            tq = cleantitle.get(localtitle)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            query = urlparse.urljoin(self.base_link, self.search_link)

            post = urllib.urlencode({'k': "%s"}) % tq
            r = client.request(query, post=post)
            r = json.loads(r)

            r = [i.get('result') for i in r if i.get('type', '').encode('utf-8') == content_type]
            r = [(i.get('url'), i.get('originalTitle'), i.get('title'), i.get('anneeProduction', 0), i.get('dateStart', 0)) for i in r]
            r = [(i[0], re.sub('<.+?>|</.+?>', '', i[1] if i[1] else ''), re.sub('<.+?>|</.+?>', '', i[2] if i[2] else ''), i[3] if i[3] else re.findall('(\d{4})', i[4])[0]) for i in r if i[3] or i[4]]
            r = sorted(r, key=lambda i: int(i[3]), reverse=True)  # with year > no year
            r = [i[0] for i in r if i[3] in y and (t.lower() == cleantitle.get(i[1].lower()) or tq.lower() == cleantitle.query(i[2].lower()))][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return