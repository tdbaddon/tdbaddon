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



import re,urllib,urlparse,random,urlresolver
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag
import requests
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    
    def __init__(self):
        self.domains = ['300movies.co']
        self.base_link = 'http://300mbmovies4u.co'
        self.search_link = '/?s=%s+%s'
        
        


    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			titlecheck = cleanmovie+year
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			
			html = BeautifulSoup(requests.get(query, headers=headers, timeout=10).content)
			
			containers = html.findAll('div', attrs={'class': 'cover'})
			
			for result in containers:
				
				r_title = result.findAll('a')[0]["title"]
				r_href = result.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
				r_title = r_title.encode('utf-8')
				c_title = cleantitle_get_2(r_title)
				if titlecheck in c_title:
					self.zen_url.append([r_href,r_title])
					print("THREEMOVIES PASSED", self.zen_url)
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
		try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			ep_search = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(ep_search).lower()
			titlecheck = cleanmovie+episodecheck
			query = self.search_link % (urllib.quote_plus(title), ep_search)
			query = urlparse.urljoin(self.base_link, query)
			print("HEVC query", query)
			html = BeautifulSoup(requests.get(query, headers=headers, timeout=10).content)
			
			containers = html.findAll('div', attrs={'class': 'cover'})
			
			for result in containers:
				print("HEVC containers", result)
				r_title = result.findAll('a')[0]["title"]
				r_href = result.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
				r_title = r_title.encode('utf-8')
				c_title = cleantitle.get(r_title)
				if titlecheck in c_title:
					self.zen_url.append([r_href,r_title])
					print("THREEMOVIES PASSED SHOW ", r_title, r_href)
			return self.url
		except:
			return
			
	
			
    def sources(self, url, hostDict, hostprDict):
	
        try:
			sources = []
			headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
			
			for movielink,title in self.zen_url:
				quality = quality_tag(title)
				html = BeautifulSoup(requests.get(movielink, headers=headers, timeout=10).content)		
				containers = html.findAll('div', attrs={'class': 'txt-block'})
				for result in containers:
					print("THREEMOVIES LINKS ",result)
					links = result.findAll('a')
					
					for r_href in links: 
						url = r_href['href']
						myurl = str(url)
						if any (value in myurl for value in hostprDict):

								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Threemovies'
								
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')														
								host = client.replaceHTMLCodes(host)
								host = host.encode('utf-8')										
								sources.append({'source': host, 'quality': quality, 'provider': 'Threemovies', 'url': url, 'direct': False, 'debridonly': True})

	 

			return sources
        except:
            return sources

    def resolve(self, url):

            return url
