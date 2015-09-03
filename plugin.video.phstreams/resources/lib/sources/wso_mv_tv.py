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


import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://watchmovies-online.ch'
        self.tvbase_link = 'http://watchseries-online.ch'
        self.tvsearch_link = 'https://www.google.com/search?q=allintitle:%s&sitesearch=watchseries-online.ch'
        self.moviesearch_link = '/?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.moviesearch_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'div', attrs = {'class': 'Post-body'})

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = tvshowtitle
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            title = url
            hdlr = 'S%02dE%02d' % (int(season), int(episode))

            query = self.tvsearch_link % (urllib.quote_plus('"%s %s"' % (title, hdlr)))

            result = client.source(query)

            tvshowtitle = cleantitle.tv(title)

            result = client.parseDOM(result, 'h3', attrs = {'class': '.+?'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in result]
            result = [(i[0][0], i[1][-1]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]

            result = [(i[0], re.compile('(^Watch Full "|^Watch |)(.+?) %s' % hdlr).findall(i[1])) for i in result]
            result = [(i[0], i[1][0][-1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result][-1]

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

            content = re.compile('/\d{4}/\d{2}/').findall(url)

            if len(content) > 0: url = urlparse.urljoin(self.tvbase_link, url)
            else: url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            links = client.parseDOM(result, 'td', attrs = {'class': 'even tdhost'})
            links += client.parseDOM(result, 'td', attrs = {'class': 'odd tdhost'})

            q = re.compile('<label>Quality</label>(.+?)<').findall(result)
            if len(q) > 0: q = q[0]
            else: q = ''

            if q.endswith(('CAM', 'TS')): quality = 'CAM'
            else: quality = 'SD'

            for i in links:
                try:
                    host = client.parseDOM(i, 'a')[0]
                    host = host.split('<', 1)[0]
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = client.parseDOM(i, 'a', ret='href')[0]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'WSO', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            result = client.request(url)

            try: url = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'wsoButton'})[0]
            except: pass

            url = resolvers.request(url)
            return url
        except:
            return

