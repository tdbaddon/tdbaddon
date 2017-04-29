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

import re, urllib, urlparse, base64, json
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['bobbyhd.com']
        self.base_link = 'http://webapp.bobbyhd.com'
        self.search_link = '/search.php?keyword=%s'
        self.player_link = '/player.php?alias=%s'

    def getOriginalTitle(self, imdb):
        try:
            tmdb_link = base64.b64decode(
                'aHR0cHM6Ly9hcGkudGhlbW92aWVkYi5vcmcvMy9maW5kLyVzP2FwaV9rZXk9MTBiYWIxZWZmNzZkM2NlM2EyMzQ5ZWIxMDQ4OTRhNmEmbGFuZ3VhZ2U9ZW4tVVMmZXh0ZXJuYWxfc291cmNlPWltZGJfaWQ=')
            t = client.request(tmdb_link % imdb, timeout='10')
            try: title = json.loads(t)['movie_results'][0]['original_title']
            except: pass
            try: title = json.loads(t)['tv_results'][0]['original_name']
            except: pass
            title = cleantitle.normalize(title)
            return title
        except:
            return

    def searchMovie(self, title, year, headers):
        try:
            title = cleantitle.normalize(title)
            title = cleantitle.getsearch(title)
            query = self.search_link % ('%s+%s' % (urllib.quote_plus(title), year))
            query = urlparse.urljoin(self.base_link, query)
            for i in range(3):
                r = client.request(query, headers=headers, timeout='10', mobile=True)
                if not r == None: break

            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            r = [(i[0],i[1]) for i in match if cleantitle.get(title) == cleantitle.get(i[1])][0]
            if r:
                return r
        except:
            return

    def movie(self, imdb, title, localtitle, year):
        try:
            headers = {}
            r = self.searchMovie(title, year, headers)
            if r == None:
                t = cache.get(self.getOriginalTitle, 900, imdb)
                if t != title:
                    r = self.searchMovie(t, year, headers)
            url = {'type': 'movie', 'id': r[0], 'episode': 0, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year, 'headers': {}}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = eval(data['headers'])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.getsearch(title)
            cleanmovie = cleantitle.get(title)
            data['season'], data['episode'] = season, episode
            full_check = 'season%01d' % (int(data['season']))
            full_check = cleanmovie + full_check
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            for i in range(3):
                r = client.request(query,headers=headers, timeout='10', mobile=True)
                if not r == None: break

            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            r = [(i[0],i[1]) for i in match if full_check == cleantitle.get(i[1])][0]
            url = {'type': 'tvshow', 'id': r[0], 'episode': episode, 'season': season, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            if data['id'] == None: return sources
            headers = eval(data['headers'])

            url = urlparse.urljoin(self.base_link, self.player_link % data['id'])

            for i in range(3):
                r = client.request(url, headers=headers, timeout='10', mobile=True)
                if not r == None: break

            if data['type'] == 'tvshow':
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(r)
            else:
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(r)

            for url, ep in match:
                try:
                    if data['type'] == 'tvshow':
                        if int(data['episode']) != int(ep):
                            raise Exception()
                    quality = directstream.googletag(url)[0]['quality']
                    sources.append({'source': 'gvideo', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)
