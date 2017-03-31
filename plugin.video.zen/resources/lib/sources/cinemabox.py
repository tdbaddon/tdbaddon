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

from BeautifulSoup import BeautifulSoup

from schism_titles import title_match, cleantitle_get, cleantitle_get_2, cleantitle_get_full, cleantitle_geturl, cleantitle_get_simple, cleantitle_query, cleantitle_normalize
from schism_meta import meta_info , meta_quality, meta_gvideo_quality, meta_host
from schism_net import OPEN_URL, random_agent, get_sources, get_files
from schism_commons import parseDOM, replaceHTMLCodes


class source:
    def __init__(self):
        self.domains = ['playboxhd.net']
        self.base_link = 'http://playboxhd.com'
        self.search_link = '/api/box?type=search&os=Android&v=291.0&k=0&keyword=%s'
        self.sources_link = '/api/box?type=detail&id=%s&os=Android&v=291.0&k=0&al=key'
        self.stream_link =	'/api/box?type=stream&id=%s&os=Android&v=291.0'		
			
			
			
    def movie(self, imdb, title, year):
		self.zen_url = []
		try:
				
			title = cleantitle_query(title)
			cleanmovie = cleantitle_get(title)
			query = self.search_link % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			print ("CINEMABOX query", query)
			r = OPEN_URL(query, mobile=True, timeout=30).json()
			print ("CINEMABOX ITEMS", r)
			html = r['data']['films']
			for item in html:
				print ("CINEMABOX ITEMS 3", item)			
				t = item['title'].encode('utf-8')
				h = re.findall('''['"]id['"]\s*:\s*(\d+)''', str(item))[0]
				print ("CINEMABOX ITEMS 4", t,h)
				if title_match(cleanmovie,cleantitle_get(t),  amount=1.0) == True:
					if year in item['publishDate']:
						s = self.sources_link % h
						s = urlparse.urljoin(self.base_link, s)
						print ("CINEMABOX ITEMS PASSED 5", t,h,s)
						s = OPEN_URL(s, mobile=True).json()
						s= s['data']['chapters']
						if len(s)> 0:
							for src in s:            
								name= src['title'].encode('utf8')
								if title_match(cleanmovie,cleantitle_get(name),  amount=1.0) == True:
									id = re.findall('''['"]id['"]\s*:\s*(\d+)''', str(src))[0]

								
						stream = self.stream_link % id
						stream = urlparse.urljoin(self.base_link, stream)
						self.zen_url.append(stream)

								
									
						print (">>>>>>>>> Cinemabox FOUND LINK", stream)

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
			
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = cleantitle_query(title)
			cleanmovie = cleantitle_get(title)

			data['season'], data['episode'] = season, episode
			season = "S%02d" % int(data['season'])
			episode = "%02d" % int(data['episode'])
			episode = "E0" + episode
			episodecheck = season + episode
			print ("CINEMABOX episodecheck", episodecheck)		

			query = self.search_link % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			
			
			print ("CINEMABOX query", query)
			r = OPEN_URL(query, mobile=True, timeout=30).json()

			html = r['data']['films']
			for item in html:
				# print ("CINEMABOX ITEMS 3", item)			
				t = item['title'].encode('utf-8')
				h = re.findall('''['"]id['"]\s*:\s*(\d+)''', str(item))[0]

				if title_match(cleanmovie,cleantitle_get(t),  amount=1.0) == True:
						
						s = self.sources_link % h
						s = urlparse.urljoin(self.base_link, s)
						print ("CINEMABOX PASSED 4", t,h,s)
						s = OPEN_URL(s, mobile=True).json()
						s= s['data']['chapters']
						if len(s)> 0:
							for src in s:            
								name = src['title'].encode('utf8')
								
								if episodecheck.lower() == name.lower():
									
									
									id = re.findall('''['"]id['"]\s*:\s*(\d+)''', str(src))[0]
									print ("CINEMABOX PASSED 6", name.lower())


									
								
						stream = self.stream_link % id
						stream = urlparse.urljoin(self.base_link, stream)
						self.zen_url.append(stream)

								
									
						print (">>>>>>>>> Cinemabox FOUND LINK", stream)

			return self.zen_url

        except:
			return	
	
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			dupes = []
			sources = []
			for url in self.zen_url:
				r = OPEN_URL(url, mobile=True).json()
				r = r['data']
				for item in r:
					name = item['server'].encode('utf8')
					quality = item['quality']
					if "auto" in quality.lower(): quality = 'HD'
					quality = meta_quality(quality)
					stream = item['stream'].encode('utf-8')
					url = self._decrypt(stream)

					
					if not url in dupes:
						print (">>>>>>>>>>>> CINEMABOX SRC", url)
						dupes.append(url)
						if "openload" in url: sources.append({'source': 'openload', 'quality': quality, 'provider': 'Cinemabox', 'url': url, 'direct': False, 'debridonly': False})
						elif "google" in url: sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Cinemabox', 'url': url, 'direct': True, 'debridonly': False})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url
			
    def _decrypt(self,url):
        from resources.lib.modules import pyaes as pyaes
        import base64
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(base64.urlsafe_b64decode('cXdlcnR5dWlvcGFzZGZnaGprbHp4YzEyMzQ1Njc4OTA='), '\0' * 16))
        url = base64.decodestring(url)
        url = decrypter.feed(url) + decrypter.feed()
        return url			