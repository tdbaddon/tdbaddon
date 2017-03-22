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

import base64
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['streamit.ws']
        self.base_link = 'https://streamit.ws'
        self.search_link = '/livesearch.php'
        self.episode_link = '/lade_episode.php'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = self.__search(title, year)
            if not url and title != localtitle: url = self.__search(localtitle, year)
            return urllib.urlencode({'url': url, 'imdb': re.sub('[^0-9]', '', imdb)}) if url else None
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(tvshowtitle, year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(localtvshowtitle, year)
            return urllib.urlencode({'url': url, 'imdb': re.sub('[^0-9]', '', imdb)}) if url else None
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
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
            if not url:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = urlparse.urljoin(self.base_link, data.get('url',''))
            imdb = data.get('imdb')
            season = data.get('season')
            episode = data.get('episode')

            if season and episode and imdb:
                r = urllib.urlencode({'val': 's%se%s' % (season, episode), 'IMDB': imdb})
                r = client.request(urlparse.urljoin(self.base_link, self.episode_link), XHR=True, post=r)
            else:
                r = client.request(url)

            l = client.parseDOM(r, 'select', attrs={'id': 'sel_sprache'})
            l = client.parseDOM(l, 'option', ret='id')

            r = [(client.parseDOM(r, 'div', attrs={'id': i})) for i in l if i == 'deutsch']
            r = [(i[0], client.parseDOM(i[0], 'option', ret='id')) for i in r]
            r = [(id, client.parseDOM(content, 'div', attrs={'id': id})) for content, ids in r for id in ids]
            r = [(re.findall('hd(\d{3,4})', i[0]), client.parseDOM(i[1], 'a', ret='href')) for i in r if i[1]]
            r = [(i[0][0] if i[0] else '0', i[1]) for i in r]

            links = [(x[1], '4K') for x in r if int(x[0]) >= 2160]
            links += [(x[1], '1440') for x in r if int(x[0]) >= 1440]
            links += [(x[1], '1080p') for x in r if int(x[0]) >= 1080]
            links += [(x[1], 'HD') for x in r if 720 <= int(x[0]) < 1080]
            links += [(x[1], 'SD') for x in r if int(x[0]) < 720]

            for urls, quality in links:
                for link in urls:
                    try:
                        data = urlparse.parse_qs(urlparse.urlparse(link).query, keep_blank_values=True)

                        if 'm' in data:
                            data = data.get('m')[0]
                            link = base64.b64decode(data)

                        link = link.strip()

                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                        if not host in hostDict: continue

                        sources.append({'source': host, 'quality': quality, 'language': 'de', 'url': link, 'direct': False, 'debridonly': False, 'checkquality': True})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, title, year):
        try:
            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(urlparse.urljoin(self.base_link, self.search_link), post=urllib.urlencode({'val': title}), XHR=True)
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r if i]
            r = [(i[0][0], i[1][0], re.findall('\((\d{4})', i[1][0])) for i in r if i[0] and i[1]]
            r = [(i[0], i[1], i[2][0] if i[2] else '0') for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return