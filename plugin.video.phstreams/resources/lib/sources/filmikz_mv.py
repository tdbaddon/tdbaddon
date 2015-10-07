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


import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://filmikz.ch'
        self.search_link = '/movies.php'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)

            result = client.source(query)

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = re.compile('(<li>.+?</li>)').findall(result)
            result = [i for i in result if "'main2'" in i]
            result = [re.compile('href=(.+?)>(.+?)<').findall(i) for i in result]
            result = [i[0] for i in result if len(i) > 0]
            result = [(i[0], re.compile('(.+?) [(](\d{4})[)]').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1]) for i in result if len(i[1]) > 0]
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

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            links = re.compile("/watch\.php\?q=(.+?)'").findall(result)

            for i in links:
                try:
                    url = base64.urlsafe_b64decode(i.encode('utf-8'))
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = base64.urlsafe_b64decode(i.encode('utf-8'))
                    host = urlparse.urlparse(host).netloc
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Filmikz', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return


