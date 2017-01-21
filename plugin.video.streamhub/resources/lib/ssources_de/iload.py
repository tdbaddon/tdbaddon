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
        self.domains = ['iload.to']
        self.base_link = 'http://iload.to'
        self.search_link_mv = '/suche/%s/Filme'
        self.search_link_tv = '/suche/%s/Serien'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(self.search_link_mv, imdb, title)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(self.search_link_mv, imdb, title)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = self.__search(self.search_link_tv, imdb, tvshowtitle)
            if not url:
                title = cleantitle.local(tvshowtitle, imdb, 'de-DE')
                url = self.__search(self.search_link_tv, imdb, title)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)
            r = client.parseDOM(r, 'td', attrs={'data-title-name': 'Season %02d' % int(season)})
            r = client.parseDOM(r, 'a', ret='href')[0]
            r = client.request(urlparse.urljoin(self.base_link, r))
            r = client.parseDOM(r, 'td', attrs={'data-title-name': 'Episode %02d' % int(episode)})
            r = client.parseDOM(r, 'a', ret='href')[0]
            return r
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)
            r = client.parseDOM(r, 'div', attrs={'id': 'Module'})
            r = [(r, client.parseDOM(r, 'a', attrs={'href': '[^\'"]*xrel_search_query[^\'"]*'}, ret='href'))]
            r = [(i[0], i[1][0] if len(i[1]) > 0 else '') for i in r]

            rels = client.parseDOM(r[0][0], 'a', attrs={'href': '[^\'"]*ReleaseList[^\'"]*'}, ret='href')
            if rels and len(rels) > 1:
                r = []
                for rel in rels:
                    relData = client.request(urlparse.urljoin(self.base_link, rel))
                    relData = client.parseDOM(relData, 'table', attrs={'class': 'release-list'})
                    relData = client.parseDOM(relData, 'tr', attrs={'class': 'row'})
                    relData = [(client.parseDOM(i, 'td', attrs={'class': '[^\'"]*list-name[^\'"]*'}),
                                client.parseDOM(i, 'img', attrs={'class': 'countryflag'}, ret='alt'),
                                client.parseDOM(i, 'td', attrs={'class': 'release-types'})
                                ) for i in relData]
                    relData = [(i[0][0], i[1][0].lower(), i[2][0]) for i in relData if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
                    relData = [(i[0], i[2]) for i in relData if i[1] == 'deutsch']
                    relData = [(i[0], client.parseDOM(i[1], 'img', attrs={'class': 'release-type-stream'})) for i in relData]
                    relData = [i[0] for i in relData if len(i[1]) > 0]
                    #relData = client.parseDOM(relData, 'a', ret='href')[:3]
                    relData = client.parseDOM(relData, 'a', ret='href')

                    for i in relData:
                        i = client.request(urlparse.urljoin(self.base_link, i))
                        i = client.parseDOM(i, 'div', attrs={'id': 'Module'})
                        i = [(i, client.parseDOM(i, 'a', attrs={'href': '[^\'"]*xrel_search_query[^\'"]*'}, ret='href'))]
                        r += [(x[0], x[1][0] if len(x[1]) > 0 else '') for x in i]

            r = [(client.parseDOM(i[0], 'div', attrs={'id': 'ModuleReleaseDownloads'}), i[1]) for i in r]
            r = [(re.compile('(<a.+?/a>)', re.DOTALL).findall(i[0][0]), i[1]) for i in r if len(i[0]) > 0]

            for items, rel in r:
                rel = urlparse.urlparse(rel).query
                rel = urlparse.parse_qs(rel)['xrel_search_query'][0]

                fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', rel.upper())
                fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                fmt = [i.lower() for i in fmt]

                if '1080p' in fmt: quality = '1080p'
                elif '720p' in fmt: quality = 'HD'
                else: quality = 'SD'
                if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                info = []
                if '3d' in fmt: info.append('3D')
                if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

                items = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in items]
                items = [(i[0][0], i[1][0]) for i in items if len(i[0]) > 0 and len(i[1]) > 0]
                items = [(i[0], client.parseDOM(i[1], 'img', ret='src')) for i in items]
                items = [(i[0], i[1][0]) for i in items if len(i[1]) > 0]
                items = [(i[0], re.findall('.+/(.+\.\w+)\.\w+', i[1])) for i in items]
                items = [(i[0], i[1][0]) for i in items if len(i[1]) > 0 and i[1][0].lower() in hostDict]

                for link, hoster in items:
                    sources.append({'source': hoster, 'quality': quality, 'provider': 'ILOAD', 'language': 'de', 'url': link, 'info': info, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = client.request(urlparse.urljoin(self.base_link, url), output='geturl')
            return url if self.base_link not in url else None
        except:
            return

    def __search(self, search_link, imdb, title):
        try:
            query = search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'big-list'})
            r = client.parseDOM(r, 'table', attrs={'class': 'row'})
            r = client.parseDOM(r, 'td', attrs={'class': 'list-name'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = client.parseDOM(r, 'a', attrs={'href': '[^\'"]+/tt\d+[^\'"]+'}, ret='href')
            r = [re.findall('.+?(tt\d+).*?', i) for i in r]
            r = [i[0] for i in r if len(i) > 0]

            return url if imdb in r else None
        except:
            return
