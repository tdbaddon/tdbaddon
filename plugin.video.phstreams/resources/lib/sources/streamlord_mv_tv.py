# -*- coding: utf-8 -*-

'''
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
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import cloudflare
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['streamlord.com']
        self.base_link = 'http://www.streamlord.com'
        self.search_link = '/search.html'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                year = data['year']

                query = urlparse.urljoin(self.base_link, self.search_link)
                post = urllib.urlencode({'search': title})

                title = cleantitle.get(title)

                r = cloudflare.source(query, post=post)
                r = client.parseDOM(r, 'div', attrs = {'class': 'item movie'})

                r = [client.parseDOM(i, 'a', ret='href') for i in r]
                r = sum(r, [])
                if 'tvshowtitle' in data: r = [(i, re.findall('watch-tvshow-(.+?)-\d+\.html', i)) for i in r]
                else: r = [(i, re.findall('watch-movie-(.+?)-\d+\.html', i)) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                r = [i for i in r if title == cleantitle.get(i[1])]
                r = [i[0] for i in r][0]

                r = urlparse.urljoin(self.base_link, r)

                cookie, agent, url = cloudflare.request(r, output='extended')

                atr = [client.parseDOM(i, 'li') for i in client.parseDOM(url, 'td')]
                atr = [re.findall('(\d{4})', i[1])[0] for i in atr if len(i) > 1 and i[0] == 'Released']
                atr = [i for i in atr if i == year][0]

                if 'season' in data and 'episode' in data:
                    r = re.findall('href="(episode[^"]*-[Ss]%02d[Ee]%02d-[^"]+)' % (int(data['season']), int(data['episode'])), url)[0]
                    r = urlparse.urljoin(self.base_link, r)
                    cookie, agent, url = cloudflare.request(r, output='extended')


            else:
                r = urlparse.urljoin(self.base_link, url)

                cookie, agent, url = cloudflare.request(r, output='extended')


            quality = 'HD' if '-movie-' in url else 'SD'

            url = re.findall('''["']sources['"]\s*:\s*\[(.*?)\]''', url)[0]
            url = re.findall('''['"]*file['"]*\s*:\s*['"]*([^'"]+)''', url)[0]

            url += '|' + urllib.urlencode({'Cookie': str(cookie), 'User-Agent': agent, 'Referer': r})

            sources.append({'source': 'cdn', 'quality': quality, 'provider': 'Streamlord', 'url': url, 'direct': True, 'debridonly': False, 'autoplay': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


