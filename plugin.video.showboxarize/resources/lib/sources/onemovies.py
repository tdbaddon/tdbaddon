# -*- coding: utf-8 -*-

'''
    Flixnet Add-on
    Copyright (C) 2016 Flixnet

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


import re,urllib,urlparse,hashlib,random,string,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunfuck

CODE = '''def retA():
    class Infix:
        def __init__(self, function):
            self.function = function
        def __ror__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __or__(self, other):
            return self.function(other)
        def __rlshift__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __rshift__(self, other):
            return self.function(other)
        def __call__(self, value1, value2):
            return self.function(value1, value2)
    def my_add(x, y):
        try: return x + y
        except Exception: return str(x) + str(y)
    x = Infix(my_add)
    return %s
param = retA()'''


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru', '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru', '123movies.unblckd.me', 'gomovies.to']
        self.base_link = 'https://gomovies.to'
        self.search_link = '/ajax/suggest_search'
        self.search_link_2 = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'        
        self.embed_link = '/ajax/load_embed/'
        self.sourcelink = '/ajax/v3_get_sources/%s?xx=%s&xy=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            t = cleantitle.get(title)

            q = self.search_link_2 % (urllib.quote_plus(cleantitle.query(title)))
            q = urlparse.urljoin(self.base_link, q)

            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': title})
            try:
                r = client.request(u, post=p, XHR=True)
                r = json.loads(r)['content']
            except:
                r = None

            if r is None:

                r = client.request(q)
                r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            else:
                r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            r = [i[0] for i in r if cleantitle.get(t) in cleantitle.get(i[1])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = self.onemovies_info(i[1])
                    if not y == year: raise Exception()
                    url = {'url': urlparse.urlparse(i[0]).path, 'episode': 0}
                    url = urllib.urlencode(url)
                    return url
                except:
                    pass
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
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

            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            q = self.search_link_2 % (urllib.quote_plus('%s - Season %s' % (data['tvshowtitle'], season)))
            q = urlparse.urljoin(self.base_link, q)

            u = urlparse.urljoin(self.base_link, self.search_link)
            p = urllib.urlencode({'keyword': '%s - Season %s' % (data['tvshowtitle'], season)})

            r = client.request(u, post=p, XHR=True)

            try:
                r = json.loads(r)['content']
            except:
                r = None

            if r is None:
                r = client.request(q)
                r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            else:
                r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            for i in r:
                try:
                    url = {'url': urlparse.urlparse(i[0]).path, 'episode': episode}
                    url = urllib.urlencode(url)
                    return url
                except:
                    pass
        except:
            return

    def onemovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = client.request(u % url)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = data['url']
            episode = data['episode']

            try:
                if int(episode) == 0:
                    episode = None
            except:
                episode = None

            url = urlparse.urljoin(self.base_link, url)
            url = url.replace('/watching.html', '')

            try:
                u = urlparse.urljoin(url, 'watching.html')
                r = client.request(u)
                r = client.parseDOM(r, 'script', ret='src')
                r = [i for i in r if 'js/client' in i]
                client_link = r[0]
            except:
                client_link = None
                pass




            vid_id = re.findall('-(\d+)', url)[-1]

            quality = self.onemovies_info(vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts':
                quality = 'CAM'
            elif quality == 'hd':
                quality = 'HD'
            else:
                quality = 'SD'

            try:
                headers = {'Referer': url}

                u = urlparse.urljoin(self.base_link, self.server_link % vid_id)

                r = client.request(u, headers=headers, XHR=True)

                r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
                r = zip(client.parseDOM(r, 'a', ret='onclick'), client.parseDOM(r, 'a'))
                r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

                if not episode is None:
                    r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
                else:
                    r = [i[0] for i in r]

                r = [re.findall('(\d+),(\d+)', i) for i in r]
                r = [i[0][:2] for i in r if len(i) > 0]

                script = client.request(client_link)
                if '$_$' in script:
                    params = self.uncensored1(script)
                elif script.startswith('[]') and script.endswith('()'):
                    params = self.uncensored2(script)
                else:
                    raise Exception()

                for i in r:
                    try:
                        if int(i[0]) <= 11:
                            u = urlparse.urljoin(self.base_link, self.sourcelink % (i[1],params['x'],params['y']))
                            r = client.request(u)
                            url = json.loads(r)['playlist'][0]['sources']
                            url = [i['file'] for i in url if 'file' in i]
                            url = [directstream.googletag(i) for i in url]
                            url = [i[0] for i in url if i]
                            for s in url:
                                sources.append({'source': 'gvideo', 'quality': s['quality'], 'language': 'en', 'url': s['url'], 'direct': True, 'debridonly': False})

                        if int(i[0]) == 14:
                            sources.append({'source': 'openload.co', 'quality': quality, 'language': 'en', 'url': urlparse.urljoin(self.base_link, self.embed_link + i[1]),'direct': False, 'debridonly': False})
                    except:
                        pass

            except:
                pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if self.embed_link in url:
                result = client.request(url, XHR=True)
                url = json.loads(result)['embed_url']
                return url

            try:
                if not url.startswith('http'):
                    url = 'http:' + url

                for i in range(3):
                    u = directstream.googlepass(url)
                    if not u == None: break

                return u
            except:
                return
        except:
            return

    def uncensored(a, b):
        x = '' ; i = 0
        for i, y in enumerate(a):
            z = b[i % len(b) - 1]
            y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
            x += chr(y)
        x = base64.b64encode(x)
        return x

    def uncensored1(self, script):
        try:
            script = '(' + script.split("(_$$)) ('_');")[0].split("/* `$$` */")[-1].strip()
            script = script.replace('(__$)[$$$]', '\'"\'')
            script = script.replace('(__$)[_$]', '"\\\\"')
            script = script.replace('(o^_^o)', '3')
            script = script.replace('(c^_^o)', '0')
            script = script.replace('(_$$)', '1')
            script = script.replace('($$_)', '4')

            vGlobals = {"__builtins__": None, '__name__': __name__, 'str': str, 'Exception': Exception}
            vLocals = {'param': None}
            exec (CODE % script.replace('+', '|x|'), vGlobals, vLocals)
            data = vLocals['param'].decode('string_escape')
            x = re.search('''xx=['"]([^"']+)''', data).group(1)
            y = re.search('''xy=['"]([^"']+)''', data).group(1)
            return {'x': x, 'y': y}
        except:
            pass

    def uncensored2(self, script):
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            x = re.search('''xx=['"]([^"']+)''', js).group(1)
            y = re.search('''xy=['"]([^"']+)''', js).group(1)
            return {'x': x, 'y': y}
        except:
            pass