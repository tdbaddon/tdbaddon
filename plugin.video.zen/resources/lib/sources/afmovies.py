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
import re,urllib,urlparse,hashlib,random,string,json,base64,requests
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag
rq = requests.session()
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from schism_net import OPEN_URL

class source:
    def __init__(self):
        self.domains = ['afdah.tv']
        self.base_link = 'http://afdah.tv'
        self.search_link = '/?s=%s'
        
		
		
    def movie(self, imdb, title, year):
		try:
			self.zen_url = []
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			headers = {'User-Agent': random_agent(), 'X-Requested-With':'XMLHttpRequest'}
			search_url = urlparse.urljoin(self.base_link, '/wp-content/themes/afdah/ajax-search.php')
			data = {'yreuq': title, 'meti': 'title'}

			moviesearch = requests.post(search_url, headers=headers, data=data)
			moviesearch = moviesearch.content
			match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(moviesearch)
			for href, movietitle in match:
				if year in movietitle and cleanmovie == cleantitle.get(movietitle):
					
					url = href.encode('utf-8')
					if not "http" in url: url = urlparse.urljoin(self.base_link, url)
					return url
		except:
			return
			
			
		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			
			headers = {'User-Agent': random_agent()}
			html = OPEN_URL(url)
			r = BeautifulSoup(html.content)
			r = r.findAll('tr')
			for items in r:
				href = items.findAll('a')[0]['href'].encode('utf-8')
				print ("AFMOVIE R2", href)
				try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
				except: host = 'Afmovies'
				if not host in hostDict: continue
				sources.append({'source': host, 'quality': 'SD', 'provider': 'Afmovies', 'url': href,  'direct': False, 'debridonly': False})

			return sources
        except:
            return sources


    def resolve(self, url):
		return url
		
		
 