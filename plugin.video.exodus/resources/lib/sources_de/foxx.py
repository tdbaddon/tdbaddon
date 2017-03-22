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

import re, urllib, urlparse, json, base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze
from resources.lib.modules import anilist


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['foxx.to']
        self.base_link = 'https://foxx.to'
        self.search_link = '/wp-admin/admin-ajax.php?s=%s&post_type=%s&action=search_in_place'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(title, 'movies')
            if not url and title != localtitle: url = self.__search(localtitle, 'movies')
            if not url and self.__is_anime('movie', 'imdb', imdb): url = self.__search(anilist.getAlternativTitle(title), 'movies')
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(tvshowtitle, 'tvshows')
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(localtvshowtitle, 'tvshows')
            if not url and self.__is_anime('show', 'tvdb', tvdb): url = self.__search(tvmaze.tvMaze().showLookup('thetvdb', tvdb).get('name'), 'tvshows')
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

            u = re.findall('/([^/]+)', url)[-1].split('-')
            u = '-'.join(u[:(len(u) - 3)])
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

            r = client.request(url, headers={'Accept-Encoding': 'gzip'})

            rels = client.parseDOM(r, 'nav', attrs={'class': 'player'})
            rels = client.parseDOM(rels, 'ul', attrs={'class': 'idTabs'})
            rels = client.parseDOM(rels, 'li')
            rels = [(client.parseDOM(i, 'a', attrs={'class': 'options'}, ret='href'), client.parseDOM(i, 'img', ret='src')) for i in rels]
            rels = [(i[0][0][1:], re.findall('\/flags\/(\w+)\.png$', i[1][0])) for i in rels if len(i[0]) > 0 and len(i[1]) > 0]
            rels = [i[0] for i in rels if len(i[1]) > 0 and i[1][0].lower() == 'de']

            r = [client.parseDOM(r, 'div', attrs={'id': i}) for i in rels]
            r = [(re.findall('link"?\s*:\s*"(.+?)"', i[0]), client.parseDOM(i, 'iframe', attrs={'class': '[^\'"]*metaframe[^\'"]*'}, ret='src')) for i in r]
            r = [i[0][0] if len(i[0]) > 0 else i[1][0] for i in r if len(i[0]) > 0 or len(i[1]) > 0]

            for i in r:
                try:
                    i = re.sub('\[.+?\]|\[/.+?\]', '', i)
                    i = client.replaceHTMLCodes(i)

                    if self.base_link in i:
                        i = client.request(i, referer=url)

                        s = re.compile('(eval\(function.*?)</script>', re.DOTALL).findall(i)

                        for x in s:
                            try: i += jsunpack.unpack(x)
                            except: pass

                        i = re.findall('file"?\s*:\s*"(.+?)"', i)

                        for u in i:
                            try:
                                u = u.replace('\\/', '/').replace('\/', '/')
                                u = client.replaceHTMLCodes(u).encode('utf-8')

                                sources.append({'source': 'gvideo', 'quality': directstream.googletag(u)[0]['quality'], 'language': 'de', 'url': u, 'direct': True, 'debridonly': False})
                            except:
                                pass
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
            r = r.get(post_type, [])
            r = [(i['link'], i['title']) for i in r if 'link' in i and 'title' in i]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    @staticmethod
    def __is_anime(content, type, type_id):
        try:
            r = 'search/%s/%s?type=%s&extended=full' % (type, type_id, content)
            r = json.loads(trakt.getTrakt(r))
            r = r[0].get(content, []).get('genres', [])
            return 'anime' in r or 'animation' in r
        except:
            return False