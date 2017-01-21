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


import re,urllib,urlparse,hashlib,string,time,json,base64

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client
from resources.lib.smodules import cache
from resources.lib.smodules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yesmovies.to']
        self.base_link = 'https://yesmovies.to'
        self.info_link = '/ajax/movie_info/%s.html'
        self.episode_link = '/ajax/v3_movie_get_episodes/%s/%s/%s/%s.html'
        self.playlist_link = '/ajax/v2_get_sources/%s.html?hash=%s'
        self.key1 = base64.b64decode('eHdoMzhpZjM5dWN4')
        self.key2 = base64.b64decode('OHFoZm05b3lxMXV4')
        self.key = base64.b64decode('Y3RpdzR6bHJuMDl0YXU3a3F2YzE1M3Vv')


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = '/search/%s.html' % (urllib.quote_plus(cleantitle.query(title)))
            q = urlparse.urljoin(self.base_link, q)

            for i in range(3):
                r = client.request(q)
                if not r == None: break

            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.ymovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass
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

            t = cleantitle.get(data['tvshowtitle'])
            title = data['tvshowtitle']
            season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            year = re.findall('(\d{4})', premiered)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]

            r = cache.get(self.ymovies_info_season, 720, title, season)
            r = [(i[0], re.findall('(.+?)\s+(?:-|)\s+season\s+(\d+)$', i[1].lower())) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and season == '%01d' % int(i[2])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.ymovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                except:
                    pass
        except:
            return


    def ymovies_info_season(self, title, season):
        try:
            q = '%s Season %s' % (cleantitle.query(title), season)
            q = '/search/%s.html' % (urllib.quote_plus(q))
            q = urlparse.urljoin(self.base_link, q)

            for i in range(3):
                r = client.request(q)
                if not r == None: break

            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]

            return r
        except:
            return


    def ymovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)

            for i in range(3):
                r = client.request(u % url)
                if not r == None: break

            q = client.parseDOM(r, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(r, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            url = urlparse.urljoin(self.base_link, url)

            vid_id = re.findall('-(\d+)', url)[-1]

            '''
            quality = cache.get(self.ymovies_info, 9000, vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'
            '''

            for i in range(3):
                r = client.request(url)
                if not r == None: break

            ref = client.parseDOM(r, 'a', ret='href', attrs = {'class': 'mod-btn mod-btn-watch'})[0]
            ref = urlparse.urljoin(self.base_link, ref)

            for i in range(3):
                r = client.request(ref, referer=url)
                if not r == None: break

            h = {'X-Requested-With': 'XMLHttpRequest'}

            server = re.findall('server\s*:\s*"(.+?)"', r)[0]

            type = re.findall('type\s*:\s*"(.+?)"', r)[0]

            episode_id = re.findall('episode_id\s*:\s*"(.+?)"', r)[0]

            r = self.episode_link % (vid_id, server, episode_id, type)
            u = urlparse.urljoin(self.base_link, r)

            for i in range(13):
                r = client.request(u, headers=h, referer=ref)
                if not r == None: break

            r = re.compile('(<li.+?/li>)', re.DOTALL).findall(r)
            r = [(client.parseDOM(i, 'li', ret='onclick'), client.parseDOM(i, 'a', ret='title')) for i in r]

            if not episode == None:
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
                r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0][0] for i in r if i[0]]

            r = [re.findall('(\d+)', i) for i in r]
            r = [i[:2] for i in r if len(i) > 1]
            r = [i[0] for i in r if i[1] in ['12', '13', '14', '15']]

            for u in r:
                try:
                    p = '/ajax/movie_load_embed/%s.html' % u
                    p = urlparse.urljoin(self.base_link, p)

                    for i in range(3):
                        u = client.request(p, headers=h, referer=ref, timeout='10')
                        if not u == None: break

                    url = json.loads(u)['embed_url']

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]

                    sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


