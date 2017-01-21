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
        self.domains = ['kinox.to']
        self.base_link = 'http://kinox.to'
        self.search_link = '/Search.html?q=%s'
        self.get_links_epi = '/aGET/MirrorByEpisode/?Addr=%s&SeriesID=%s&Season=%s&Episode=%s'
        self.mirror_link = '/aGET/Mirror/%s&Hoster=%s&Mirror=%s'

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

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            hostDict = [i[0] for i in hostDict]

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = urlparse.urljoin(self.base_link, data['url'])
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False

            r = client.request(url)

            if season and episode:
                r = client.parseDOM(r, 'select', attrs={'id': 'SeasonSelection'}, ret='rel')[0]
                r = client.replaceHTMLCodes(r)[1:]
                r = urlparse.parse_qs(r)
                r = dict([(i, r[i][0]) if r[i] else (i, '') for i in r])
                r = urlparse.urljoin(self.base_link, self.get_links_epi % (r['Addr'], r['SeriesID'], season, episode))
                r = client.request(r)

            r = client.parseDOM(r, 'ul', attrs={'id': 'HosterList'})[0]
            r = re.compile('(<li.+?/li>)', re.DOTALL).findall(r)
            r = [(client.parseDOM(i, 'li', attrs={'id': 'Hoster_\d+'}, ret='rel'),
                  client.parseDOM(i, 'li', attrs={'id': 'Hoster_\d+'})) for i in r]
            r = [(client.replaceHTMLCodes(i[0][0]), i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('class="Named"[^>]*>([^<]+).*?(\d+)/(\d+)', i[1])) for i in r]
            r = [(i[0], i[1][0][0].lower().rsplit('.', 1)[0], i[1][0][1], i[1][0][2]) for i in r if len(i[1]) > 0]
            r = [(i[0], i[1], i[3]) for i in r if i[1] in hostDict]

            for i in r:
                u = urlparse.parse_qs('&id=%s' % i[0])
                u = dict([(x, u[x][0]) if u[x] else (x, '') for x in u])
                for x in range(0, int(i[2])):
                    url = self.mirror_link % (u['id'], u['Hoster'], x + 1)
                    if season and episode: url += "&Season=%s&Episode=%s" % (season, episode)
                    try:
                        sources.append(
                            {'source': i[1], 'quality': 'SD',
                             'provider': 'KinoX',
                             'language': 'de',
                             'url': url, 'direct': False,
                             'debridonly': False})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, referer=self.base_link)
            r = json.loads(r)['Stream']
            r = [(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'iframe', ret='src'))]
            r = [i[0][0] if len(i[0]) > 0 else i[1][0] for i in r if len(i[0]) > 0 or len(i[1]) > 0][0]

            if not r.startswith('http'):
                r = urlparse.parse_qs(r)
                r = [r[i][0] if r[i] and r[i][0].startswith('http') else (i, '') for i in r][0]

            return r
        except:
            return

    def __search(self, imdb):
        try:
            l = ['1', '15']

            r = client.request(urlparse.urljoin(self.base_link, self.search_link % imdb))
            r = client.parseDOM(r, 'table', attrs={'id': 'RsltTableStatic'})
            r = client.parseDOM(r, 'tr')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'),
                  client.parseDOM(i, 'img', attrs={'alt': 'language'}, ret='src')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1], re.findall('.+?(\d+)\.', i[2])) for i in r]
            r = [(i[0], i[1], i[2][0] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]))  # german > german/subbed
            r = [i[0] for i in r if i[2] in l][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return
