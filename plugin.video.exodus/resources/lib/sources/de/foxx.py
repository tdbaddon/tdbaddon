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

import base64
import json
import re
import urllib
import urlparse

from resources.lib.modules import anilist
from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import dom_parser
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['foxx.to']
        self.base_link = 'http://foxx.to'
        self.search_link = '/wp-json/dooplay/search/?keyword=%s&nonce=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            if not url and source_utils.is_anime('movie', 'imdb', imdb): url = self.__search([anilist.getAlternativTitle(title)] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and source_utils.is_anime('show', 'tvdb', tvdb): url = self.__search([tvmaze.tvMaze().showLookup('thetvdb', tvdb).get('name')] + source_utils.aliases_to_array(aliases), year)
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
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'iframe', attrs={'class': 'metaframe'}, req='src')]
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'source', req='src')]

            for i in links:
                try:
                    i = re.sub('\[.+?\]|\[/.+?\]', '', i)
                    i = client.replaceHTMLCodes(i)

                    if self.domains[0] in i:
                        i = client.request(i, referer=url)

                        for x in re.findall('''\(["']?(.*)["']?\)''', i):
                            try: i += jsunpack.unpack(base64.decodestring(re.sub('"\s*\+\s*"', '', x)))
                            except: pass

                        s = re.compile('(eval\(function.*?)</script>', re.DOTALL).findall(i)

                        for x in s:
                            try: i += jsunpack.unpack(x)
                            except: pass

                        i = [(match[0], match[1]) for match in re.findall('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', i, re.DOTALL)]
                        i = [(x[0].replace('\/', '/'), source_utils.label_to_quality(x[1])) for x in i if '/no-video.mp4' not in x[0]]

                        for url, quality in i:
                            sources.append({'source': 'gvideo', 'quality': quality, 'language': 'de', 'url': url, 'direct': True, 'debridonly': False})
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

    def __search(self, titles, year):
        try:
            n = cache.get(self.__get_nonce, 24)

            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])), n)
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)
            r = json.loads(r)
            r = [(r[i].get('url'), r[i].get('title'), r[i].get('extra').get('date')) for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return

    def __get_nonce(self):
        n = client.request(self.base_link)
        try: n = re.findall('nonce"?\s*:\s*"?([0-9a-zA-Z]+)', n)[0]
        except: n = '5d12d0fa54'
        return n
