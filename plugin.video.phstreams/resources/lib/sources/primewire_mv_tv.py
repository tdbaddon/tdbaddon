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
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.domains = ['primewire.ag']
        self.base_link = 'http://www.primewire.ag'
        self.key_link = 'http://www.primewire.ag/index.php?search'
        self.moviesearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=2'


    def request(self, url, check):
        try:
            result = client.source(url)
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.source(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

            result = client.source(proxy.get() + urllib.quote_plus(url))
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
        except:
            return


    def movie(self, imdb, title, year):
        try:
            result = self.request(self.key_link, 'searchform')

            query = client.parseDOM(result, 'input', ret='value', attrs = {'name': 'key'})[0]
            query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), query)

            result = self.request(query, 'index_item')
            result = client.parseDOM(result, 'div', attrs = {'class': 'index_item.+?'})

            title = 'watch' + cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['q'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            except: pass

            match = [i[0] for i in result if title == cleantitle.get(i[1])]

            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    result = self.request(urlparse.urljoin(self.base_link, i), 'choose_tabs')
                    if imdb in str(result): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            result = self.request(self.key_link, 'searchform')

            query = client.parseDOM(result, 'input', ret='value', attrs = {'name': 'key'})[0]
            query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', tvshowtitle)), query)

            result = self.request(query, 'index_item')
            result = client.parseDOM(result, 'div', attrs = {'class': 'index_item.+?'})

            tvshowtitle = 'watch' + cleantitle.get(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['q'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            try: result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            except: pass

            match = [i[0] for i in result if tvshowtitle == cleantitle.get(i[1])]

            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    result = self.request(urlparse.urljoin(self.base_link, i), 'tv_episode_item')
                    if imdb in str(result): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = self.request(url, 'tv_episode_item')
            result = client.parseDOM(result, 'div', attrs = {'class': 'tv_episode_item'})

            title = cleantitle.get(title)

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tv_episode_name'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in result]
            result = [(i[0], i[1][0], i[2]) for i in result if len(i[1]) > 0] + [(i[0], None, i[2]) for i in result if len(i[1]) == 0]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0] + [(i[0], i[1], None) for i in result if len(i[2]) == 0]
            result = [(i[0][0], i[1], i[2]) for i in result if len(i[0]) > 0]

            url = [i for i in result if title == cleantitle.get(i[1]) and premiered == i[2]][:1]
            if len(url) == 0: url = [i for i in result if premiered == i[2]]
            if len(url) == 0 or len(url) > 1: url = [i for i in result if 'season-%01d-episode-%01d' % (int(season), int(episode)) in i[0]]

            url = client.replaceHTMLCodes(url[0][0])
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass
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

            result = self.request(url, 'choose_tabs')

            links = client.parseDOM(result, 'tbody')

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')[0]
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['url'][0]
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = client.parseDOM(i, 'span', ret='class')[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()

                    sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


