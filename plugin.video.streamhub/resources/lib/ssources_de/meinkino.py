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
from resources.lib.smodules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['meinkino.to']
        self.base_link = 'http://meinkino.to'
        self.search_link = '/filter?type=%s&veroeffentlichung[]=%s&suche=%s'
        self.get_link = '/geturl/%s'

    def movie(self, imdb, title, year):
        try:
            url = self.__search(title, 'filme', year)
            if not url:
                title = cleantitle.local(title, imdb, 'de-DE')
                url = self.__search(title, 'filme', year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            return urllib.urlencode(url)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            return self.__search(cleantitle.local(title, imdb, 'de-DE'), 'tv', data['year'], season, episode)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            query = urlparse.urljoin(self.base_link, self.get_link % (re.findall('-id(.*?)$', url)[0]))
            header = {'X-Requested-With': 'XMLHttpRequest',
                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

            r = client.request(query, post='', headers=header)
            r = json.loads(r)
            r = [i[1] for i in r.items()]

            for i in r:
                if isinstance(i, list):
                    for urlData in i:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(urlData['link_mp4'])[0]['quality'],
                             'provider': 'MeinKino',
                             'language': 'de',
                             'url': urlData['link_mp4'], 'direct': True,
                             'debridonly': False})
                elif isinstance(i, dict):
                    for key, value in i.iteritems():
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(value.strip().lower()).netloc)[0]
                        if not host in hostDict: continue

                        sources.append({'source': host, 'quality': 'SD',
                                        'provider': 'MeinKino',
                                        'language': 'de',
                                        'url': value, 'direct': False,
                                        'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, title, type, year, season=0, episode=False):
        try:
            query = self.search_link % (type, year, urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-items'})
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', attrs={'class': 'ml-name'}, ret='href'),
                  client.parseDOM(i, 'a', attrs={'class': 'ml-name'})) for i in r]
            r = [(i[0][0], re.sub('<.+?>|</.+?>', '', i[1][0]).strip()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(.+?)\s+(?:staf+el|s)\s+(\d+)', i[1].lower())) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and int(i[2]) == int(season)][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            if episode:
                query = urlparse.urljoin(self.base_link, url)
                r = client.request(query)
                r = client.parseDOM(r, 'div', attrs={'class': 'season-list'})
                r = client.parseDOM(r, 'li')
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[1]) > 0 and int(i[1][0]) == int(episode)]
                url = re.findall('(?://.+?|)(/.+)', r[0][0])[0]
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
            return url
        except:
            return
