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



import re,urllib,urlparse,random,json
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import jsunpack
from resources.lib.modules import directstream

from schism_net import OPEN_URL
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes, get_size, get_host, get_video
from schism_titles import cleantitle_query , cleantitle_get, cleantitle_get_2, cleantitle_get_full, cleantitle_geturl, title_normalize
import requests
from BeautifulSoup import BeautifulSoup
class source:
    def __init__(self):
        self.domains = ['moviego.cc']
        self.base_link = 'http://moviego.cc'
        self.search_link = 'http://moviego.cc/engine/ajax/search.php'
        self.ep_url = '/engine/ajax/getlink.php?id=%s'
        # print("MOVIEGO started")
		
    def movie(self, imdb, title, year):

        try:
			headers = {'Accept':'*/*','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6', 'Referer':'http://moviego.cc/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'X-Requested-With':'XMLHttpRequest' }
			data = { 'query' : cleantitle_query(title) } 
			# print("MOVIEGO MOVIES")
			title = cleantitle_query(title)
			cleanmovie = cleantitle_get(title)
			# searchquery = self.search_link % (urllib.quote_plus(title),year)
			query = self.search_link
			# print("MOVIEGO Query", headers, data)
			link = requests.post(query, headers=headers, data=data)
			link = link.content
			r = re.compile('<a href="(.+?)"><span class="searchheading">(.+?)</span></a>').findall(link)
			for url, t in r:
				if year in t and cleanmovie == cleantitle_get(t):
					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')
					# print("MOVIEGO URL PASSED", url)
					return url
        except:
            return
			

		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			alt_links = []
			play_links = []
			link = client.request(url)
			film_quality = re.findall('<div class="poster-qulabel">(.*?)</div>',link)[0]
			if "1080" in film_quality: quality = "1080p"
			elif "720" in film_quality: quality = "HD"
			else: quality = "SD"
			# print ("MOVIEGO SOURCES", quality)
			r = BeautifulSoup(link)
			r = r.findAll('iframe')
			
			try:
				for u in r:
					iframe = u['src'].encode('utf-8')
					if '/play/' in iframe:
						# print ("MOVIEGO IFRAME", iframe)
						videourl = client.request(iframe)
						s = BeautifulSoup(videourl)
						s = s.findAll('script')
						unpacked_script = ""
						for scripts in s:
							try: unpacked_script += jsunpack.unpack(scripts.text)
							except:pass
							links = get_video(unpacked_script)
							for url in links:
								# print ("MOVIEGO pack", url)
								try:sources.append({'source': 'gvideo', 'quality': google_tag(url), 'provider': 'Moviego', 'url': url, 'direct': True, 'debridonly': False})
								except:pass
					else:
						try:
							
							host = get_host(iframe)
							if host in hostDict: sources.append({'source': host, 'quality': quality, 'provider': 'Moviego', 'url': iframe, 'direct': True, 'debridonly': False})
						except:
							pass

			except:
				pass

				

			
			return sources
        except:
            return sources


    def resolve(self, url):
            return url

			
			

	