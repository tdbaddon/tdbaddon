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


import re,urllib,urlparse,json,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.domains = ['fimlywap.im.to']
        self.base_link = 'http://fimlywap.im'
        #self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5QktzR2FGempSMVF5eWxNUGM2elZvUDcxVXM1N2k5bUVrJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxMzA1Mjg2NDc5NDEyNDIwMTQ1MTpkZXl3cW1mNDVhYSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        #exodus
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNjE2OTI4MDMzMzcxNDY1MDkyNzotMGVwYXI3djBqeSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

    def get_movie(self, imdb, title, year):
        try:
            t = cleantitle.movie(title)

            try:
                query = '%s %s' % (title, year)
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.source(query)
                result = json.loads(result)['results']
                r = [(i['url'], i['titleNoFormatting']) for i in result]
                r = [(i[0], re.compile('(.+?) [\d{4}|(\d{4})]').findall(i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if t == cleantitle.movie(i[1])]
                u = [i[0] for i in r][0]

            except:
                return

            url = u
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('%s SOURCES URL %s' % (self.__class__, url))
        try:
            sources = []

            if url == None: return sources

            result = client.source(url)
            result = client.parseDOM(result, 'table', attrs = {'class': 'rows differ_download'})[0]
            links = client.parseDOM(result, 'tr')

            for link in links:
                try: quality = client.parseDOM(link, 'span', attrs = {'class': 'quality_1'})[0].lower()
                except: quality = 'hd'
                if quality == 'ts': quality = 'CAM'
                elif '360p' in quality : quality = 'SD'
                elif '720p' in quality : quality = 'HD'
                else: quality = 'SD'

                url = client.parseDOM(link, 'a', ret="href")[0]
                host = client.host(url)

                sources.append({'source': host, 'parts' : '1', 'quality': quality, 'provider': 'filmywap', 'url': url, 'direct': False, 'debridonly': False})

            logger.debug('%s SOURCES [%s]' % (__name__,sources))
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        return url