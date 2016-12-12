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


import re,urllib,urlparse,random
import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules.common import  random_agent, quality_tag
from BeautifulSoup import BeautifulSoup
debridstatus = control.setting('debridsources')

# if not debridstatus == 'true': raise Exception() 

class source:
    def __init__(self):
        self.domains = ['myvideolink.xyz']
        self.base_link = 'http://myvideolinks.ga'
        self.search_link = '/?s=%s+%s'
        self.ep_link = '/?s=%s'

    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			headers = {'User-Agent': random_agent()}
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			# print("MYVIDEOLINK query", query)
			link = BeautifulSoup(requests.get(query, headers=headers, timeout=20).content)
			containers = link.findAll('h2', attrs={'class': 'post-title'})
			for r in containers:
				r_href = r.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
				r_title = r.findAll('a')[0]["title"]
				r_title = r_title.encode('utf-8')
				# print("MYVIDEOLINK r", r_title, r_href)
				if year in r_title:
					movie_title = cleantitle.get(r_title)
					if cleanmovie in movie_title:
						# print("MYVIDEOLINK PASSED", r_title, r_href)
						self.zen_url.append([r_href,movie_title])


	 

			return self.zen_url
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
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			headers = {'User-Agent': random_agent()}
			cleanmovie = cleantitle.get(title)		
			title = cleantitle.getsearch(title)			
			episodecheck = 's%02de%02d' % (int(data['season']), int(data['episode']))
			
			query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(data['season']), int(data['episode']))
			query = self.ep_link % (query)
			query = urlparse.urljoin(self.base_link, query)
			link = BeautifulSoup(requests.get(query, headers=headers, timeout=20).content)
			containers = link.findAll('h2', attrs={'class': 'post-title'})
			for r in containers:
				r_href = r.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
				r_title = r.findAll('a')[0]["title"]
				r_title = r_title.encode('utf-8')
				print("MYVIDEOLINK r", r_title, r_href)
				if episodecheck in r_title.lower():
					movie_title = cleantitle.get(r_title)
					if cleanmovie in movie_title:
						print("MYVIDEOLINK PASSED", r_title, r_href)
						self.zen_url.append([r_href,movie_title])
			return self.zen_url
        except:
            return	

    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.zen_url:
				mylink = client.request(movielink)
				for item in client.parseDOM(mylink, 'div', attrs = {'class': 'entry-content'}):
					match_blocks = re.compile('<h(.+?)</h(.+?)</ul',re.DOTALL).findall(item)
					for info,links in match_blocks:
						quality = "SD"
						if "1080" in info: quality = "1080p"
						elif "720" in info: quality = "HD"				
						match = re.compile('href="([^"]+)').findall(links)			
						for url in match:
							url = url.encode('utf-8')
							if any(value in url for value in hostprDict):
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Videomega'
								host = client.replaceHTMLCodes(host)
								host = host.encode('utf-8')							
								sources.append({'source': host, 'quality': quality, 'provider': 'Myvideolink', 'url': url, 'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url