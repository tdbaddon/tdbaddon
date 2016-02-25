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
        self.domains = ['watch1080p.com', 'sefilmdk.com']
        self.base_link = 'http://watch1080p.com'
        self.watch_link = '/watch/%s/'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxMjg0NjI0MTAwMTc0NDgzNzMwNzpia210NWhrb3ZsZyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            query = '%s %s' % (title.replace(':', ' '), year)
            query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

            result = client.source(query)
            result = json.loads(result)['results']

            title = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(i['url'], i['titleNoFormatting']) for i in result]
            result = [(i[0], re.compile('(^Watch Full "|^Watch |)(.+? [(]\d{4}[)])').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][-1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.get(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = urlparse.urljoin(self.base_link, result)
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

            result = cloudflare.source(url)
            result = re.sub(r'[^\x00-\x7F]+', '', result)
            result = client.parseDOM(result, 'a', ret='href', attrs = {'class': '[^"]*btn_watch_detail[^"]*'})
            if len(result) == 0:
                url = self.watch_link % [i for i in url.split('/') if not i == ''][-1]
                url = urlparse.urljoin(self.base_link, url)
                result = cloudflare.source(url)
                result = re.sub(r'[^\x00-\x7F]+', '', result)
                result = client.parseDOM(result, 'a', ret='href', attrs = {'class': '[^"]*btn_watch_detail[^"]*'})

            result = urlparse.urljoin(self.base_link, result[0])

            result = cloudflare.source(result)
            result = re.sub(r'[^\x00-\x7F]+', '', result)

            result = client.parseDOM(result, 'div', attrs = {'class': 'server'})[0]
            result = result.split('"svname"')
            result = [(zip(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')), i) for i in result]
            result = [i for i in result if len(i[0]) > 0]
            result = [[(x[0], x[1], i[1]) for x in i[0]] for i in result]
            result = sum(result, [])

            result = [(i[0], re.sub('[^0-9]', '', i[1].strip().split(' ')[-1]), i[2].split(':')[0].split('>')[-1].strip()) for i in result]
            result = [(i[0], '720', i[2]) if i[1] == '' else (i[0], i[1], i[2]) for i in result]

            result = [i for i in result if '1080' in i[1] or '720' in i[1]]
            result = [('%s?quality=1080P' % i[0], '1080p', i[2]) if '1080' in i[1] else ('%s?quality=720P' % i[0], 'HD', i[2]) for i in result]

            links = []
            links += [(i[0], i[1], 'gvideo') for i in result if i[2] in ['Fast Location 1', 'Fast Location 4']]
            links += [(i[0], i[1], 'cdn') for i in result if i[2] in ['Global CDN 4', 'Russian CDN 6', 'Original CDN 2']]

            for i in links: sources.append({'source': i[2], 'quality': i[1], 'provider': 'Watchmovies', 'url': i[0], 'direct': True, 'debridonly': False})

            links = []
            links += [(i[0], i[1], 'openload') for i in result if i[2] in ['Original CDN 1']]

            for i in links: sources.append({'source': i[2], 'quality': i[1], 'provider': 'Watchmovies', 'url': i[0], 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            try: quality = urlparse.parse_qs(urlparse.urlparse(url).query)['quality'][0]
            except: quality = '1080P'
            quality = re.sub('[^0-9]', '', quality)

            url = urlparse.urljoin(self.base_link, url)
            url = url.rsplit('?', 1)[0]

            result = cloudflare.request(url)

            url = client.parseDOM(result, 'div', attrs = {'class': 'player'})[0]
            url = client.parseDOM(url, 'iframe', ret='src')[0]

            result = cloudflare.request(url)

            replace = re.findall("\.replace\('(.*?)'.+?'(.*?)'\)", result)
            for i in replace:
                try: result = result.replace(i[0], i[1])
                except: pass

            count = len(re.findall('window\.atob', result))
            result = re.compile("window\.atob[\([]+'([^']+)").findall(result)[0]
            for i in xrange(count):
                try: result = base64.decodestring(result)
                except: pass

            url = client.parseDOM(result, 'iframe', ret='src')
            if len(url) > 0: return url[0]

            result = re.compile('''<source[^>]+src=["']([^'"]+)[^>]+res=['"]([^'"]+)''').findall(result)
            url = [i for i in result if i[1] == quality]
            if len(url) > 0: url = url[0][0]
            else: url = result[0][0]

            return url
        except:
            return


