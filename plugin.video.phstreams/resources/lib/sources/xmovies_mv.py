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
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

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

            years = ['-%s' % str(year), '-%s' % str(int(year)+1), '-%s' % str(int(year)-1)]

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

            referer = urlparse.urljoin(self.base_link, url)

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': referer}

            post = urlparse.urlparse(url).path
            post = re.compile('/.+?/(.+)').findall(post)[0].rsplit('/')[0]
            post = 'mx=%s&isseries=0&part=0' % post

            url = urlparse.urljoin(self.base_link, '/lib/picasa.php')

            result = cloudflare.source(url, post=post, headers=headers)

            result = client.parseDOM(result, 'div', attrs = {'class': '[^"]*download[^"]*'})[0]
            result = re.compile('href="([^"]+)[^>]+>(\d+)p?<').findall(result)
            result = [('%s|referer=%s' % (i[0], referer), i[1])  for i in result]

            links = [(i[0], '1080p') for i in result if int(i[1]) >= 1080]
            links += [(i[0], 'HD') for i in result if 720 <= int(i[1]) < 1080]
            links += [(i[0], 'SD') for i in result if 480 <= int(i[1]) < 720]
            if not 'SD' in [i[1] for i in links]: links += [(i[0], 'SD') for i in result if 360 <= int(i[1]) < 480]

            for i in links: sources.append({'source': 'gvideo', 'quality': i[1], 'provider': 'Xmovies', 'url': i[0], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url, referer = re.compile('(.+?)\|referer=(.+)').findall(url)[0]

            url = client.request(url, referer=referer, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


