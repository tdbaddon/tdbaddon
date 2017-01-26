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


class source:
    def __init__(self):
        self.domains = ['http://putmv.com']
        self.base_link = 'http://putmv.com'
        self.search_link = '/search/%s.html'


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            headers = {'User-Agent': random_agent()}	
            self.zen_url = []
            cleanmovie = cleantitle.get(title)
            title = cleantitle.getsearch(title)
			
            query = "%s+%s" % (urllib.quote_plus(title),year)
            query = self.search_link %query
            query = urlparse.urljoin(self.base_link, query)
            # print ("PUTMV query", query)
            html = requests.get(query, headers=headers, timeout=15).text
            
            containers = re.compile('<h5 class="movie-name"><a href="(.+?)">(.+?)</a></h5>').findall(html)
            for r_href,r_title in containers:
                if cleanmovie == cleantitle.get(r_title):
						if year in r_href:
							# print ("PUTMV PLAY URL", r_href)
							url = r_href
							return url
        except:
            return	


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            referer = url

            for i in range(3):
                u = requests.get(referer).text
                if not u == None: break


            links = []

            try:


                    headers = {'User-Agent': random_agent(), 'X-Requested-With': 'XMLHttpRequest', 'Referer': referer}

                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')

                    iframe = re.compile('<a data-film="(.+?)" data-name="(.+?)" data-server="(.+?)"').findall(u)
                    for p1, p2, p3 in iframe:
						try:
							post = {'ipplugins': '1', 'ip_film': p1, 'ip_name': p2 , 'ip_server': p3}
							# post = urllib.urlencode(post)
							# print ("PUTMV URL", post)

							for i in range(3):
								req = requests.post(url, data=post, headers=headers).content
							# print ("PUTMV req1", req)

							result = json.loads(req)
							token = result['s'].encode('utf-8')
							server = result['v'].encode('utf-8')
		  
							# print ("PUTMV server", token,server)
							
							url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')

							post = {'u': token, 'w': '100%', 'h': '500' , 's': server, 'n':'0'}
							req_player = requests.post(url, data=post, headers=headers).content
							# print ("PUTMV req_player", req_player)
							result = json.loads(req_player)['data']
							result = [i['files'] for i in result]

							for i in result:
								try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Putmovie', 'url': i, 'direct': True, 'debridonly': False})
								except: pass
						except:
							pass
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):

            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url



