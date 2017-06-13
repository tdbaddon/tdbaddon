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

from schism_net import OPEN_URL
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full, cleantitle_geturl

class source:
	def __init__(self):
		self.base_link = 'http://watchfilm.to'
		self.movie_link = 'http://movie-time.me/%s-%s/'
		self.ep_link = 'http://watchseries-online.pl/episode/%s'

	def movie(self, imdb, title, year):
		self.elysium_url = []
		try:
				
			# print("WATCHCARTOON")
			title = cleantitle_geturl(title)
			url = self.movie_link % (title, year)
			url = url.encode('utf-8')
			print("WSO URL", url)
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
		self.elysium_url = []
		try:
			
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			episodeid = "s%02de%02d" % (int(data['season']) , int(data['episode']))
			title = cleantitle_geturl(title)

			query = title + "-" + episodeid
			url= self.ep_link % query

			print("Watchfilm TV SHOW", url)

			return url
		except:
			return
		
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			
			if url == None: return

					
			link = OPEN_URL(url, timeout='10').content
			html = BeautifulSoup(link)
			r = html.findAll('div', attrs={'class': 'play-btn'})

			for result in r:
				href = result.findAll('a')[0]['href'].encode('utf-8')
				try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
				except: host = 'none'
				quality = 'SD'

				url = replaceHTMLCodes(href)
				url = url.encode('utf-8')
				if host in hostDict: sources.append({'source': host, 'quality':quality, 'provider': 'Wso', 'url': href, 'direct': False, 'debridonly': False})




			return sources
		except:
			return sources


	def resolve(self, url):

		return url

