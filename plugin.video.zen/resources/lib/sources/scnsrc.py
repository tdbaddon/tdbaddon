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
from resources.lib.modules.common import  random_agent
import requests
from BeautifulSoup import BeautifulSoup
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['scnsrc.me']
        self.base_link = 'http://www.scnsrc.me'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            if not debridstatus == 'true': raise Exception()			
            self.zen_url = []
           
            cleanmovie = cleantitle.get(title)
            title = cleantitle.getsearch(title)
            titlecheck = cleanmovie+year
			
            query = self.search_link % (urllib.quote_plus(title),year)
            query = urlparse.urljoin(self.base_link, query)
            query = query + "&x=0&y=0"
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
           
            result = html.findAll('div', attrs={'class': 'post'})

            for r in result:
				r_href = r.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
                # print ("MOVIEXK r2", r_href)
				r_title = r.findAll('a')[0]["title"]
                # print ("MOVIEXK r3", r_title)
				r_title = r_title.encode('utf-8')
				c_title = cleantitle_get_2(r_title)		
				if year in r_title:
					if titlecheck in c_title:
						self.zen_url.append([r_href,r_title])
						# print "SCNSRC MOVIES %s %s" % (r_title , r_href)
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
            if not debridstatus == 'true': raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			
            cleanmovie = cleantitle.get(title)
            title = cleantitle.getsearch(title)
            data['season'], data['episode'] = season, episode
			
            episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            episodecheck = str(episodecheck).lower()
            titlecheck = cleanmovie+episodecheck
            query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            query = self.search_link % (urllib.quote_plus(title),query)
            query = urlparse.urljoin(self.base_link, query)
            query = query + "&x=0&y=0"	
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
           
            result = html.findAll('div', attrs={'class': 'post'})

            for r in result:
				r_href = r.findAll('a')[0]["href"]
				r_href = r_href.encode('utf-8')
                # print ("MOVIEXK r2", r_href)
				r_title = r.findAll('a')[0]["title"]
                # print ("MOVIEXK r3", r_title)
				r_title = r_title.encode('utf-8')	
				c_title = cleantitle.get(r_title)				
				if titlecheck in c_title:
					self.zen_url.append([r_href,r_title])
            return self.zen_url
        except:
            return			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.zen_url:

				headers = {'User-Agent': random_agent()}
				html = BeautifulSoup(requests.get(movielink, headers=headers, timeout=15).content)
				result = html.findAll('div', attrs={'class': 'comm_content'})[:3]
				for r in result:
					r_href = r.findAll('a')
					for items in r_href:
						url = items['href'].encode('utf-8')
						if "1080" in url: quality = "1080p"
						elif "720" in url: quality = "HD"
						else: quality = "SD"
						info = ''
						if "hevc" in url.lower(): info = "HEVC"
						if not any(value in url for value in ['sample','uploadkadeh','wordpress','crazy4tv','imdb.com','youtube','userboard','kumpulbagi','mexashare','myvideolink.xyz', 'myvideolinks.xyz' , 'costaction', 'crazydl','.rar', '.RAR', 'ul.to', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up', 'adf.ly','.jpg','.jpeg']):
							if any(value in url for value in hostprDict):
									try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
									except: host = 'Videomega'
									url = client.replaceHTMLCodes(url)
									url = url.encode('utf-8')
									sources.append({'source': host, 'quality': quality, 'provider': 'Scnsrc', 'url': url, 'info': info,'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url