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

from schism_net import OPEN_URL, OPEN_CF
from schism_commons import get_files, quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full, cleantitle_geturl

# html = scraper.get("URLTOSCRAPE").content
class source:
	def __init__(self):
		self.base_link = 'http://123movies.mx'
		self.movie_link = '/movies/%s/'
		self.ep_link = '/episodes/%s/'

	def movie(self, imdb, title, year):
		self.elysium_url = []
		try:
			url = self.base_link
			title = cleantitle_geturl(title)
			query = title
			query = self.movie_link % query
			url = urlparse.urljoin(self.base_link, query)
			r = OPEN_URL(url).content
			check = re.findall('span class="date">(.+?)</span>',r)[0]
			if year in check:
				print ("123MOVIES FOUND MOVIE", url)
				self.elysium_url.append(url)
				return self.elysium_url
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
		self.elysium_url = []
		try:
			
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			self.elysium_url = []

			title = cleantitle_geturl(title)
			query = title + "-" + season + "x" + episode
			query= self.ep_link % query
			url = urlparse.urljoin(self.base_link, query)

			self.elysium_url.append(url)
			return self.elysium_url
		except:
			return

			
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			for url in self.elysium_url:
				if url == None: return
				r = OPEN_URL(url).content
				s = re.compile('sources:\[(.+?)\]').findall(r)
				for src in s:
					print ("123MOVIES SOURCES", src)
					match = re.findall('''['"]?file['"]?\s*:\s*['"]([^'"]*)''', src)
					for href in match:
						print ("123MOVIES SOURCES 2", href)
						quality = google_tag(href)
						print ("123MOVIES SOURCES 3", href)	
						sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Onemx', 'url': href, 'direct': True, 'debridonly': False})

			return sources
		except:
			return sources


	def resolve(self, url):
		return url

