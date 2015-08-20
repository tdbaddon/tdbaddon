# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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
        self.base_link = 'https://sweflix.net'
        self.search_link = '/index.php?act=query&query=%s'
        self.footer_link = '/film_api.php?target=footer&fid=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, "div", attrs = { "class": "hover-group.+?" })

            title = cleantitle.movie(title)
            years = ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="data-movieid")[0], client.parseDOM(i, "h5")[-1], client.parseDOM(i, "p")[-1]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

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

            url = urlparse.urljoin(self.base_link, self.footer_link % url)
            result = client.source(url)

            url = client.parseDOM(result, "a", ret="href")
            url = [i for i in url if 'play/' in i][0]
            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            url = client.parseDOM(result, "source", ret="src", attrs = { "type": "video/.+?" })[0]
            if '1080p' in url: quality = '1080p'
            else: quality = 'HD'

            sources.append({'source': 'Sweflix', 'quality': quality, 'provider': 'Sweflix', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

