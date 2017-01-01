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


import re,json,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['genvideos.org', 'genvideos.com']
        self.base_link = 'http://genvideos.com'
        self.search_link = '/results?q=%s'


    def movie(self, imdb, title, year):
        try:
            q = self.search_link % (urllib.quote_plus(title))
            q = urlparse.urljoin(self.base_link, q)

            t = cleantitle.get(title)
            a = client.randomagent() ; h = {'User-agent': a}

            r = client.request(q, headers=h, output='cookie')
            r = client.request('http://genvideos.com/av', headers=h, cookie=r, output='cookie')
            r = client.request(q, headers=h, cookie=r, referer=q)

            r = client.parseDOM(r, 'div', attrs = {'class': 'cell_container'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            referer = urlparse.urljoin(self.base_link, url)

            h = {'X-Requested-With': 'XMLHttpRequest'}

            try: post = urlparse.parse_qs(urlparse.urlparse(referer).query).values()[0][0]
            except: post = referer.strip('/').split('/')[-1].split('watch_', 1)[-1].rsplit('#')[0].rsplit('.')[0]

            post = urllib.urlencode({'v': post})

            url = urlparse.urljoin(self.base_link, '/video_info/iframe')

            r = client.request(url, post=post, headers=h, referer=url)
            r = json.loads(r).values()
            r = [urllib.unquote(i.split('url=')[-1])  for i in r]

            for i in r:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Genvideo', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


