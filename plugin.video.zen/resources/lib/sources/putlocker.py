# -*- coding: utf-8 -*-

'''
    zen Add-on
    Copyright (C) 2016 zen

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

from resources.lib.modules import control
class source:
    def __init__(self):
        self.base_link = control.setting('putlocker_base')
        if self.base_link == '' or self.base_link == None: self.base_link = 'http://cartoonhd.online'
		
        self.social_lock = '0A6ru35yevokjaqbb8'
        self.search_link = 'http://api.cartoonhd.online/api/v1/' + self.social_lock
        self.shows_link = '/show/%s/season/%s/episode/%s'
        self.movies_link = '/movie/%s'

    def movie(self, imdb, title, year):
        try:


            query = self.movies_link % (cleantitle.geturl(title))
            print ("PUTLOCKER query", query)
            url = urlparse.urljoin(self.base_link, query)
            print ("PUTLOCKER url", url)
            url = url.encode('utf-8')
            url = client.request(url, output='geturl')
            url = url.encode('utf-8')		
           
			
            return url
        except:
            return




    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
           
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
          
            title = cleantitle.geturl(title)
            query = self.shows_link % (title, int(season), int(episode))
          
            url = urlparse.urljoin(self.base_link, query)
            
            url = url.encode('utf-8')
            url = client.request(url, output='geturl')
            url = url.encode('utf-8')			
            
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources


            if not "http" in url: url = urlparse.urljoin(self.base_link, url)
          
            r = client.request(url, output='extended')

            
            cookie = r[4] ; headers = r[3] ; result = r[0]

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url


            u = '/ajax/tnembeds.php'
            self.base_link = client.request(self.base_link, output='geturl')
            u = urlparse.urljoin(self.base_link, u)
            # print ("PUTLOCKER u", u)
            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)
            # print ("PUTLOCKER post", post)
            r = client.request(u, post=post, XHR=True)
            # print ("PUTLOCKER r2", r)
            r = str(json.loads(r))
            # print ("PUTLOCKER r3", r)
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)
            print ("PUTLOCKER r4", r)
            for i in r:
				if "google" in i:
					try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Putlocker', 'url': i, 'direct': True, 'debridonly': False})
					except: continue
				else:
					try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i.strip().lower()).netloc)[0]
					except: host = 'none'
					if not host in hostDict:continue
					sources.append({'source':host, 'quality': 'SD', 'provider': 'Putlocker', 'url': i + "=url_resolver", 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources
			
			
    def resolve(self, url):
            if "url_resolver" in url: url = url.replace('=url_resolver', '')

            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
		
			
    def movieshd_token(self):
        try:
            token = client.request(self.base_link)
            token = re.findall("var\s+tok\s*=\s*'([^']+)", token)[0]
            return token
        except:
            return


    def movieshd_set(self):
        return ''.join([random.choice(string.ascii_letters) for _ in xrange(25)])

    def movieshd_sl(self):
        return hashlib.md5(base64.encodestring('0A6ru35yyi5yn4THYpJqy0X82tE95btV')+self.social_lock).hexdigest()


    def movieshd_rt(self, s, shift=13):
        s2 = ''
        for c in s:
            limit = 122 if c in string.ascii_lowercase else 90
            new_code = ord(c) + shift
            if new_code > limit:
                new_code -= 26
            s2 += chr(new_code)
        return s2

