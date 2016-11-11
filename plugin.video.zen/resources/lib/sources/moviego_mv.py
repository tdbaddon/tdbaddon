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

class source:
    def __init__(self):
        self.domains = ['moviego.cc']
        self.base_link = 'http://moviego.cc'
        self.search_link = '/index.php?do=search&subaction=search&full_search=1&result_from=1&story=%s+%s'
        self.ep_url = '/engine/ajax/getlink.php?id=%s'

    def movie(self, imdb, title, year):
        self.url = []	
        try:
					
			self.url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			searchquery = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, searchquery)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'short_overlay'})
			r = [(client.parseDOM(i, 'a', ret='href')) for i in r]
			r = [i for i in r if len(i) > 0]
			r = [i[0] for i in r if cleanmovie in cleantitle.get(i[0]) and year in i[0]][0]
			url = r
			url = client.replaceHTMLCodes(url)
			url = url.encode('utf-8')
			print("MOVIEGO URL r2", url)
			return url
        except:
            return
			

		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			link = client.request(url)
			re.findall('-(\d+)', url)[-1]
			film_id = re.findall("\/(\d+)-",link)[0]
			film_quality = re.findall('<div class="poster-qulabel">(.*?)</div>',link)[0]
			if film_id:
				film_id = film_id.encode('utf-8')
				try: film_quality = film_quality.encode('utf-8')
				except: pass
				print ("MOVIEGO RESULTS", film_id,film_quality)
				ep_query = self.ep_url % film_id
				query = urlparse.urljoin(self.base_link, ep_query)
				link = client.request(query)
				results = json.loads(link)
				url = results['file']
				print ("MOVIEGO 3r", url)
				if "1080" in film_quality: quality = "1080p"
				elif "720" in film_quality: quality = "HD"
				else: quality = "SD"
				url = client.replaceHTMLCodes(url)
				url = url.encode('utf-8')
					
				sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Moviego', 'url': url, 'direct': True, 'debridonly': False})
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