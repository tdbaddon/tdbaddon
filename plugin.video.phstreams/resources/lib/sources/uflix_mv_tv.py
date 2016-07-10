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


class source:
    def __init__(self):
        self.domains = ['uflix.ws']
        self.base_link = 'http://uflix.ws'
        self.search_link = '/index.php?menu=search&query=%s'


    def movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query).decode('iso-8859-1').encode('utf-8')

            r = client.parseDOM(r, 'div', attrs = {'id': 'movies'})[0]

            r = client.parseDOM(r, 'figcaption')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], re.findall('(?:^Watch |)(.+?)(?: Online|)$', i[1]), re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1][0], i[2][0]) for i in r if len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1].replace(i[2], ''), i[2]) for i in r]

            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(tvshowtitle)

            r = client.request(query).decode('iso-8859-1').encode('utf-8')

            r = client.parseDOM(r, 'div', attrs = {'id': 'series'})[0]

            r = client.parseDOM(r, 'figcaption')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], re.findall('(?:^Watch |)(.+?)(?: Online|)$', i[1]), re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1][0], i[2][0]) for i in r if len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1].replace(i[2], ''), i[2]) for i in r]

            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url).decode('iso-8859-1').encode('utf-8')

            r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'link'}), client.parseDOM(r, 'a', attrs = {'class': 'link'}))
            r = [i for i in r if '/season/%01d/episode/%01d' % (int(season), int(episode)) in i[0]][0]

            t = client.parseDOM(r[1], 'span')[0]

            if not cleantitle.get(title) == cleantitle.get(t): raise Exception()

            url = re.findall('(?://.+?|)(/.+)', r[0])[0]
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

            r = client.request(url).decode('iso-8859-1').encode('utf-8')

            if not ('/episode/' in url or 'fullhdbr.png' in r or 'Blu-Ray.gif' in r): raise Exception()

            links = re.findall('url=(.+?)&', r)
            links = [x for y,x in enumerate(links) if x not in links[:y]]

            for i in links:
                try:
                    url = base64.b64decode(i)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'uFlix', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


