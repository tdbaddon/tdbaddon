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
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['rlshd.net']
        self.base_link = 'rlshd.net'
        self.search_link = 'http://www.rlshd.net/?s='


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = "http://www.rlshd.net/?s=%s+%s" % (urllib.quote_plus(title),year)
			titlecheck = cleanmovie+year
			link = client.request(query, timeout="10")
			
			match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>').findall(link)
			for movielink,title in match:
				# print "RLSHD MOVIELINKS %s %s" % (movielink,title)
				c_title = cleantitle_get_2(title)
				
				if titlecheck in c_title:

							# print "RLSHD MOVIES PASSED %s %s" % (movielink,title)
							self.zen_url.append([movielink,c_title])
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
			titlecheck = cleanmovie+episodecheck
			query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(data['season']), int(data['episode']))
			movielink = self.search_link + query
			link = client.request(movielink, timeout="10")
			match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>').findall(link)
			for movielink,title2 in match:
				c_title = cleantitle.get(title2)
				if titlecheck in c_title:
					self.zen_url.append([movielink,title])
			return self.zen_url
        except:
            return
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []

			
			for movielink,title in self.zen_url:
				mylink = client.request(movielink, timeout="5")
				if "1080" in title: quality = "1080p"
				elif "720" in title: quality = "HD"				
				else: quality = "SD"
				# posts = client.parseDOM(mylink, 'p', attrs = {'class': 'sociallocker'})
				try:
					posts = re.compile('<p class="sociallocker"(.+?)</p>',re.DOTALL).findall(mylink)
					for item in posts:
						
						match = re.compile('href="([^"]+)').findall(item)
						for url in match:
							# print "RLSHD NEW URL PASSED %s" % url
							url = str(url)
							if not any(value in url for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
								if any(value in url for value in hostprDict):
									
																
									try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
									except: host = 'Videomega'
									url = client.replaceHTMLCodes(url)
									url = url.encode('utf-8')										
									sources.append({'source': host, 'quality': quality, 'provider': 'Rlshd', 'url': url, 'direct': False, 'debridonly': True})
				except:
					match = re.compile('<a href="(.+?)" target="_blank">').findall(mylink)

					for url in match:
							# print "RLSHD NEW URL PASSED %s" % url
							url = str(url)
							if not any(value in url for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
								if any(value in url for value in hostprDict):
									
																
									try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
									except: host = 'Videomega'
										
									sources.append({'source': host, 'quality': quality, 'provider': 'Rlshd', 'url': url, 'direct': False, 'debridonly': True})

												
					
					
			return sources
        except:
            return sources			
			

    def resolve(self, url):

            return url