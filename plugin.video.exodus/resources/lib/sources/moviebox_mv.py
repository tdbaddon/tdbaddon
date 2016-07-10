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

import urllib
import json


import re,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['movie-box.co']
        self.base_link = 'http://movie-box.co'
        self.search_link = '/wp-json/wp/v2/posts?search=%s'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = self.search_link % urllib.quote_plus(data['title'])
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(data['title'])

            r = client.request(query)
            r = json.loads(r)

            r = [(i['content']['rendered'], i['title']['rendered']) for i in r]
            r = [(i[0], cleantitle.get(i[1]), re.findall('(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if len(i[2]) > 0]
            r = [i[0] for i in r if t == i[1] and data['year'] == i[2]][0]

            url = 'http://' + re.findall('(openload\.(?:io|co)/(?:embed|f)/[0-9a-zA-Z-_]+)', r)[0]

            sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': 'MovieBox', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


