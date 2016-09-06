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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['xmovies8.tv']
        self.base_link = 'http://xmovies8.tv'
        self.search_link = '/movies/search?s=%s'


    def movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)

            for i in range(5):
                r = client.request(query)
                if not r == None: break

            t = cleantitle.get(title)

            r = client.parseDOM(r, 'div', attrs = {'class': 'col-lg.+?'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h2', attrs = {'class': 'c-title.+?'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if len(i[2]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            u = urlparse.urljoin(self.base_link, url)
            r = u.replace('/watching.html', '') + '/watching.html'

            for i in range(5):
                post = client.request(u)
                if not post == None: break

            post = re.findall('movie=(\d+)', post)[0]
            post = urllib.urlencode({'id': post, 'episode_id': '0', 'link_id': '0', 'from': 'v3'})

            headers = {
            'Accept-Formating': 'application/json, text/javascript',
            'X-Requested-With': 'XMLHttpRequest',
            'Server': 'cloudflare-nginx',
            'Referer': r}

            url = urlparse.urljoin(self.base_link, '/ajax/movie/load_episodes')

            for i in range(5):
                r = client.request(url, post=post, headers=headers)
                if not r == None: break

            r = re.findall("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?", r)
            r = list(set(r))
            r = [i for i in r if i[1] == '0' or int(i[1]) >= 720]


            links = []

            for p in r:
                try:
                    play = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v2')

                    post = urllib.urlencode({'id': p[0], 'quality': p[1]})

                    for i in range(5):
                        url = client.request(play, post=post, headers=headers)
                        if not url == None: break

                    url = json.loads(url)['link']

                    url = client.request(url, headers=headers, output='geturl')


                    if 'openload.' in url:
                        links += [{'source': 'openload.co', 'url': url, 'quality': 'HD', 'direct': False}]

                    elif 'videomega.' in url:
                        links += [{'source': 'videomega.tv', 'url': url, 'quality': 'HD', 'direct': False}]

                    else:
                        try: links.append({'source': 'gvideo', 'url': url, 'quality': directstream.googletag(url)[0]['quality'], 'direct': True})
                        except: pass

                except:
                    pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Xmovies', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


