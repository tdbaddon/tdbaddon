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
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
debridstatus = control.setting('debridsources')
from resources.lib.modules.common import  random_agent
from BeautifulSoup import BeautifulSoup
from schism_net import OPEN_URL
import requests
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['newmyvideolink.xyz']
        self.base_link = control.setting('myvideolink_base')
        if self.base_link == '' or self.base_link == None:self.base_link = 'http://newmyvideolink.xyz'

		
        self.search_link = '?s=%s+%s'
	

			# r = client.parseDOM(req, 'h2', attrs = {'class': 'post-title'})
			
			# r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
	
    def movie(self, imdb, title, year):
		self.zen_url = []

		try:
			if not debridstatus == 'true': raise Exception()

			print( "MYVIDEOLINK 2")
		  	self.real_link = self.base_link

			
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			type = 'zen_movies'
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.real_link, query)
			req = OPEN_URL(query).content

			r = client.parseDOM(req, 'h2', attrs = {'class': 'post-titl.+?'})
			r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
			r = [(i[0][0], i[1][0]) for i in r ]	
			r = [(i[0], i[1]) for i in r if cleanmovie in cleantitle.get(i[1]) and year in i[1]]
			u = [(i[0].encode('utf-8'), i[1].encode('utf-8'), type) for i in r]
			self.zen_url += u
			print ("MOVIES PASSED MYVIDEOLINK", self.zen_url)
			 	
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
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			self.real_link = self.base_link
			type = 'zen_shows'
			data['season'], data['episode'] = season, episode
			episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(episodecheck).lower()
			query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),query)
			query = urlparse.urljoin(self.real_link, query)
			
			req = OPEN_URL(query).content
			r = client.parseDOM(req, 'h2', attrs = {'class': 'post-titl.+?'})
			r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
			r = [(i[0][0], i[1][0]) for i in r ]	
			r = [(i[0], i[1]) for i in r if cleanmovie in cleantitle.get(i[1]) and episodecheck in cleantitle.get(i[1])]
			u = [(i[0].encode('utf-8'), i[1].encode('utf-8'), type) for i in r]
			self.zen_url += u
			print ("MYVIDEOLINK SHOWS", self.zen_url)

			
			
			
			
			return self.zen_url
        except:
            return			
			
    def get_refresh(self):
			r = OPEN_URL(self.base_link, timeout='10').text
			print ("MYVIDEOLINK OPENURL", r)
			checkrefresh = re.findall('<div class="post">(.+?)</div>', r)[0]
			checkrefresh2 = re.findall('<meta http-equiv="refresh"', r)[0]
			if checkrefresh and "http" in checkrefresh:
				print ("MYVIDEOLINK FOUND REDIRECT") 
				s = checkrefresh.encode('utf-8')
				print ("MYVIDEOLINK REDIRECT", s) 
				
				if not s.startswith("http"): s = "http://" + s
				url = s.encode('utf-8')
				return url
			elif checkrefresh2:
				print ("MYVIDEOLINK FOUND REDIRECT") 
				s = re.findall("URL='(http.+?)'", r)[0]
				print ("MYVIDEOLINK REDIRECT", s) 
				url = s.encode('utf-8')
				return url			
				
				
			else:
				url = client.request(self.base_link, output='geturl')
				return url
			
	
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for url,title,type in self.zen_url:

					req = OPEN_URL(url).content
					pattern = '<h1>(.*?)</h1(.*?)</ul>'
					html = re.compile(pattern, re.DOTALL).findall(req)
					for titles, block in html:
				
						quality = "SD"
						quality = quality_tag(titles)
						info = ''
						if "hevc" in titles.lower(): info = "HEVC"	
						info = get_size(block)
							
						links = re.compile('href="([^"]+)').findall(block)
						for href in links:
								
							
							if any(value in href for value in hostprDict):
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
								except: host = 'Videomega'
								url = client.replaceHTMLCodes(href)
								url = url.encode('utf-8')
								sources.append({'source': host, 'quality': quality, 'provider': 'Myvideolink', 'url': url, 'info': info,'direct': False, 'debridonly': True})
							
			return sources
        except:
            return sources


    def resolve(self, url):

            return url