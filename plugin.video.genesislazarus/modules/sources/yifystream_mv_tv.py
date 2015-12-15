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
import base64
from modules.libraries import cleantitle
from modules.libraries import cloudflare
from modules.libraries import client
from modules import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://yify-streaming.com'
        self.moviesearch_link = '/?cat=2817%2C2812%2C2740&s='
        self.tvsearch_link = '/?cat=2&s='


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.moviesearch_link + urllib.quote_plus(title))

            result = cloudflare.source(query)
            
            result = client.parseDOM(result, "header", attrs = { "class": "entry-header" })

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, "a", ret="href"), client.parseDOM(i, "a")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = urlparse.urlparse(url).path
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            query = '%s "Season %s" "Episode %s"' % (url, season, episode)
            query = urlparse.urljoin(self.base_link, self.tvsearch_link + urllib.quote_plus(query))

            result = cloudflare.source(query)

            result = client.parseDOM(result, "header", attrs = { "class": "entry-header" })

            show = cleantitle.tv(url)

            result = [(client.parseDOM(i, "a", ret="href"), client.parseDOM(i, "a")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(i[0], re.compile('(.+?): Season (\d*).+?Episode (\d*)').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1], i[1][0][2]) for i in result if len(i[1]) > 0]
            result = [i for i in result if season == '%01d' % int(i[2]) and episode == '%01d' % int(i[3])]
            result = [i[0] for i in result if show == cleantitle.tv(i[1])][0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = urlparse.urlparse(url).path
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)
            
            result = client.parseDOM(result, "a", ret="href")

            url = [i for i in result if '.php' in i and 'i=' in i][0]
            url = client.replaceHTMLCodes(url)
            url = urlparse.parse_qs(urlparse.urlparse(url).query)['i'][0]
            url = base64.decodestring(url)

            url = resolvers.request(url)

            if not type(url) == list: raise Exception()

            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'YIFYstream', 'url': i['url']})

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

