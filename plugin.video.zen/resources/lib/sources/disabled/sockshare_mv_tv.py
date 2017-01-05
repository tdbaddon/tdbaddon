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
        self.domains = ['sockshare.biz']
        self.base_link = 'http://sockshare.biz'
        self.search_link = '/search/%s.html'
        self.episodes_link = "http://sockshare.biz/watch/"

# http://sockshare.biz/watch/supergirl-s02-2015-online.html?p=7&s=11
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
           
            html = requests.get(query, headers=headers, timeout=15).content
            
            containers = re.compile('<span class="year">(.+?)</span><a class="play" href="(.+?)" title="(.+?)">').findall(html)
            for r_year, r_href, r_title in containers:
                if cleanmovie == cleantitle.get(r_title):
						if r_year == year:
							
							url = r_href
            return url
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
        
        try:
            headers = {'User-Agent': random_agent()}	
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            data['season'], data['episode'] = season, episode
            year = data['year']
            cleanmovie = cleantitle.get(title)
            title = cleantitle.getsearch(title)
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            seasoncheck = "s%02d" % int(season)
            html = requests.get(query, headers=headers, timeout=15).content
            containers = re.compile('<span class="year">(.+?)</span><a class="play" href="(.+?)" title="(.+?)">').findall(html)
            for r_year, r_href, r_title in containers:
                if cleanmovie in cleantitle.get(r_title):
					if seasoncheck in cleantitle.get(r_title):
						if year == r_year:
							url = r_href.encode('utf-8') + "?p=" + episode + "&s=11"
							print ("SOCKSHARE PASSED EPISODE", url)
							return url			
        except:
            pass
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            referer = url
            headers = {'User-Agent': random_agent(), 'X-Requested-With': 'XMLHttpRequest', 'Referer': referer}
            url_plugin = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')
            html = BeautifulSoup(requests.get(referer, headers=headers, timeout=15).content)
            # print ("SOCKSHARE NEW SOURCES", html)
            r = html.findAll('div', attrs={'class': 'new_player'})
            for container in r:
				block = container.findAll('a')
				for items in block:
					p1 = items['data-film'].encode('utf-8')
					p2 = items['data-name'].encode('utf-8')
					p3 = items['data-server'].encode('utf-8')
					post = {'ipplugins': '1', 'ip_film': p1, 'ip_name': p2 , 'ip_server': p3}
					req = requests.post(url_plugin, data=post, headers=headers).json()
					token = req['s'].encode('utf-8')
					server = req['v'].encode('utf-8')
					url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')
					post = {'u': token, 'w': '100%', 'h': '360' , 's': server, 'n':'0'}
					req_player = requests.post(url, data=post, headers=headers).json()
					# print ("SOCKSHARE SOURCES", req_player)
					result = req_player['data']
					result = [i['files'] for i in result]
					for i in result:
						try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Sockshare', 'url': i, 'direct': True, 'debridonly': False})
						except: pass


            return sources
        except:
            return sources


    def resolve(self, url):

            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url



