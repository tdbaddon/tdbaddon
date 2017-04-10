# -*- coding: utf-8 -*-

"""
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
"""

import json
import re
import urllib
import urlparse

from resources.lib.modules import anilist
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import dom_parser
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['foxx.to']
        self.base_link = 'https://foxx.to'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(localtitle, year)
            if not url and title != localtitle: url = self.__search(title, year)
            if not url and self.__is_anime('movie', 'imdb', imdb): url = self.__search(anilist.getAlternativTitle(title), year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(localtvshowtitle, year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(tvshowtitle, year)
            if not url and self.__is_anime('show', 'tvdb', tvdb): url = self.__search(tvmaze.tvMaze().showLookup('thetvdb', tvdb).get('name'), year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')

            if season == 1 and episode == 1:
                season = episode = ''

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'ul', attrs={'class': 'episodios'})
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('[^\'"]*%s' % ('-%sx%s' % (season, episode)))})[0].attrs['href']

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            rels = dom_parser.parse_dom(r, 'nav', attrs={'class': 'player'})
            rels = dom_parser.parse_dom(rels, 'ul', attrs={'class': 'idTabs'})
            rels = dom_parser.parse_dom(rels, 'li')
            rels = [(dom_parser.parse_dom(i, 'a', attrs={'class': 'options'}, req='href'), dom_parser.parse_dom(i, 'img', req='src')) for i in rels]
            rels = [(i[0][0].attrs['href'][1:], re.findall('\/flags\/(\w+)\.png$', i[1][0].attrs['src'])) for i in rels if i[0] and i[1]]
            rels = [i[0] for i in rels if len(i[1]) > 0 and i[1][0].lower() == 'de']

            r = [dom_parser.parse_dom(r, 'div', attrs={'id': i}) for i in rels]

            links = re.findall('''(?:link|file)["']?\s*:\s*["'](.+?)["']''', ''.join([i[0].content for i in r]))
            links += [l.attrs['src'] for l in dom_parser.parse_dom(i, 'iframe', attrs={'class': 'metaframe'}, req='src') for i in r]
            links += [l.attrs['src'] for l in dom_parser.parse_dom(i, 'source', req='src') for i in r]

            for i in links:
                try:
                    i = re.sub('\[.+?\]|\[/.+?\]', '', i)
                    i = client.replaceHTMLCodes(i)

                    if self.domains[0] in i:
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
                        try:
                            valid, host = source_utils.is_host_valid(i, hostDict)
                            if not valid: continue

                            urls = []
                            if 'google' in i: host = 'gvideo'; direct = True; urls = directstream.google(i);
                            if 'google' in i and not urls and directstream.googletag(i):  host = 'gvideo'; direct = True; urls = [{'quality': directstream.googletag(i)[0]['quality'], 'url': i}]
                            elif 'ok.ru' in i: host = 'vk'; direct = True; urls = directstream.odnoklassniki(i)
                            elif 'vk.com' in i: host = 'vk'; direct = True; urls = directstream.vk(i)
                            else: direct = False; urls = [{'quality': 'SD', 'url': i}]

                            for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'de', 'url': x['url'], 'direct': direct, 'debridonly': False})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'details'})
            r = [(dom_parser.parse_dom(i, 'div', attrs={'class': 'title'}), dom_parser.parse_dom(i, 'span', attrs={'class': 'year'})) for i in r]
            r = [(dom_parser.parse_dom(i[0][0], 'a', req='href'), i[1][0].content) for i in r if i[0] and i[1]]
            r = [(i[0][0].attrs['href'], i[0][0].content, i[1]) for i in r if i[0]]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y][0]

            return source_utils.strip_domain(r)
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