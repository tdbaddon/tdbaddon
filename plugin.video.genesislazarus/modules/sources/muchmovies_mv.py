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


import re
import urllib
import urlparse
from modules.libraries import cleantitle
from modules.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://umovies.me'
        self.search_link = '/search/%s'


    def get_movie(self, imdb, title, year):
        try:
            query = urllib.quote_plus(title.replace(' ', '-').rsplit(':', 1)[0])
            query = urlparse.urljoin(self.base_link, self.search_link % query)

            result = client.source(query, mobile=True)
            result = client.parseDOM(result, "ul", attrs = { "class": "movies.+?" })
            result = client.parseDOM(result, "li")

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "h3")[0]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

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
            sources.append({'source': 'Muchmovies', 'quality': 'HD', 'provider': 'Muchmovies', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            result = client.request(url, mobile=True)
            url = client.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            return url
        except:
            return

