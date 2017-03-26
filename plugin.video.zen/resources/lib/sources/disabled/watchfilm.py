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
		self.base_link = 'http://watchfilm.to'
		self.movie_link = '/movies/%s/'
		self.ep_link = '/episode/%s/'

	def movie(self, imdb, title, year):
		self.zen_url = []
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
		self.zen_url = []
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
					
				link = OPEN_URL(url, timeout='10')
				print("Watchfilm link", link.content)
				html = link.content
					
				r = re.compile('<a href="(.+?)" target="streamplayer">').findall(html)
				for result in r:
					print("Watchfilm SOURCES", result)
					result = result.encode('utf-8')
					
					if result.startswith("//"): result = "http:" + result
						
					if "player.watchfilm.to" in result:
						try:
							s = OPEN_URL(result, timeout='10')
							s = s.content
							match = re.compile('file:\s*"(.+?)",label:"(.+?)",').findall(s)
							for href, quality in match:
								quality = google_tag(href)
								print("WONLINE SCRIPTS", href,quality)
								sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Watchfilm', 'url': href, 'direct': True, 'debridonly': False})
						except:
							pass
						try:
							s = OPEN_URL(result, timeout='10')
							s = s.content

							match = re.compile('var ff =\s*"(.+?)";').findall(s)
							for href in match:
								
								quality = "SD"
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
							
								except: host = 'none'
								url = replaceHTMLCodes(href)
								url = url.encode('utf-8')
								if host in hostDict: sources.append({'source': host, 'quality':quality, 'provider': 'Watchfilm', 'url': href, 'direct': False, 'debridonly': False})
						except:
							pass

			except:
				pass

			return sources
		except:
			return sources


	def resolve(self, url):

		return url

