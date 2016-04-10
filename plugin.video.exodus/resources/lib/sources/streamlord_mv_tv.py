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

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import cloudflare
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['streamlord.com']
        self.base_link = 'http://www.streamlord.com'
        self.search_link = '/search.html'
        self.user = control.setting('streamlord.user')
        self.password = control.setting('streamlord.pass')


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


                if (self.user == '' or self.password == ''): raise Exception()

                query = urlparse.urljoin(self.base_link, '/login.html')
                post = urllib.urlencode({'username': self.user, 'password': self.password, 'submit': 'Login'})

                try:
                    r, headers, content, cookie = client.source(query, post=post, output='extended')
                    headers = {'Cookie': cookie, 'User-Agent': headers['User-Agent']}
                except:
                    cookie, agent, url = cloudflare.request(query, post=post, output='extended')
                    headers = {'Cookie': cookie, 'User-Agent': agent}


                query = urlparse.urljoin(self.base_link, self.search_link)
                post = urllib.urlencode({'search': title})

                r = cloudflare.source(query, post=post, headers=headers)

                if 'tvshowtitle' in data:
                    r = re.findall('(watch-tvshow-.+?-\d+\.html)', r)
                    r = [(i, re.findall('watch-tvshow-(.+?)-\d+\.html', i)) for i in r]
                else:
                    r = re.findall('(watch-movie-.+?-\d+\.html)', r)
                    r = [(i, re.findall('watch-movie-(.+?)-\d+\.html', i)) for i in r]

                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1])]
                r = [i[0] for i in r][0]

                r = urlparse.urljoin(self.base_link, r)

                url = cloudflare.source(r, headers=headers)

                if 'season' in data and 'episode' in data:
                    r = re.findall('(episode-.+?-.+?\d+.+?\d+-\d+.html)', url)
                    r = [i for i in r if '-s%02de%02d-' % (int(data['season']), int(data['episode'])) in i.lower()][0]
                    r = urlparse.urljoin(self.base_link, r)

                    url = cloudflare.source(r, headers=headers)

            else:
                r = urlparse.urljoin(self.base_link, url)
                cookie, agent, url = cloudflare.request(r, output='extended')
                headers = {'Cookie': cookie, 'User-Agent': agent}



            quality = 'HD' if '-movie-' in url else 'SD'


            func = re.findall('''["']sources['"]\s*:\s*\[(.*?)\]''', url)[0]
            func = re.findall('''['"]*file['"]*\s*:\s*([^\(]+)''', func)[0]

            u = re.findall('function\s+%s[^{]+{\s*([^}]+)' % func, url)[0]
            u = re.findall('\[([^\]]+)[^+]+\+\s*([^.]+).*?getElementById\("([^"]+)', u)[0]

            a = re.findall('var\s+%s\s*=\s*\[([^\]]+)' % u[1], url)[0]
            b = client.parseDOM(url, 'span', {'id': u[2]})[0]

            url = u[0] + a + b
            url = url.replace('"', '').replace(',', '').replace('\/', '/')
            url += '|' + urllib.urlencode(headers)  

            sources.append({'source': 'cdn', 'quality': quality, 'provider': 'Streamlord', 'url': url, 'direct': True, 'debridonly': False, 'autoplay': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


