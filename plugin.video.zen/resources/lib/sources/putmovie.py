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


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules.common import  random_agent
import requests
from BeautifulSoup import BeautifulSoup
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from schism_net import OPEN_URL

class source:
    def __init__(self):
        self.domains = ['http://putmv.com']
        self.base_link = 'http://putmv.com'
        self.search_link = '/search-movies/%s.html'


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            
            self.zen_url = []
            cleanmovie = cleantitle.get(title)
            title = cleantitle.getsearch(title)
			
            query = "%s+%s" % (urllib.quote_plus(title),year)
            query = self.search_link %query
            query = urlparse.urljoin(self.base_link, query)
            print ("PUTMOVIE query", query)
            html = OPEN_URL(query).content
            html = BeautifulSoup(html)
            r = html.findAll('div', attrs={'class': 'movie_pic'})
            
            for s in r:
                print ("PUTMOVIE RESULTS", s)
                t = s.findAll('img')[0]['alt'].encode('utf-8')
                h = s.findAll('a')[0]['href'].encode('utf-8')
                url = h
                if year in t and cleanmovie == cleantitle.get(t): return url
					
        except:
            return	


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            r = requests.get(url).text
            r = re.compile('<a target="_blank"  href="(.+?)" class="buttonlink" title="(.+?)"').findall(r)
            for h,t in r:
				quality = "SD"
				t = t.replace("Server ", "")
				sources.append({'source': t, 'quality': 'SD', 'provider': 'Putmovie', 'url': h, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):

            r = OPEN_URL(url, timeout='3').content
            r = BeautifulSoup(r)

            url = r.findAll('iframe')[0]['src'].encode('utf-8')
   
            return url



