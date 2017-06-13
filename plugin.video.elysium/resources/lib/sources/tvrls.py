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



import re,urllib,urlparse,random
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['tv-release.net']
        self.base_link = 'http://tv-release.pw'
        self.search_link = '/?s=%s+%s'
        print ("TVRLS START")		

    def movie(self, imdb, title, year):
        self.elysium_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			count = 0
			self.elysium_url = []
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			titlecheck = cleanmovie+year
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'id': 'content'})
			for containers in r:
				print ("TVRLS containers", containers)
				match = re.compile("<a href='(.+?)'>(.+?)</a>").findall(containers)
				for movielink,title2 in match:
					title3 = cleantitle_get_2(title2)
					if titlecheck in title3:
						if "1080" in title2 or "720" in title2:
							count += 1
							if not count > 6:				
								self.elysium_url.append([movielink,title2])
			return self.elysium_url
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
        self.elysium_url = []	
        try:
			count = 0
			if not debridstatus == 'true': raise Exception()	
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode

			title = cleantitle.getsearch(title)
			print ("TVRLS EPISODES title", title)	
			cleanmovie = cleantitle.get(title)
			print ("TVRLS EPISODES cleanmovie", cleanmovie)	
			episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(episodecheck)
			episodecheck = episodecheck.lower()
			titlecheck = cleanmovie+episodecheck
			print ("TVRLS EPISODES titlecheck", titlecheck)	

			query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),query)
			query = urlparse.urljoin(self.base_link, query)
			print ("TVRLS query", query)			
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'id': 'content'})
			for containers in r:
				print ("TVRLS containers", containers)
				match = re.compile("<a href='(.+?)'>(.+?)</a>").findall(containers)
				for movielink,title2 in match:
					print ("TVRLS movielink title2", title2, movielink)
					title = cleantitle.get(title2)
					if titlecheck in title:
						if "1080" in title2 or "720" in title2:
							count += 1
							if not count > 6:
								self.elysium_url.append([movielink,title2])
			return self.elysium_url
        except:
            return

			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.elysium_url:
				mylink = client.request(movielink)
				info = get_size(title)
	
				quality = quality_tag(title)
				
				match2 = re.compile("<a target='_blank' href='(.+?)'>").findall(mylink)			
				for url in match2:
						if any(value in url for value in hostprDict):
							if "http" in url:
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Videomega'
								host = client.replaceHTMLCodes(host)
								host = host.encode('utf-8')							
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')								
								sources.append({'source': host, 'quality': quality, 'provider': 'Tvrls', 'url': url, 'info': info, 'direct': False, 'debridonly': True})

			return sources
        except:
            return sources


    def resolve(self, url):
            return url