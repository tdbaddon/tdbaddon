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

from schism_net import OPEN_URL, OPEN_CF, get_sources , get_files
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
	def __init__(self):
		self.base_link = 'http://watchonline.pro'
		self.search_link = '/advanced-search/?search_query=%s+%s&orderby=&order=&wpas=1'
		self.ep_link = '/episode/%s/'

	def movie(self, imdb, title, year):
		self.zen_url = []
		try:
			
			# print("WATCHCARTOON")
			title = cleantitle_query(title)
			cleanmovie = cleantitle_get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			
			r = OPEN_URL(query, timeout='15')
			
			html = BeautifulSoup(r.content)
			print ("WONLINE BeautifulSoup", html)
			r = html.findAll('div', attrs={'class': 'resultado'})
			print ("WONLINE s1",  r)
			for u in r:
				r_title = u.findAll('img')[0]['alt']
				r_title = r_title.encode('utf-8')
			
				r_href = u.findAll('a')[0]['href']
				r_title = r_title.encode('utf-8')
				
				
				print("WONLINE MATCHES", r_title,r_href)
				if year in r_title and cleanmovie == cleantitle_get(r_title): 
					if "http:" in r_href: url = replaceHTMLCodes(r_href)
					print("WONLINE PASSED", url)
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
			episodeid = "s%02de%02d" % (int(data['season']) , int(data['episode']))
			title = cleantitle_query(title)
			title = title.replace(' ','-')
			query = title + "-" + episodeid
			query= self.ep_link % query
			url = urlparse.urljoin(self.base_link, query)
			print("WONLINE TV SHOW", url)

			return url
		except:
			return
		
	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			
			if url == None: return
			try:
					
				link = OPEN_URL(url, timeout='10')
				html = BeautifulSoup(link.content)
					
				r = html.findAll('iframe')
				for u in r:
					src = u['src'].encode('utf-8')
					print("WONLINE sources", src)
					if src.startswith("//"): src = "http:" + src
						
					if "wp-embed.php" in src or "player.123movies" in src:
						try:
							s = OPEN_URL(src).content
							
							match = get_sources(s)
							for h in match:
								files = get_files(h)
								for href in files:
									href = href.replace('\\','')
									quality = google_tag(href)
									
									sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Wonline', 'url': href, 'direct': True, 'debridonly': False})
						except:
							pass
							
							
					elif "raptu.com" in src:
						try:
							s = OPEN_URL(src).content
							
							match = get_sources(s)
							for h in match:
								files = re.compile('"file":"(.+?)","label":"(.+?)",').findall(h)
								for href, q in files:
									href = href.replace('\\','')
									quality = quality_tag(q)
									
									sources.append({'source': 'gvideo', 'quality':quality, 'provider': 'Wonline', 'url': href, 'direct': True, 'debridonly': False})
						except:
							pass
							
					else:
							if "google" in src: quality = google_tag(src)
							else: quality = quality_tag(src)
							try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(src.strip().lower()).netloc)[0]
						
							except: host = 'none'
							url = replaceHTMLCodes(src)
							url = url.encode('utf-8')
							if host in hostDict: sources.append({'source': host, 'quality':quality, 'provider': 'Wonline', 'url': url, 'direct': False, 'debridonly': False})

			except:
				pass

			return sources
		except:
			return sources


	def resolve(self, url):

		return url

