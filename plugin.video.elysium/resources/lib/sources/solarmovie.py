# -*- coding: utf-8 -*-
'''
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


import re,urllib,urlparse,hashlib,random,string,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream

import requests
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import random_agent
from resources.lib.modules import control
from schism_net import OPEN_URL
from schism_titles import clean_html
from schism_meta import meta_quality, meta_gvideo_quality

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
        self.language = ['en']

        self.base_link = 'https://solarmoviez.to'

        self.search_link = '/search/%s.html'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'
        self.session = requests.Session()

    def request(self, url, headers, post):
        try:
            r = client.request(url, headers=headers, post=post)
            if r == None: return r

            if 'internetmatters.org' in r:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = urlparse.urljoin(self.base_link_2, url)
                r = client.request(url, headers=headers, post=post)

            return r
        except:
            return


    def movie(self, imdb, title, year):
        try:
            self.elysium = []

            cleaned_title = cleantitle.get(title)
            title = cleantitle.getsearch(title)
            q = self.search_link % (urllib.quote_plus(title))
            r = urlparse.urljoin(self.base_link, q)
            html = BeautifulSoup(OPEN_URL(r).content)
            print ("ONEMOVIES EPISODES", html)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for link in containers:
                    link_title = link('a')[0]['title'].encode('utf-8')
                    href = link('a')[0]['href'].encode('utf-8')
                    info = link('a')[0]['data-url'].encode('utf-8')
                    if cleantitle.get(link_title) == cleaned_title:
                        info = urlparse.urljoin(self.base_link, info)
                        html = OPEN_URL(info).content
                        pattern = '<div class="jt-info">%s</div>' % year
                        match = re.findall(pattern, html)
                        if match:
							url = client.replaceHTMLCodes(href)
							url = {'url': url, 'type': 'movie' }
							url = urllib.urlencode(url)
							
							print("SOLARMOVIE PASSED", url) 
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
            title = cleantitle.getsearch(data['tvshowtitle'])

            season = '%01d' % int(season)
            episode = '%01d' % int(episode)
            query = (urllib.quote_plus(title))
            q = self.search_link % (query)
            r = urlparse.urljoin(self.base_link, q)
            checkseason = cleantitle.get(title) + "season" + season
            html = BeautifulSoup(OPEN_URL(r).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for link in containers:
                    link_title = link('a')[0]['title'].encode('utf-8')
                    href = link('a')[0]['href'].encode('utf-8')
                    if cleantitle.get(link_title) == checkseason:
						url = {'url': href, 'type': 'tv_shows' , 'episode' : episode }
						url = urllib.urlencode(url)
							
						print("SOLARMOVIE PASSED", url) 
						return url

        except:
            return


    def onemovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = self.request(u % url, headers=None, post=None)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return



    def sources(self, url, hostDict, hostprDict):
        original_url = url
        sources = []
        results = []
        try:
            

            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = data['url'].encode('utf-8')
            type = data['type'].encode('utf-8')
            referer = url

            url = url.replace('/watching.html', '')
            url = url.replace('.html','')
            if not url.endswith('/'): url = url + "/watching.html"
            else : url = url + "watching.html"
			

            referer=url
		
            request = OPEN_URL(url)
            html = request.content

            try:mid = re.compile('name="movie_id" value="(.+?)"').findall(html)[0]
            except:mid = re.compile('id: "(.+?)"').findall(html)[0]
					
						
            time_now = int(time.time() * 10000)
            EPISODES = '/ajax/v4_movie_episodes/%s' % (mid)
            EPISODES = urlparse.urljoin(self.base_link, EPISODES)	
            r = OPEN_URL(EPISODES).content
            r = clean_html(r)
            print("SOLARMOVIE SOURCES", EPISODES) 				
            match = re.compile('data-id="(.+?)" id=".+?">.+?a href=".+?"\s*title="(.+?)">').findall(r)
            for data_id,t, in match:
				if type == 'tv_shows':
					episode = data['episode'].encode('utf-8')
					
					episode = "%02d" % int(episode)
					ep_check1 = episode + ":"
					ep_check2 = "Episode %s:" % episode
					
					if ep_check1 in t or ep_check2 in t: results.append(data_id)
				else: results.append(data_id)	
				
            for data_id in results:
					try:
							s = '/ajax/movie_token'
							src = urlparse.urljoin(self.base_link, s)	
							payload = {'eid':data_id, 'mid': mid, '_':time_now}
							

							data = OPEN_URL(src, params=payload, XHR=True).content
							
							if '$_$' in data:
								p = self.uncensored1(data)
								
							elif data.startswith('[]') and data.endswith('()'):
								
								p = self.uncensored2(data)
								
							else:
								continue

							xx ,xy = p
							
							print ("UNCENSORED DATA", xx, xy, data_id)
							if xx:
								servers = '/ajax/movie_sources/%s' % (data_id)
								payload = {'x':xx, 'y':xy}
								srv = urlparse.urljoin(self.base_link, servers)	
								
								srv = OPEN_URL(srv, params=payload, XHR=True).json()
								
								playlist = srv['playlist'][0]['sources']
								for u in playlist:
									url = u['file'].encode('utf-8')
									quality = meta_gvideo_quality(url)
									sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Solarmovie', 'url': url, 'direct': True, 'debridonly': False})
						


					except:
						continue

        except:
            pass
        return sources


    def resolve(self, url):
            return url






    def uncensored(a, b):
        x = '' ; i = 0
        for i, y in enumerate(a):
            z = b[i % len(b) - 1]
            y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
            x += chr(y)
        x = base64.b64encode(x)
        return x

    def uncensored1(self, data):
        try:
            script = data
            
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
            data = re.compile('''=['"]([^"^']+?)['"]''').findall(data)
            xx = data[0]
            xy = data[1]
            return xx, xy
        except:
            pass

    def uncensored2(self, script):
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            data = re.compile('''=['"]([^"^']+?)['"]''').findall(js)
            xx = data[0]
            xy = data[1]
            return xx, xy
        except:
            pass


