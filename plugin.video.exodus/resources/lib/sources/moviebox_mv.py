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


import re,urlparse

from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['movie-box.co']
        self.base_link = 'https://movie-box.co'
        self.movie_link = '/stream-hd/%s-%s.html'


    def movie(self, imdb, title, year):
        try:
            url = re.sub('([^\s\-\w])+', '', title.lower()).replace(' ', '-')
            url = self.movie_link % (url, year)
            url = urlparse.urljoin(self.base_link, url)

            url = client.request(url, output='geturl')

            if url == None: raise Exception()

            url = urlparse.urljoin(self.base_link, url)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            url = client.request(url)

            url = re.findall('(openload\.(?:io|co)/(?:embed|f)/[0-9a-zA-Z-_]+)', url)[0]
            url = 'http://' + url

            sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': 'MovieBox', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


