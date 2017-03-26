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
from resources.lib.modules import control
from schism_net import OPEN_URL, OPEN_CF
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full, cleantitle_geturl

# html = scraper.get("URLTOSCRAPE").content
class source:
	def __init__(self):

		self.base_link = control.setting('pftv_base')
		if self.base_link == '' or self.base_link == None:self.base_link = 'http://project-free-tv.im'

		self.movie_link = '/movies/%s/'
		self.ep_link = '/episode/%s/'
		
		
	def movie(self, imdb, title, year):
		self.zen_url = []
		try:
			url = self.base_link
			title = cleantitle_geturl(title)
			query = title + "-" + year
			query = self.movie_link % query
			url = urlparse.urljoin(self.base_link, query)
			print("PROJECTFREETV URL", url)
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
			self.zen_url = []
			
			title = cleantitle_geturl(title)
			query = title + "-season-" + season + "-episode-" + episode
			query= self.ep_link % query
			url = urlparse.urljoin(self.base_link, query)

			
			return url
		except:
			return

			
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
				# for url in self.zen_url:
				if url == None: return
				print ("PROJECTFREETV SOURCE", url)
				r = OPEN_URL(url).content
				links = client.parseDOM(r, 'tr')
				for i in links:
					try:
						print ("PROJECTFREETV SOURCE r2", i)
						url = re.findall('callvalue\((.+?)\)', i)[0]
						url = re.findall('(http.+?)(?:\'|\")', url)[0]
						url = replaceHTMLCodes(url)
						url = url.encode('utf-8')
						print ("PROJECTFREETV SOURCE r3", url)

						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
						host = host.encode('utf-8')
					
						if not host in hostDict: raise Exception()


						sources.append({'source': host, 'quality':'SD', 'provider': 'Projectfree', 'url': url, 'direct': False, 'debridonly': False})
					except:
						pass

				return sources
		except:
			return sources


	def resolve(self, url):
		return url

