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
from resources.lib.resolvers import googleplus


class source:
    def __init__(self):
        self.base_link = 'http://www.hdmoviezone.net'
        self.cookie_link = 'http://gl.hdmoviezone.net/getimage.php'
        self.stream_link = 'http://gl.hdmoviezone.net/hdmzgl.php'
        self.search_link = '/feed/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(title)))

            result = client.source(query)
            result = client.parseDOM(result, 'item')
            result = [(client.parseDOM(i, 'link')[0], client.parseDOM(i, 'span', ret='data-title', attrs = {'class': 'imdbRating'})[0]) for i in result]
            result = [i[0] for i in result if imdb in i[1]][0]

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

            url = urlparse.urljoin(self.base_link , url)
            result = client.source(url)

            url = client.parseDOM(result, 'div', attrs = {'class': 'fullwindowlink'})[0]
            url = client.parseDOM(url, 'a', ret='href')[0]
            url = urlparse.urljoin(self.base_link , url)

            result = client.source(url)
            result = client.parseDOM(result, 'body')[0]

            post = re.compile('movie_player_file *= *"(.+?)"').findall(result)[0]
            post = urllib.urlencode({'url': post})

            cookie = client.source(self.cookie_link, output='cookie', close=False)

            headers = {'Host': 'gl.hdmoviezone.net',
            'Accept': 'text/html, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.hdmoviezone.net',
            'Cookie': cookie}

            result = client.source(self.stream_link, post=post, headers=headers)

            result = json.loads(result)
            result = result['content']

            links = [i['url'] for i in result]

            for url in links:
                try:
                    i = googleplus.tag(url)[0]
                    sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Moviezone', 'url': i['url']})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


