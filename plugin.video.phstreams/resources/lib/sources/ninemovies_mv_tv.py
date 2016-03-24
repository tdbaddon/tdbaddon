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


import re,urllib,urlparse,json,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['fmovies.to']
        self.base_link = 'http://fmovies.to'
        self.hash_link = '/ajax/episode/info'
        self.search_link = '/sitemap'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def fmovies_cache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            result = client.source(url)
            result = re.findall('href="(.+?)">(.+?)<', result)
            result = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            result = [(i[0].split('"')[0], re.findall('(.+?)\((\d{4})\)$', i[1].strip())) for i in result]
            result = [(i[0], i[1][0][0].strip(), i[1][0][1]) for i in result if len(i[1]) > 0]

            return result
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
                title = cleantitle.get(title)

                year = re.findall('(\d{4})', data['premiered'])[0] if 'tvshowtitle' in data else data['year']
                years = ['%s' % str(int(year)+1), '%s' % str(int(year)-1)]

                try: episode = data['episode']
                except: pass

                r = cache.get(self.fmovies_cache, 120)

                url = [i for i in r if i[2] == year]
                if 'tvshowtitle' in data: url += [i for i in r if any(x in i[2] for x in years)]

                if 'season' in data and int(data['season']) > 1:
                    url = [(i[0], re.findall('(.+?) (\d*)$', i[1])) for i in url]
                    url = [(i[0], i[1][0][0], i[1][0][1]) for i in url if len(i[1]) > 0]
                    url = [i for i in url if title == cleantitle.get(i[1])]
                    url = [i for i in url if '%01d' % int(data['season']) == '%01d' % int(i[2])]
                else:
                    url = [i for i in url if title == cleantitle.get(i[1])]

                url = url[0][0]
                url = urlparse.urljoin(self.base_link, url)


            try: url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except: pass

            result = client.source(url)

            try: quality = client.parseDOM(result, 'span', attrs = {'class': 'quality'})[0].lower()
            except: quality = 'hd'
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd' or 'hd ' in quality: quality = 'HD'
            else: quality = 'SD'

            result = client.parseDOM(result, 'ul', attrs = {'class': 'episodes'})
            result = zip(client.parseDOM(result, 'a', ret='data-id'), client.parseDOM(result, 'a'))
            result = [(i[0], re.findall('(\d+)', i[1])) for i in result]
            result = [(i[0], ''.join(i[1][:1])) for i in result]

            try: result = [i for i in result if '%01d' % int(i[1]) == '%01d' % int(episode)]
            except: pass

            links = [urllib.urlencode({'hash_id': i[0], 'referer': url}) for i in result]

            for i in links: sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Ninemovies', 'url': i, 'direct': True, 'debridonly': False})

            try:
                if not quality == 'HD': raise Exception()
                quality = directstream.googletag(self.resolve(links[0]))[0]['quality']
                if not quality == 'SD': raise Exception()
                for i in sources: i['quality'] = 'SD'
            except:
                pass

            return sources
        except:
            return sources


    def __get_token(self, data):
        n = 0
        for key in data:
            if not key.startswith('_'):
                for i, c in enumerate(data[key]):
                    n += ord(c) * (i + 1990)
        return {'_token': hex(n)[2:]}


    def resolve(self, url):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.hash_link)

            query = {'id': data['hash_id'], 'update': '0'}
            query.update(self.__get_token(query))
            url = url + '?' + urllib.urlencode(query)

            result = client.source(url, headers=headers, referer=data['referer'])
            result = json.loads(result)

            query = result['params']
            query['mobile'] = '0'
            query.update(self.__get_token(query))
            grabber = result['grabber'] + '?' + urllib.urlencode(query)

            result = client.source(grabber, headers=headers, referer=url)
            result = json.loads(result)
            result = result['data']

            url = [(re.findall('(\d+)', i['label']), i['file']) for i in result if 'label' in i and 'file' in i]
            url = [(int(i[0][0]), i[1]) for i in url if len(i[0]) > 0]
            url = sorted(url, key=lambda k: k[0])
            url = url[-1][1].replace('%2C', ',')

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


