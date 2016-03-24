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

from resources.lib.modules import cleantitle
from resources.lib.modules import cloudflare
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['xmovies8.tv']
        self.base_link = 'http://xmovies8.tv'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNjQ4MjIzNjE2MjI4MzE1ODkwMDpjZzNhZmZ2bWNvayZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTowbGdidnQwcndsOCZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM=='


    def movie(self, imdb, title, year):
        try:
            query = '%s %s' % (title.replace(':', ' '), year)
            query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

            result = client.source(query)
            result = json.loads(result)['results']

            t = cleantitle.get(title)
            years = ['(%s)' % str(year)]

            result = [(i['url'], i['titleNoFormatting']) for i in result]
            result = [(i[0], re.compile('(^Watch Full "|^Watch |^Xmovies8:|^xmovies8:|)(.+? [(]\d{4}[)])').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][-1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if t == cleantitle.get(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = '/'.join(url.split('/')[:3]) + '/'
            return url
        except:
            pass

        try:
            t = title.replace('\'', '')
            t = re.sub(r'[^a-zA-Z0-9\s]+', ' ', t).lower().strip()
            t = re.sub('\s\s+' , ' ', t)
            t = '/movie/' + t.replace(' ' , '-') + '-'

            years = ['-%s' % str(year)]

            query = base64.b64decode(self.search_link_2) % t

            result = client.source(query)
            result = json.loads(result)['results']
            result = [i['contentNoFormatting'] for i in result]
            result = ''.join(result)
            result = re.compile('(/movie/.+?)\s').findall(result)
            result = [i for i in result if t in i]
            result = [i for i in result if any(x in i for x in years)][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = '/'.join(url.split('/')[:3]) + '/'
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)

            url = client.parseDOM(result, 'embed', ret='src')[0]
            url = client.replaceHTMLCodes(url)

            url = 'https://docs.google.com/file/d/%s/preview' % urlparse.parse_qs(urlparse.urlparse(url).query)['docid'][0]

            url = directstream.google(url)

            for i in url: sources.append({'source': 'gvideo', 'quality': i['quality'], 'provider': 'Xmovies', 'url': i['url'], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


