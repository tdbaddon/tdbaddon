# -*- coding: utf-8 -*-

'''
Copyright Zen Addon 2016

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
from schism_net import OPEN_URL
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes , get_size, get_host
from schism_titles import cleantitle_get, cleantitle_get_2, cleantitle_query, cleantitle_get_full, cleantitle_geturl
# html = scraper.get("URLTOSCRAPE").content
class source:
	def __init__(self):
		self.base_link = 'http://vumoo.li'
		self.search_link = '/videos/search/?search=%s'
		self.player_link = '/api/getContents?id=%s&p=1&imdb=%s'

	def movie(self, imdb, title, year):
		self.zen_url = []
		try:
			title = cleantitle_query(title)
			titlecheck = cleantitle_get(title)
			query = self.search_link % (urllib.quote_plus(title))
			url = urlparse.urljoin(self.base_link, query)
			# print ("ZEN SCRAPER ITEMS", url)
			r = OPEN_URL(url).content
			r = BeautifulSoup(r)
			r = r.findAll('article', attrs={'class': 'movie_item'})
			for u in r:
				
				h = u.findAll('a')[0]['href'].encode('utf-8')
				t = u.findAll('a')[0]['data-title'].encode('utf-8')	
				# print ("ZEN SCRAPER ITEMS", titlecheck, t,h)
				if titlecheck == cleantitle_get(t):
					type = 'movies'
					season = ''
					episode = ''
					self.zen_url.append([h,imdb,type,season,episode])
					# print ("ZEN SCRAPER ITEMS PASSED", h) 
					return self.zen_url
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
			title = cleantitle_query(title)
			titlecheck = cleantitle_get(title)
			query = self.search_link % (urllib.quote_plus(title))
			url = urlparse.urljoin(self.base_link, query)
			# print ("ZEN SCRAPER ITEMS", url)
			r = OPEN_URL(url).content
			r = BeautifulSoup(r)
			r = r.findAll('article', attrs={'class': 'movie_item'})
			for u in r:
				h = u.findAll('a')[0]['href'].encode('utf-8')
				t = u.findAll('a')[0]['data-title'].encode('utf-8')	
				# print ("ZEN SCRAPER ITEMS", titlecheck, t,h)
				if titlecheck == cleantitle_get(t):
					type = 'shows'
					self.zen_url.append([h,imdb,type,season,episode])
					# print ("ZEN SCRAPER ITEMS PASSED", h) 
					return self.zen_url
		except:
			return

			
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			for url,imdb,type,season,episode in self.zen_url:
				player_items = []
				if url == None: return
				
				url = urlparse.urljoin(self.base_link, url)
				print ("ZEN URL SOURCES", url)
				r = OPEN_URL(url).content
				if not imdb in r: raise Exception()
				if type == "movies":
					link_id = re.findall("p_link_id='(.+?)'",r)[0]
					link_id = link_id.encode('utf-8')
					api_link = "/api/plink?id=%s&res=" % link_id
					player_items.append(api_link)
				elif type == "shows":
					pattern = 'season%s-%s-' % (season, episode)
					# print ("ZEN URL TV SOURCES", pattern)
					r = BeautifulSoup(r)
					r =r.findAll('li')
					for items in r:
						try:
							ids = items['id'].encode('utf-8')
							href = items['data-click'].encode('utf-8')
							print ("ZEN URL TV SOURCES", ids, href)
							if pattern in ids:
									if "/api/plink" in href:
										player_items.append(href)
						except:
							pass

						
				for items in player_items:	
					
						api = items.split('res=')[0]
						print ("ZEN API ITEMS", api)
						res = ['1080','720', '360']
						for s in res:
							s = "res=%s" %s
							player = api + s
							player = urlparse.urljoin(self.base_link, player)
							
							try:
								url = OPEN_URL(player, output='geturl')
							# b = a.url
								# print ("ZEN FINAL REDIRECTED URL", url)
								
								quality = google_tag(url)
								# href = href.encode('utf-8')
								sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Vumoo', 'url': url, 'direct': True, 'debridonly': False})
							except:
								pass

					

			return sources
		except:
			return sources


	def resolve(self, url):
		return url

