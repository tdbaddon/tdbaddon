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
        '''self.domains = ['123movies.to']
        self.base_link = 'http://123movies.to'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxP2tleT1BSXphU3lCS3NHYUZ6alIxUXl5bE1QYzZ6Vm9QNzFVczU3aTltRWsmbnVtPTEwJmhsPWVuJmN4PTAxNTc3MDA5MzA5OTIyNTYzNDAxMzpvOHRwZHlram93dSYmZ29vZ2xlaG9zdD13d3cuZ29vZ2xlLmNvbSZxPSVz'
        self.search2_link = '/movie/search/%s'
        '''
        self.domains = ['123movies.to', '123movies.ru']
        self.base_link = 'http://123movies.ru'
        self.info_link = '/ajax/movie_load_info/%s'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTp1a2lqdGJvbm1jNCZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.search2_link = '/movie/search/%s'


    def get_movie(self, imdb, title, year):
        try:
            t = cleantitle.movie(title)

            try:
                query = '%s %s' % (title, year)
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.source(query)
                result = json.loads(result)['results']

                r = [(i['url'], i['titleNoFormatting']) for i in result]
                r = [(i[0], re.findall('(?:^Watch Full "|^Watch |)(.+?)(?:For Free On 123Movies|On 123Movies|$)', i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i[0] for i in r if t == cleantitle.get(i[1])]

                for i in r:
                    url = self._info(i, year)
                    if not url == None: return url
            except:
                pass

            try:
                query = self.search2_link % urllib.quote_plus(title)
                query = urlparse.urljoin(self.base_link, query)

                result = cloudflare.source(query)

                r = client.parseDOM(result, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i[0] for i in r if t == cleantitle.get(i[1])]

                for i in r:
                    url = self._info(i, year)
                    if not url == None: return url
            except:
                pass

        except:
            return

    def get_sources(self, url):
        logger.debug('%s SOURCES URL %s' % (self.__class__, url))
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            url = url.replace('/watching.html', '')

            content = re.compile('(.+?)\?episode=\d*$').findall(url)
            content = 'movie' if len(content) == 0 else 'episode'

            try: url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except: pass

            url = urlparse.urljoin(self.base_link, url) + '/watching.html'

            result = cloudflare.source(url)
            movie = client.parseDOM(result, 'div', ret='movie-id', attrs = {'id': 'media-player'})[0]

            try: quality = client.parseDOM(result, 'span', attrs = {'class': 'quality'})[0].lower()
            except: quality = 'hd'
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'

            url = '/movie/loadepisodes/%s' % movie
            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url)

            r = client.parseDOM(result, 'div', attrs = {'class': 'les-content'})
            r = zip(client.parseDOM(r, 'a', ret='onclick'), client.parseDOM(r, 'a', ret='episode-id'), client.parseDOM(r, 'a'))
            r = [(re.sub('[^0-9]', '', i[0].split(',')[0]), re.sub('[^0-9]', '', i[0].split(',')[-1]), i[1], ''.join(re.findall('(\d+)', i[2])[:1])) for i in r]
            r = [(i[0], i[1], i[2], i[3]) for i in r]

            if content == 'episode':
                r = [i for i in r if i[3] == '%01d' % int(episode)]
            else:
                b = client.parseDOM(result, 'div', ret='data-episodes', attrs = {'id': 'server-backup'})
                b = [re.findall('(.+?)-(.+)', i) for i in b]
                r += [('99', i[0][1], i[0][0], '720') for i in b if len(i) > 0]


            direct_link = '/ajax/load_episode/%s/%s'

            embed_link = '/ajax/load_embed/%s/%s'

            links = []
            links += [{'source': 'gvideo', 'url': direct_link % (i[2], i[1]), 'direct': True} for i in r if 2 <= int(i[0]) <= 11]
            links += [{'source': 'cdn', 'url': direct_link % (i[2], i[1]), 'direct': True} for i in r if i[0] == '99']
            links += [{'source': 'openload.co', 'url': embed_link % (i[2], i[1]), 'direct': False} for i in r if i[0] == '14']
            links += [{'source': 'videomega.tv', 'url': embed_link % (i[2], i[1]), 'direct': False} for i in r if i[0] == '13']
            links += [{'source': 'videowood.tv', 'url': embed_link % (i[2], i[1]), 'direct': False} for i in r if i[0] == '12']

            for i in links: sources.append({'source': i['source'], 'quality': quality, 'provider': 'Onemovies', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            logger.debug('%s SOURCES [%s]' % (__name__,sources))
            return sources
        except:
            return sources

    def resolve(self, url):
        logger.debug('%s ORIGINAL URL [%s]' % (__name__, url))
        try:
            url = urlparse.urljoin(self.base_link, url)
            result = cloudflare.source(url)
        except:
            pass

        try:
            url = re.compile('"?file"?\s*=\s*"(.+?)"\s+"?label"?\s*=\s*"(\d+)p?"').findall(result)
            url = [(int(i[1]), i[0]) for i in url]
            url = sorted(url, key=lambda k: k[0])
            url = url[-1][1]

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return url
        except:
            pass

        try:
            url = json.loads(result)['embed_url']
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return url
        except:
            pass