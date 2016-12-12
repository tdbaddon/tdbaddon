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
        self.domains = ['mvgee.com']
        self.base_link = 'http://mvgee.com'
        self.search_link = '/search?q=%s+%s'
        self.api_link = 'http://mvgee.com/io/1.0/stream?imdbId=%s&season=%s&provider=%s&name=%s'
		



    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
				
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			checktitle = cleanmovie+year
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			
			link = client.request(query)
			result = json.loads(link)
			items = result['suggestions']
			for item in items:
				href = item['data']['href']
				value = item['value']
				url = href.encode('utf-8')
				value = value.encode('utf-8')
				if checktitle == cleantitle.get(value):
					if not self.base_link in url: url = urlparse.urljoin(self.base_link, url)
					print ("MVGEE PASSED", url)
					return url
					
        except:
            return
		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			if url == None: return sources
			link = client.request(url)
			data_id = re.compile('{"imdbId":"(.+?)","season":(\d+),"provider":"(.+?)","name":"(.+?)"}').findall(link)
			for imdbid,s_id,provider_id,name_id in data_id:
				print ("MVGEE SOURCES", imdbid,s_id,provider_id,name_id)
				api_link = self.api_link % (imdbid,s_id,provider_id,name_id)
				print ("MVGEE api_link", api_link)
				html = client.request(api_link)
				result = json.loads(html)
				response = result['streams']
				for items in response:
					href = items['src'].encode('utf-8')
					label = items['label'].encode('utf-8')
					if "720" in label: quality = "HD"
					elif "1080" in label: quality = "1080p"
					else: quality = "SD"
					# print ("MVGEE SOURCES", label, href)
					href = href.replace(" ","")
					sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Moviegee', 'url': href, 'direct': True, 'debridonly': False})
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