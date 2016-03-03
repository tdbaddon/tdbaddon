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
        self.domains = ['123movies.to']
        self.base_link = 'http://123movies.to'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTp1a2lqdGJvbm1jNCZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.search2_link = '/movie/search/%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            try:
                query = '%s %s' % (title, year)
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.source(query)
                result = json.loads(result)['results']

                r = [(i['url'], i['titleNoFormatting']) for i in result]
                r = [(i[0], re.compile('(^Watch Full "|^Watch |)(.+)').findall(i[1])) for i in r]
                r = [(i[0], i[1][0][-1]) for i in r if len(i[1]) > 0]
                r = [(i[0], i[1].rsplit(' For Free On 123Movies', 1)[0].rsplit('On 123Movies', 1)[0]) for i in r]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if t == cleantitle.get(i[1])]
                u = [i[0] for i in r][0]

            except:
                query = self.search2_link % urllib.quote_plus(title)
                query = urlparse.urljoin(self.base_link, query)

                result = client.source(query)

                r = client.parseDOM(result, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if t == cleantitle.get(i[1])]
                u = [i[0] for i in r][0]


            url = urlparse.urljoin(self.base_link, u)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            tvshowtitle = cleantitle.get(data['tvshowtitle'] )
            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            try:
                query = '%s season %01d' % (data['tvshowtitle'], int(season))
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.source(query)
                result = json.loads(result)['results']

                r = [(i['url'], i['titleNoFormatting']) for i in result]
                r = [(i[0], re.compile('(^Watch Full "|^Watch |)(.+)').findall(i[1])) for i in r]
                r = [(i[0], i[1][0][-1]) for i in r if len(i[1]) > 0]
                r = [(i[0], re.compile('(.+?) - Season (\d*)').findall(i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1], i[2]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1], i[2]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if tvshowtitle == cleantitle.get(i[1])]
                u = [i[0] for i in r if season == '%01d' % int(i[2])][0]

            except:
                query = self.search2_link % urllib.quote_plus(data['tvshowtitle'])
                query = urlparse.urljoin(self.base_link, query)

                result = client.source(query)

                r = client.parseDOM(result, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(i[0], re.compile('(.+?) - Season (\d*)').findall(i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [(re.sub('http.+?//.+?/','', i[0]), i[1], i[2]) for i in r]
                r = [('/'.join(i[0].split('/')[:2]), i[1], i[2]) for i in r]
                r = [x for y,x in enumerate(r) if x not in r[:y]]
                r = [i for i in r if tvshowtitle == cleantitle.get(i[1])]
                u = [i[0] for i in r if season == '%01d' % int(i[2])][0]


            url = urlparse.urljoin(self.base_link, u)
            url = urlparse.urlparse(url).path
            url += '?episode=%01d' % int(episode)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
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

            result = client.parseDOM(result, 'div', attrs = {'class': 'les-content'})
            result = zip(client.parseDOM(result, 'a', ret='onclick'), client.parseDOM(result, 'a', ret='episode-id'), client.parseDOM(result, 'a'))
            result = [(re.sub('[^0-9]', '', i[0].split(',')[0]), re.sub('[^0-9]', '', i[0].split(',')[-1]), i[1], ''.join(re.findall('(\d+)', i[2])[:1])) for i in result]
            result = [(i[0], i[1], i[2], i[3]) for i in result]

            if content == 'episode': result = [i for i in result if i[3] == '%01d' % int(episode)]

            links = [('movie/load_episode/%s/%s' % (i[2], i[1]), 'gvideo') for i in result if 2 <= int(i[0]) <= 11]

            for i in links: sources.append({'source': i[1], 'quality': quality, 'provider': 'Onemovies', 'url': i[0], 'direct': True, 'debridonly': False})

            links = []
            links += [('movie/loadEmbed/%s/%s' % (i[2], i[1]), 'openload.co') for i in result if i[0] == '14']
            #links += [('movie/loadEmbed/%s/%s' % (i[2], i[1]), 'videomega.tv') for i in result if i[0] == '13']
            #links += [('movie/loadEmbed/%s/%s' % (i[2], i[1]), 'videowood.tv') for i in result if i[0] == '12']

            for i in links: sources.append({'source': i[1], 'quality': quality, 'provider': 'Onemovies', 'url': i[0], 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
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
            return url
        except:
            pass

        try:
            url = json.loads(result)['embed_url']
            return url
        except:
            pass


