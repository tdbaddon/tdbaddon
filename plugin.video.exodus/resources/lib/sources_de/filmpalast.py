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


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['filmpalast.to']
        self.base_link = 'http://filmpalast.to'
        self.search_link = '/search/title/%s'
        self.stream_link = 'stream/%s/1'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(title)
            if not url and title != localtitle: url = self.__search(localtitle)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle']
            title += ' S%02dE%02d' % (int(season), int(episode))

            url = self.__search(title)
            if not url and data['tvshowtitle'] != data['localtvshowtitle']:
                title = data['localtvshowtitle']
                title += ' S%02dE%02d' % (int(season), int(episode))
                url = self.__search(title)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)

            quality = client.parseDOM(r, 'span', attrs={'id': 'release_text'})[0].split('&nbsp;')[0]
            fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', quality.upper())
            fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
            fmt = [i.lower() for i in fmt]

            if '1080p' in fmt: quality = '1080p'
            elif '720p' in fmt: quality = 'HD'
            else: quality = 'SD'
            if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
            elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

            r = client.parseDOM(r, 'ul', attrs={'class': 'currentStreamLinks'})
            r = [(client.parseDOM(i, 'p', attrs={'class': 'hostName'}),
                  client.parseDOM(i, 'a', attrs={'class': '[^\'"]*stream-src[^\'"]*'}, ret='data-id')) for i in r]
            r = [(i[0][0].lower(), i[1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

            for hoster, id in r:
                if 'openload' in hoster: hoster = 'openload.co'
                if hoster not in hostDict: continue

                sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'info' : '' if len(id) == 1 else 'multi-part', 'url': id, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            h_url = []

            for id in url:
                query = urlparse.urljoin(self.base_link, self.stream_link % id)
                r = client.request(query, XHR=True, post=urllib.urlencode({'streamID': id}))
                r = json.loads(r)
                if 'error' in r and r['error'] == '0' and 'url' in r:
                    h_url.append(r['url'])

            h_url = h_url[0] if len(h_url) == 1 else 'stack://' + ' , '.join(h_url)

            return h_url
        except:
            return

    def __search(self, title):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'article')
            r = [(client.parseDOM(i, 'a', attrs={'class': 'rb'}, ret='href'),
                  client.parseDOM(i, 'a', attrs={'class': 'rb'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
