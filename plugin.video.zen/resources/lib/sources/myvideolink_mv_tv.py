# -*- coding: utf-8 -*-

'''
    zen Add-on
    Copyright (C) 2016 zen

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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
# if not debridstatus == 'true': raise Exception() 

class source:
    def __init__(self):
        self.domains = ['myvideolink.xyz']
        self.base_link = 'newmyvideolink.xyz'
        self.search_link = 'http://newmyvideolink.xyz/?s='


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = "http://newmyvideolink.xyz/?s=%s+%s" % (urllib.quote_plus(title),year)
			link = client.request(query)
			match = re.compile('<h2><a href="(.*?)" title=".*?">(.*?)</a>').findall(link)
			for movielink,title in match:
				if year in title:
					title = cleantitle.get(title)
					if cleanmovie in title:
						self.zen_url.append([movielink,title])


	 

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
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)			
			episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(episodecheck)
			episodecheck = episodecheck.lower()
			query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(data['season']), int(data['episode']))
			movielink = self.search_link + str(query)
			link = client.request(movielink)
			match = re.compile('<h2><a href="(.*?)" title=".*?">(.*?)</a>').findall(link)
			for href, title2 in match:
				if episodecheck in title2.lower():
					title2 = cleantitle.get(title2)
					if cleanmovie in title2:
							self.zen_url.append([href,title2])
			# print ("MYVIDEOLINK", self.zen_url)
			return self.zen_url
        except:
            return	

    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []

			
			for movielink,title in self.zen_url:
				
				quality = "SD"
				if "1080" in title: quality = "1080p"
				elif "720" in title: quality = "HD"					
				
				mylink = client.request(movielink)

			
				for item in client.parseDOM(mylink, 'div', attrs = {'class': 'post_content'}):
					matchblock = re.compile('<h(.+?)</h(.+?)</ul>',re.DOTALL).findall(item)
					for title,links in matchblock:
						
						if "1080" in title: quality = "1080p"
						elif "720" in title: quality = "HD"				
 						
					
						match2 = re.compile('href="([^"]+)').findall(links)			
				
				# match2 = re.compile('<li><a href="(.+?)">').findall(mylink)


						for url in match2:
							if not any(value in url for value in ['imdb.com','youtube','userboard','kumpulbagi','mexashare','myvideolink.xyz', 'myvideolinks.xyz' , 'costaction', 'crazydl','.rar', '.RAR',  'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up', 'adf.ly','.jpg','.jpeg']):
								if any(value in url for value in hostprDict):
									try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
									except: host = 'Videomega'
									host = client.replaceHTMLCodes(host)
									host = host.encode('utf-8')							
									
									url = client.replaceHTMLCodes(url)
									url = url.encode('utf-8')									
									sources.append({'source': host, 'quality': quality, 'provider': 'Myvideolink', 'url': url, 'direct': False, 'debridonly': True})

	 

			return sources
        except:
            return sources


    def resolve(self, url):

            return url