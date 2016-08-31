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

import re,urllib,urlparse,json,base64,time,string,random

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['movieshd.tv', 'movieshd.is', 'cartoonhd.website']
        self.base_link = 'http://cartoonhd.website'
        self.search_link = '/api/v2/cautare/aug'


    def movie(self, imdb, title, year):
        try:
            tk = cache.get(self.cartoonhd_token, 8)

            st = self.cartoonhd_set() ; rt = self.cartoonhd_rt(tk + st)

            tm = int(time.time() * 1000)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)

            post = {'q': title.lower(), 'limit': '20', 'timestamp': tm, 'verifiedCheck': tk, 'set': st, 'rt': rt}
            post = urllib.urlencode(post)

            r = client.request(url, post=post, headers=headers)
            r = json.loads(r)

            t = cleantitle.get(title)

            r = [i for i in r if 'year' in i and 'meta' in i]
            r = [(i['permalink'], i['title'], str(i['year']), i['meta'].lower()) for i in r]
            r = [i for i in r if 'movie' in i[3]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            tk = cache.get(self.cartoonhd_token, 8)

            st = self.cartoonhd_set() ; rt = self.cartoonhd_rt(tk + st)

            tm = int(time.time() * 1000)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)

            post = {'q': tvshowtitle.lower(), 'limit': '20', 'timestamp': tm, 'verifiedCheck': tk, 'set': st, 'rt': rt}
            post = urllib.urlencode(post)

            r = client.request(url, post=post, headers=headers)
            r = json.loads(r)

            t = cleantitle.get(tvshowtitle)

            r = [i for i in r if 'year' in i and 'meta' in i]
            r = [(i['permalink'], i['title'], str(i['year']), i['meta'].lower()) for i in r]
            r = [i for i in r if 'tv' in i[3]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            r = '%s/season/%01d/episode/%01d' % (url, int(season), int(episode))

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def cartoonhd_token(self):
        try:
            token = client.request(self.base_link)
            token = re.findall("var\s+tok\s*=\s*'([^']+)", token)[0]
            return token
        except:
            return


    def cartoonhd_set(self):
        return ''.join([random.choice(string.ascii_letters) for _ in xrange(25)])


    def cartoonhd_rt(self, s, shift=13):
        s2 = ''
        for c in s:
            limit = 122 if c in string.ascii_lowercase else 90
            new_code = ord(c) + shift
            if new_code > limit:
                new_code -= 26
            s2 += chr(new_code)
        return s2


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, output='extended')

            cookie = r[4] ; headers = r[3] ; result = r[0]

            auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url


            u = '/ajax/embeds.php'
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            c = client.request(u, post=post, headers=headers, output='cookie', error=True)

            headers['Cookie'] = cookie + '; ' + c

            r = client.request(u, post=post, headers=headers)
            r = str(json.loads(r))
            r = client.parseDOM(r, 'iframe', ret='.+?') + client.parseDOM(r, 'IFRAME', ret='.+?')


            links = []

            for i in r:
                try: links += [{'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i, 'direct': True}]
                except: pass

            links += [{'source': 'openload.co', 'quality': 'SD', 'url': i, 'direct': False} for i in r if 'openload.co' in i]

            links += [{'source': 'videomega.tv', 'quality': 'SD', 'url': i, 'direct': False} for i in r if 'videomega.tv' in i]


            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'MoviesHD', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


