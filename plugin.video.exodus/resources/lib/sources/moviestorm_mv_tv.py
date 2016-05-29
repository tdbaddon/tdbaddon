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
from resources.lib.modules import client
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.domains = ['moviestorm.eu']
        self.base_link = 'http://moviestorm.eu'
        self.moviesearch_link = '/search'
        self.tvsearch_link = '/series/all/'


    def movie(self, imdb, title, year):
        try:
            query = self.base_link + self.moviesearch_link
            post = urllib.urlencode({'go': 'Search', 'q': title})

            result = client.request(query, post=post)
            result = client.parseDOM(result, 'div', attrs = {'class': 'movie_box'})

            result = [i for i in result if imdb in i][0]
            result = client.parseDOM(result, 'a', ret='href')[0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            result = cache.get(self.moviestorm_tvcache, 120)

            tvshowtitle = cleantitle.get(tvshowtitle)

            result = [i[0] for i in result if tvshowtitle == i[1]][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def moviestorm_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.tvsearch_link)

            result = client.request(url)
            result = re.compile('(<li>.+?</li>)').findall(result)
            result = [re.compile('href="(.+?)">(.+?)<').findall(i) for i in result]
            result = [i[0] for i in result if len(i) > 0]
            result = [i for i in result if self.base_link in i[0] and '/view/' in i[0]]
            result = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            result = [(i[0], cleantitle.get(i[1])) for i in result]

            return result
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if url == None: return

        url = '%s/season-%01d/episode-%01d/' % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url)

            links = client.parseDOM(result, 'div', attrs = {'class': 'links'})[0]
            links = client.parseDOM(links, 'tr')

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')[-1]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in ['ishared.eu', 'shared2.me']: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = client.parseDOM(i, 'td', attrs = {'class': 'quality_td'})
                    quality = quality[0].lower().strip() if len(quality) > 0 else ''
                    if quality in ['cam', 'ts']: raise Exception()

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Moviestorm', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


