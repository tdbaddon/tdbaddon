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
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://movietv.to'
        self.headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.search_link = '/search?q=%s'
        self.episode_link = '/series/getLink?id=%s&s=%s&e=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query, safe=True)

            result = client.parseDOM(result, 'div', {'class': 'movie-grid grid-.+?'})

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', {'class': 'movie-grid-title'})) for i in result]
            result = [(i[0][0], i[1][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(i[0], i[1].split('<')[0].strip(), client.parseDOM(i[2], 'span', {'class': '[^"]*year'})) for i in result]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0]
            result = [i for i in result if '/movies/' in i[0]]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % urllib.quote_plus(tvshowtitle)
            query = urlparse.urljoin(self.base_link, query)

            result = cloudflare.source(query, safe=True)
            result = client.parseDOM(result, 'div', {'class': 'movie-grid grid-.+?'})

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', {'class': 'movie-grid-title'})) for i in result]
            result = [(i[0][0], i[1][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(i[0], i[1].split('<')[0].strip(), client.parseDOM(i[2], 'span', {'class': '[^"]*year'})) for i in result]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0]
            result = [i for i in result if '/series/' in i[0]]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            if not '%01d' % int(season) == '1': return
            if '%01d' % int(episode) > '3': return

            url += '?S%02dE%02d' % (int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            content = re.compile('(.+?)\?S\d*E\d*$').findall(url)

            try: url, season, episode = re.compile('(.+?)\?S(\d*)E(\d*)$').findall(url)[0]
            except: pass

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url, safe=True)

            if len(content) == 0:
                u = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
            else:
                u = re.compile('playSeries\((\d+),(%01d),(%01d)\)' % (int(season), int(episode))).findall(result)[0]
                u = self.episode_link % (u[0], u[1], u[2])
                u = urlparse.urljoin(self.base_link, u)
                u = cloudflare.source(u, safe=True, headers=self.headers)
                u = json.loads(u)['url']

            url = '%s|User-Agent=%s&Referer=%s' % (u, urllib.quote_plus(client.agent()), urllib.quote_plus(url))

            sources.append({'source': 'MovieTV', 'quality': 'HD', 'provider': 'MovieTV', 'url': url})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


