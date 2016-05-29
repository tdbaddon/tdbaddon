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
from resources.lib.modules import client
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.domains = ['show-box.co']
        self.base_link = 'https://show-box.co'
        self.search_link = '/categories'



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


    def showbox_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            r = client.request(url)

            r = client.parseDOM(r, 'ul', attrs = {'class': 'listing.+?'})[0]
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('\d{4}$','', i[1])) for i in r]
            r = [(i[0], cleantitle.get(i[1])) for i in r]

            return r
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            t = cleantitle.get(data['tvshowtitle'])

            r = cache.get(self.showbox_tvcache, 120)

            r = [i[0] for i in r if t == cleantitle.get(i[1])]

            for url in r:
                try:
                    url = re.sub('/$', '', url)
                    url = url.replace('/category/', '/')
                    url = '%s-s%02de%02d.html' % (url, int(data['season']), int(data['episode']))
                    url = urlparse.urljoin(self.base_link, url)

                    url = client.request(url)
                    if not url == None: break
                except:
                    pass

            url = re.findall('(openload\.(?:io|co)/(?:embed|f)/[0-9a-zA-Z-_]+)', url)[0]
            url = 'http://' + url

            sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': 'ShowBox', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


