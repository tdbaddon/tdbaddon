# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2016 mrknow

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

# TODO: Check gvideo resolving

import re,urllib,urlparse, json, hashlib
import base64
import random, string
import hashlib
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib import resolvers
from resources.lib.libraries import control
import requests




class source:
    def __init__(self):
        self.base_link = 'https://123movies.ru'
        self.base_link_2 = 'https://123movies.net.ru'
        self.search_link = '/ajax/suggest_search'
        self.search_link_2 = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'

        #http://123movies.to/ajax/suggest_search


    def request(self, url, post=None, headers=None, XHR=False):
        try:
            r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            if r[0] == None: return r

            if 'internetmatters.org' in r[0]:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = urlparse.urljoin(self.base_link_2, url)
                r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            return r
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = self.search_link_2 % (urllib.quote_plus(cleantitle.query(title)))
            q = urlparse.urljoin(self.base_link, q)

            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': title})

            r = self.request(u, post=p, XHR=True)[0]

            try: r = json.loads(r)['content']
            except: r = None

            if r == None:
                r = self.request(q)[0]
                r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            else:
                r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            r = [i[0] for i in r if cleantitle.get(t) == cleantitle.get(i[1])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.onemovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            t = cleantitle.get(data['tvshowtitle'])
            year = re.findall('(\d{4})', date)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            q = self.search_link_2 % (urllib.quote_plus('%s - Season %s' % (data['tvshowtitle'], season)))
            q = urlparse.urljoin(self.base_link, q)

            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': '%s - Season %s' % (data['tvshowtitle'], season)})

            r = self.request(u, post=p, XHR=True)[0]

            try: r = json.loads(r)['content']
            except: r = None

            if r == None:
                r = self.request(q)[0]
                r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            else:
                r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            r = [(i[0], re.findall('(.+?) - season (\d+)$', i[1].lower())) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i for i in r if t == cleantitle.get(i[1])]
            r = [i[0] for i in r if season == '%01d' % int(i[2])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.muchmovies_info, 9000, i[1])
                    if not y in years: raise Exception()
                    return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                except:
                    pass
        except:
            return

    def muchmovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = self.request(u % url)[0]

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #            for i in links: sources.append({'source': i['source'], 'quality': quality, 'provider': 'Muchmovies', 'url': i['url'] + head_link})
        try:
            sources = []

            if url == None: return sources

            if url.startswith('http'): self.base_link = url

            url = urlparse.urljoin(self.base_link, url)
            url = referer = url.replace('/watching.html', '')

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            vid_id = re.findall('-(\d+)', url)[-1]

            quality = cache.get(self.muchmovies_info, 9000, vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'


            try:
                headers = {'Referer': url}

                u = urlparse.urljoin(self.base_link, self.server_link % vid_id)

                r = self.request(u, headers=headers, XHR=True)[0]

                r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
                r = zip(client.parseDOM(r, 'a', ret='onclick'), client.parseDOM(r, 'a'))
                r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

                if not episode == None:
                    r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
                else:
                    r = [i[0] for i in r]

                r = [re.findall('(\d+),(\d+)', i) for i in r]
                r = [i[0][:2] for i in r if len(i) > 0]

                links = []

                links += [{'source': 'gvideo', 'url': self.direct_link + i[1], 'direct': True} for i in r if 2 <= int(i[0]) <= 11]

                links += [{'source': 'openload.co', 'url': self.embed_link + i[1], 'direct': False} for i in r if i[0] == '14']

                links += [{'source': 'videowood.tv', 'url': self.embed_link + i[1], 'direct': False} for i in r if i[0] == '12']

                head = '|' + urllib.urlencode(headers)

                for i in links: sources.append({'source': i['source'], 'quality': quality, 'provider': 'Muchmovies', 'url': urlparse.urljoin(self.base_link, i['url']) + head})
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
        except: headers = None

        link = url.split('|')[0]

        if url.startswith('http'): self.base_link = link

        try:
            if not self.direct_link in link: raise Exception()

            vid = link.split('/')[-1]

            r = self.request(headers['Referer'], headers=headers, XHR=True)[0]

            r = client.parseDOM(r, 'img', ret='src', attrs = {'class': 'hidden'})
            if r: cookie = self.request(r[0], headers=headers, XHR=True)[4]
            else: cookie = ''

            key = '87wwxtp3dqii' ; key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'

            k = hashlib.md5(vid + key).hexdigest()
            v = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))

            cookie = '; '.join([cookie, '%s=%s' % (k, v)])

            url = urllib.quote(uncensored(vid + key2, v))
            url = '/ajax/v2_get_sources/%s?hash=%s' % (vid, url)
            url = urlparse.urljoin(self.base_link, url)

            headers['Referer'] = headers['Referer']
            headers['Cookie'] = cookie

            r = self.request(url, headers=headers, XHR=True)[0]


            url = json.loads(r)['playlist'][0]['sources']
            url = [i['file'] for i in url if 'file' in i]
            url = [client.googletag(i) for i in url]
            url = [i[0] for i in url if i]

            u = []
            try: u += [[i for i in url if i['quality'] == '1080p'][0]]
            except: pass
            try: u += [[i for i in url if i['quality'] == 'HD'][0]]
            except: pass
            try: u += [[i for i in url if i['quality'] == 'SD'][0]]
            except: pass

            url = client.replaceHTMLCodes(u[0]['url'])
            url = client.googlepass(url)
            return url
        except:
            pass

        try:
            if not self.embed_link in link: raise Exception()

            result = self.request(link, headers=headers, XHR=True)[0]

            url = json.loads(result)['embed_url']
            return url
        except:
            pass

def uncensored(a,b):
    x = '' ; i = 0
    for i, y in enumerate(a):
        z = b[i % len(b) - 1]
        y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
        x += chr(y)
    x = base64.b64encode(x)
    return x
