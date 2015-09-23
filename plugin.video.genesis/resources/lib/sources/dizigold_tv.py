# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://www.dizigold.net'
        self.headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.ajax_link = '/sistem/ajax.php'
        self.search_link = 'aranan=%s&tip=aranans'
        self.episode_link = 'sezon_id=%s&dizi_id=%s&tip=sezon'
        self.player_link = 'id=%s&tip=view'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = urlparse.urljoin(self.base_link, self.ajax_link)
            post = self.search_link % (urllib.quote_plus(tvshowtitle))

            result = client.source(query, post=post, headers=self.headers)
            result = json.loads(result)

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h3'), re.compile('<h5>.+?(\d{4}).+?</h5>').findall(i)) for i in result]
            result = [(i[0][0], i[1][0], i[2][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            url = urlparse.urljoin(self.base_link, result)

            result = client.source(url)

            url = client.parseDOM(result, 'div', ret='value', attrs = {'id': 'icerikid'})[0]
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            query = urlparse.urljoin(self.base_link, self.ajax_link)
            post = self.episode_link % ('%01d' % int(season), url)

            result = client.source(query, post=post, headers=self.headers)
            result = json.loads(result)
            result = result['data']
            result = re.compile('href="(.+?)"').findall(result)
            result = [i for i in result if '/%01d-sezon/%01d-bolum' % (int(season), int(episode)) in i][-1]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            query = urlparse.urljoin(self.base_link, self.ajax_link)
            post = re.compile('var\s*view_id\s*=\s*"(\d*)"').findall(result)[0]
            post = self.player_link % post

            result = client.source(query, post=post, headers=self.headers)
            result = json.loads(result)
            result = result['data']

            result = re.compile('"file"\s*:\s*"(.+?)".+?"label"\s*:\s*"(\d*p)"').findall(result)

            links = [{'url': i[0], 'quality': i[1]} for i in result if 'google' in i[0]]
            links += [{'url': '%s|User-Agent=%s&Referer=%s' % (i[0], urllib.quote_plus(client.agent()), urllib.quote_plus(url)), 'quality': i[1]} for i in result if not 'google' in i[0]]


            try: sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '1080p'][0]})
            except: pass
            try: sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '720p'][0]})
            except: pass
            try: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '480p'][0]})
            except: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizigold', 'url': [i['url'] for i in links if i['quality'] == '360p'][0]})


            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if not 'google' in url: return url
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

