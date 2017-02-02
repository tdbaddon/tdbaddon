# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import json
import re
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.domains = ['fmovies.to']
        self.base_link = 'http://fmovies.to'
        self.info_link = '/ajax/episode/info'
        self.search_link = '/search?keyword=%s'

    def movie(self, imdb, title, year):
        try:
            t = cleantitle.movie(title)

            q = urlparse.urljoin(self.base_link, self.search_link)
            q = q % urllib.quote_plus(title)

            r = client.request(q, error=True)
            r = client.parseDOM(r, 'div', attrs = {'class': 'item'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.movie(i[1])]

            for i in r[:4]:
                try:
                    m = client.request(urlparse.urljoin(self.base_link, i))
                    m = re.sub('\s|<.+?>|</.+?>', '', m)
                    m = re.findall('Release:(%s)' % year, m)[0]
                    u = i ; break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', u)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def sources(self, url):
        try:
            srcs = []

            if url == None: return srcs

            url = urlparse.urljoin(self.base_link, url)

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            result = client.request(url, output='extended')

            r = result[0] ; cookie = result[4]

            try: quality = client.parseDOM(r, 'span', attrs = {'class': 'quality'})[0].lower()
            except: quality = 'hd'
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd' or 'hd ' in quality: quality = 'HD'
            else: quality = 'SD'

            category = client.parseDOM(r, 'div', ret='data-id', attrs = {'id': '.+?'})[0]

            servers = client.parseDOM(r, 'ul', attrs = {'data-range-id': '0'})
            servers = zip(client.parseDOM(servers, 'a', ret='data-id'), client.parseDOM(servers, 'a'))
            servers = [(i[0], re.findall('(\d+)', i[1])) for i in servers]
            servers = [(i[0], ''.join(i[1][:1])) for i in servers]

            if not episode == None:
                servers = [i for i in servers if '%01d' % int(i[1]) == '%01d' % int(episode)]

            for s in servers[:5]:
                try:
                    headers = {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': '%s/%s' % (url, s),
                        'Cookie': cookie
                    }

                    post = {'id': s[0], 'update': '0', 'film': category}
                    post.update(self._token(post))

                    u = urlparse.urljoin(self.base_link, self.info_link)
                    u += '?' + urllib.urlencode(post)

                    r = client.request(u, headers=headers)

                    r = json.loads(r)

                    t = r['target']

                    if 'openload' in t:
                        srcs.append({'source': 'openload.co', 'quality': quality, 'provider': 'Ninemovies', 'url': t, 'direct': False, 'debridonly': False})

                    post = r['params']
                    if not post: raise Exception()
                    post['mobile'] = '0'
                    post.update(self._token(post))

                    headers['Referer'] = u

                    g = r['grabber'] + '?' + urllib.urlencode(post)

                    r = client.request(g, headers=headers)

                    r = json.loads(r)['data']
                    r = [i['file'] for i in r if 'file' in i]

                    for i in r:
                        try: srcs.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Ninemovies', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        return url


    def _token(self, data):
        n = 0
        for key in data:
            if not key.startswith('_'):
                for i, c in enumerate(data[key]):
                    n += ord(c) * 64184 + len(data[key])
        return {'_token': hex(n)[2:]}