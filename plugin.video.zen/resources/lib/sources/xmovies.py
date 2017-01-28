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


import re,urllib,urlparse,json,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream

class source:
    def __init__(self):
        self.domains = ['xmovies8.tv']
        self.base_link = 'http://xmovies8.ru'
        self.search_link = '/movies/search?s=%s'
        self.moviesearch_link = '/movie/%s-%s/'
        self.tv_link = '/movie/%s'
		
    def movie(self, imdb, title, year):
        try:
            url = self.moviesearch_link % (geturl(title.replace('\'', '-')), year)
            main = urlparse.urljoin(self.base_link, url)
            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1')
            r = client.parseDOM(r, 'title')[0]
            if not '(%s)' % year in r: raise Exception()
            url = client.request(main, output='geturl')
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
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			seasoncheck = 'season+%s' % (int(data['season']))
			seasonclean = 'season%s' % (int(data['season']))
			episodecheck = 'episode ' + episode
			query = urlparse.urljoin(self.base_link, self.tv_link)
            
			query = query % (geturl(title.replace('\'', '-')))
			print ('XMOVIES TV r1',query)
			slink = client.request(query)
			r = client.parseDOM(slink, 'h2', attrs = {'class': 'tit'})
			r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
			r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
 			print ('XMOVIES TV r2',r)
          
			r = [i[0] for i in r if cleanmovie in cleantitle.get(i[1]) and seasonclean in cleantitle.get(i[1])][0]
 			print ('XMOVIES TV r3',r)
			url = re.findall('(?://.+?|)(/.+)', r)[0]
			url = client.replaceHTMLCodes(url)
			url = url.encode('utf-8')
			url = urlparse.urljoin(self.base_link, url)
			if not 'watching.html' in url: url = url + 'watching.html'
			url = client.request(url, output="geturl")
			link = client.request(url)
			
			for item in client.parseDOM(link, 'div', attrs = {'class': 'ep_link full'}):
				match = re.compile('<a href="(.*?)" class="">(.*?)</a>').findall(item)
				match2 = re.compile('<a href="(.*?)" class=".*?">(.*?)</a>').findall(item)
				for url,episodes in match + match2:
					episodes = episodes.lower()
					if episodecheck == episodes:
						if not "http:" in url:
							url = "http:" + url
							url = client.replaceHTMLCodes(url)
							url = url.encode('utf-8')							
							print "XMOVIES TV episodes %s %s " % (url, episodes)
							return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
			
            if url == None: return sources
            print ('XMOVIES TV URLS', url)
            if "episode_id=" in url: 
				url = referer = url 


            else:
				url = path = re.sub('/watching.html$', '', url.strip('/'))
				url = referer = url + '/watching.html'

            p = client.request(url)
            p = re.findall("data\s*:\s*{\s*id:\s*(\d+),\s*episode_id:\s*(\d+),\s*link_id:\s*(\d+)", p)[0]
            p = urllib.urlencode({'id': p[0], 'episode_id': p[1], 'link_id': p[2], '_': int(time.time() * 1000)})

            headers = {
            'Accept-Formating': 'application/json, text/javascript',
            'X-Requested-With': 'XMLHttpRequest',
            'Server': 'cloudflare-nginx',
            'Referer': referer}

            r = urlparse.urljoin(self.base_link, '/ajax/movie/load_episodes')
            r = client.request(r, post=p, headers=headers)
            r = re.findall("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?", r)
            r = [i for i in r if int(i[1]) >= 720]

            for u in r:
                try:
                    p = urllib.urlencode({'id': u[0], 'quality': u[1], '_': int(time.time() * 1000)})
                    u = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v2')

                    u = client.request(u, post=p, headers=headers)
                    u = json.loads(u)['playlist']
                    u = client.request(u, headers=headers)
                    u = json.loads(u)['playlist'][0]['sources']
                    u = [i['file'] for i in u if 'file' in i]

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Xmovies', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return
			
			
def geturl(title):
    if title == None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    return title


