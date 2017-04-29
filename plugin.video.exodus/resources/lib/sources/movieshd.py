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

import re,urllib,urlparse,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movieshd.tv', 'movieshd.is', 'movieshd.watch', 'flixanity.is', 'flixanity.me']
        self.base_link = 'https://flixanity.watch'

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

    def movie(self, imdb, title, localtitle, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year, 'localtitle': localtitle}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'localtvshowtitle': localtvshowtitle}
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

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            imdb = data['imdb'] ; year = data['year']

            headers = {}

            if 'tvshowtitle' in data:
                url = '%s/tv-show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(title), int(data['season']), int(data['episode']))
                result = client.request(url, headers=headers, timeout='10')

                if result == None:
                    t = cache.get(self.getOriginalTitle, 900, imdb)
                    if title != t:
                        url = '%s/tv-show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(t), int(data['season']), int(data['episode']))
                        result = client.request(url, headers=headers, timeout='10')
            else:
                url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(title))
                result = client.request(url, headers=headers, timeout='10')

                if result == None:
                    url += '-%s' % year
                    result = client.request(url, headers=headers, timeout='10')

                if result == None:
                    t = cache.get(self.getOriginalTitle, 900, imdb)
                    if title != t:
                        url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(t))
                        result = client.request(url, headers=headers, timeout='10')


            result = client.parseDOM(result, 'title')[0]

            if '%TITLE%' in result: raise Exception()

            r = client.request(url, headers=headers, output='extended', timeout='10')

            if not imdb in r[0]: raise Exception()


            cookie = r[4] ; headers = r[3] ; result = r[0]

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url


            u = '/ajax/jne.php'
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            c = client.request(u, post=post, headers=headers, XHR=True, output='cookie', error=True)

            headers['Cookie'] = cookie + '; ' + c

            r = client.request(u, post=post, headers=headers, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)

            for i in r:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


