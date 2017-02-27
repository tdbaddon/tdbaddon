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
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['scnlog.eu']
        self.base_link = 'scnlog.eu'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			titlecheck = cleanmovie+year
			query = "http://scnlog.eu/movies/?s=%s+%s" % (urllib.quote_plus(title),year)
			link = client.request(query)
			posts = client.parseDOM(link, 'div', attrs = {'class': 'title'})
			for items in posts:
				match = re.compile('<a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a>').findall(items)
				for movielink,title in match:
					title = cleantitle_get_2(title)
					if titlecheck in title:
							
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
			titlecheck = cleanmovie+episodecheck
			query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(data['season']), int(data['episode']))
			movielink = "http://scnlog.eu/tv-shows/?s=" + str(query)
			link = client.request(movielink)
			match = re.compile('<a href="(.+?)" rel="bookmark" title="(.+?)">').findall(link)
			for movielink,title2 in match:
				title = cleantitle.get(title2)
				if titlecheck in title:
					self.zen_url.append([movielink,title])
			return self.zen_url
        except:
            return
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.zen_url:
				mylink = client.request(movielink)
				if "1080" in title: quality = "1080p"
				elif "720" in title: quality = "HD"				
				else: quality = "SD"	
				match = re.compile('<a href="(.+?)" class="external" rel="nofollow" target="_blank">').findall(mylink)
				for url in match:
					
					url = str(url)

					if not any(value in url for value in ['imagebam','imgserve','histat','crazy4tv','facebook','.rar', 'subscene','.jpg','.RAR',  'postimage', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up','imdb']):
						if any(value in url for value in hostprDict):
								
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')															
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Videomega'
									
								sources.append({'source': host, 'quality': quality, 'provider': 'Scnlog', 'url': url, 'direct': False, 'debridonly': True})

						
					
					
			return sources
        except:
            return sources			
			

    def resolve(self, url):

            return url