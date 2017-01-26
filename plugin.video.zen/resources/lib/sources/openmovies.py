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
import re,urllib,urlparse,base64
import requests
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag

class source:
	def __init__(self):
		self.base_link = 'http://openloadmovies.net'
		self.movie_link = '/movies/%s/'
		self.ep_link = '/episodes/%s/'

	def movie(self, imdb, title, year):
		self.zen_url = []
		try:
			headers = {'User-Agent': random_agent()}
			
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			title = title + "-" + year
			query = self.movie_link % title
			u = urlparse.urljoin(self.base_link, query)
			self.zen_url.append(u)
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
			headers = {'User-Agent': random_agent()}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			query = title + "-" + season + "x" + episode
			query= self.ep_link % query
			u = urlparse.urljoin(self.base_link, query)
			# print("OPENMOVIES SHOWS", u)
			self.zen_url.append(u)
			return self.zen_url
		except:
			return

			
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			headers = {'User-Agent': random_agent()}
			for url in self.zen_url:
				if url == None: return
				
				html = requests.get(url, headers=headers, timeout=10).text
				
				match = re.search('sources\s*:\s*\[(.*?)\]', html, re.DOTALL)
				if not match:	match = re.search('sources\s*:\s*\{(.*?)\}', html, re.DOTALL)
				if match:
					for match in re.finditer('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', match.group(1), re.DOTALL):
						try:
							stream_url, label = match.groups()
							stream_url = stream_url.replace('\/', '/')
							stream_url = stream_url.encode('utf-8')
							

							quality = quality_tag(label)
							# print("OpenMovies SOURCE", stream_url, label)
							sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Openmovies', 'url': stream_url, 'direct': True, 'debridonly': False})
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

