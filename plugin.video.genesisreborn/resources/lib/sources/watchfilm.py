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
import re,urllib,urlparse,base64
import requests
from resources.lib.modules import client
from resources.lib.modules import directstream
from BeautifulSoup import BeautifulSoup
from resources.lib.modules import jsunpack

from schism_net import OPEN_URL
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
	def __init__(self):
		self.base_link = 'http://rs333.watchfilm.me'
		self.movie_link = '/movies/%s/'
		self.ep_link = '/episode/%s/'

	def movie(self, imdb, title, year):
		self.genesisreborn_url = []
		try:
			
			# print("WATCHCARTOON")
			title = cleantitle_query(title)
			title = title.replace(' ','-')
			query = self.movie_link % (title)
			url = urlparse.urljoin(self.base_link, query)
			return url
					
			
		except:
			return
			
	# http://blackcinema.org/episodes/ash-vs-evil-dead-1x2/		
	def tvshow(self, imdb, tvdb, tvshowtitle, year):
		try:
			url = {'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return			

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		self.genesisreborn_url = []
		try:
			
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			episodeid = "%01dx%01d" % (int(data['season']) , int(data['episode']))
			title = cleantitle_query(title)
			title = title.replace(' ','-')
			query = title + "-" + episodeid
			query= self.ep_link % query
			url = urlparse.urljoin(self.base_link, query)
			print("Watchfilm TV SHOW", url)

			return url
		except:
			return
		
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			
			if url == None: return
			try:
				referer = url
				link = OPEN_URL(url, timeout='10')
				print("Watchfilm link", link.content)
				html = link.content
				headers = {'Referer': referer}	
				r = re.compile('<a href="(.+?)" target="streamplayer">').findall(html)
				for result in r:
					print("Watchfilm SOURCES", result)
					result = result.encode('utf-8')
					if result.startswith("//"): result = "http:" + result
						
					if "player.watchfilm.to" in result:
						try:
							
							s = OPEN_URL(result, headers=headers)
							s = s.content
							print ("WATCHFILM RESULT", s)
							check1 = re.findall("abouttext:\s*'(.+?)',", s)[0]
							check2 = re.compile('file:\s*"(.+?)",label:"(.+?)",').findall(s)
							check3 = re.compile('file":"(.+?)","res":"(.+?)"').findall(s)
														
							if check1:
								try:
									print ("WATCHFILM FOUND CHECK 1")
									quality = quality_tag(check1)
									h = re.findall("aboutlink:\s*'(.+?)'," , s)[0]
									if h:
										h = h.encode('utf-8')
										sources.append({'source': 'cdn', 'quality':quality, 'provider': 'Watchfilm', 'url': h, 'direct': True, 'debridonly': False})
								except:
									pass
								h2 = re.findall('var ff =\s*"(.+?)";', s)[0]
								if h2:
									try:
										h2 = h2.encode('utf-8')
										host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(h2.strip().lower()).netloc)[0]
										if host in hostDict: sources.append({'source': host, 'quality':quality, 'provider': 'Watchfilm', 'url': h2, 'direct': False, 'debridonly': True})
									except:
										pass
							if check2:
								print ("WATCHFILM FOUND CHECK 2")
								try:
									for href, quality in check2:
										href = href.encode('utf-8')
										quality = quality_tag(quality)
										
										sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Watchfilm', 'url': href, 'direct': True, 'debridonly': False})
								except:
									pass
									
							if check3:
								print ("WATCHFILM FOUND CHECK 3")
								try:
									for href, quality in check3:
										href = href.encode('utf-8')
										quality = quality_tag(quality)
										sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Watchfilm', 'url': href, 'direct': True, 'debridonly': False})
								except:
									pass

						except:
							pass
							


			except:
				pass

			return sources
		except:
			return sources


	def resolve(self, url):

		return url

