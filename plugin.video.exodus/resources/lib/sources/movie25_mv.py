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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.domains = ['movie25.ph', 'movie25.hk', 'tinklepad.is', 'tinklepad.ag']
        self.base_link = 'http://tinklepad.ag'
        self.search_link = 'http://tinklepad.ag/search.php?q=%s'
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwODQ5Mjc2ODA5NjE4MzM5MDAwMzowdWd1c2phYm5scSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            q = self.search_link % urllib.quote_plus(cleantitle.query(title))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q, output='extended')

            p = zip(client.parseDOM(r[0], 'input', ret='id'), client.parseDOM(r[0], 'input', ret='value'))
            p = urllib.urlencode(dict(p))

            r = client.request(q, post=p, headers=r[3], cookie=r[4])

            r = client.parseDOM(r, 'div', attrs = {'class': 'movie_table'})

            t = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i for i in r if any(x in i[1] for x in years)]

            try: r = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['q'][0], i[1]) for i in r]
            except: pass
            try: r = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in r]
            except: pass
            try: r = [(urlparse.urlparse(i[0]).path, i[1]) for i in r]
            except: pass

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'link_name')
                    if imdb in str(r): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

        try:
            q = self.search_link_2.decode('base64') % urllib.quote_plus(title)
            r = client.request(q)
            r = json.loads(r)['results']
            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0], re.findall('(?:^Watch |)(.+? \(\d{4}\))', i[1])) for i in r]
            r = [(urlparse.urljoin(self.base_link, i[0]), i[1][0]) for i in r if i[1]]

            t = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            r = [i for i in r if any(x in i[1] for x in years)]

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'link_name')
                    if imdb in str(r): url = i ; break
                except:
                    pass

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

            result = proxy.request(url, 'Links - Quality')
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
                    url = urlparse.urlparse(url).query
                    url = url.decode('base64')
                    url = re.findall('((?:http|https)://.+?/.+?)(?:&|$)', url)[0]
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


