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
class source:
    def __init__(self):
        self.domains = ['dailyreleases.net']
        self.base_link = 'http://dailyreleases.net'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()			
			self.zen_url = []
			# print ("DAILYRLS INIT")
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			# print ("DAILYRLS query", query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'id': 'post-.+?'})
			for item in r:
				href = client.parseDOM(item, 'a', ret = 'href')[0]
				item_title = client.parseDOM(item, 'a', ret = 'title')[0]
				href = href.encode('utf-8')
				item_title = item_title.encode('utf-8')
				# print ("DAILYRLS item", item_title,href)				
				if year in item_title:
					if cleanmovie in cleantitle.get(item_title):
						self.zen_url.append([href,item_title])
						# print "DAILYRLS MOVIES %s %s" % (item_title , href)
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
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			episodecheck = str(episodecheck).lower()
			query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),query)
			mylink = urlparse.urljoin(self.base_link, query)
			link = client.request(mylink)
			r = client.parseDOM(link, 'div', attrs = {'id': 'post-.+?'})
			for item in r:
				href = client.parseDOM(item, 'a', ret = 'href')[0]
				item_title = client.parseDOM(item, 'a', ret = 'title')[0]
				href = href.encode('utf-8')
				item_title = item_title.encode('utf-8')
				if cleanmovie in cleantitle.get(item_title):
					if episodecheck in cleantitle.get(item_title):
						item_title = item_title + "=episode"
						self.zen_url.append([href,item_title])
						# print "DAILYRLS TV SHOWS %s %s" % (item_title , href)
							
			return self.zen_url
        except:
            return			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.zen_url:
				mylink = client.request(movielink)
				match = re.compile('<a href="([^"]+)" rel="nofollow"').findall(mylink)
				for url in match:
					if "=episode" in title:
						if "1080" in url: quality = "1080p"
						elif "720" in url: quality = "HD"
						else: quality = "SD"
						info = ''
						if "hevc" in url.lower(): info = "HEVC"
					else:
						if "1080" in title: quality = "1080p"
						elif "720" in title: quality = "HD"
						else: quality = "SD"
						info = ''
						if "hevc" in title.lower(): info = "HEVC"					
					if not any(value in url for value in ['sample','uploadkadeh','wordpress','crazy4tv','imdb.com','youtube','userboard','kumpulbagi','mexashare','myvideolink.xyz', 'myvideolinks.xyz' , 'costaction', 'crazydl','.rar', '.RAR', 'ul.to', 'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up', 'adf.ly','.jpg','.jpeg']):
						if any(value in url for value in hostprDict):
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'Videomega'
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')
								sources.append({'source': host, 'quality': quality, 'provider': 'Dailyrls', 'url': url, 'info': info,'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url