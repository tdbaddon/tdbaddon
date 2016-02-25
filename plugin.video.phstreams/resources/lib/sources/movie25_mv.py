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


import re,urllib,urlparse,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.domains = ['movie25.hk']
        self.base_link = 'http://movie25.hk'
        self.search_link = 'http://movie25.hk/search.php?key=%s'


    def request(self, url, check):
        try:
            result = client.source(url)
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.source(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.source(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
        except:
            return


    def movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = self.request(query, 'movie_table')
            result = client.parseDOM(result, 'div', attrs = {'class': 'movie_table'})

            title = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]
            result = [i[0] for i in result if title == cleantitle.get(i[1])][0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
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

            result = self.request(url, 'Links - Quality')
            result = result.replace('\n','')

            quality = re.compile('>Links - Quality(.+?)<').findall(result)[0]
            quality = quality.strip()
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = client.parseDOM(result, 'div', attrs = {'id': 'links'})[0]
            links = links.split('link_name')

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')[0]
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['url'][0]
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


