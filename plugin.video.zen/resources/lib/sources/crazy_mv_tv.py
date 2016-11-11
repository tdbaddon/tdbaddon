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
import re,urllib,urlparse,base64
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
debridstatus = control.setting('debridsources')
# if not debridstatus == 'true': raise Exception()
class source:
    def __init__(self):
        self.domains = ['crazy4tv.com']
        self.base_link = 'http://crazy4tv.com'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			# print("CRAZY4AD query", query)
			link = client.request(query)
			r = client.parseDOM(link, 'h1', attrs = {'class': 'entry-title'})
			for items in r:
				href = client.parseDOM(items, 'a', ret = 'href')[0]
				item_title = client.parseDOM(items, 'a', ret = 'title')[0]
				href = href.encode('utf-8')
				item_title = item_title.encode('utf-8')
				# print("CRAZY4AD LINKS", href,item_title)
				if year in item_title:
					if cleanmovie in cleantitle.get(item_title):
						# print("CRAZY4AD LINKS PASSED", href,item_title)
						self.zen_url.append(href)
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
			year = data['year'] 
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			ep_query = "S%02dE%02d" % (int(data['season']),int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),ep_query )
			query = urlparse.urljoin(self.base_link, query)
			# print("CRAZY4AD query", query)
			link = client.request(query)
			r = client.parseDOM(link, 'h1', attrs = {'class': 'entry-title'})
			for items in r:
				href = client.parseDOM(items, 'a', ret = 'href')[0]
				item_title = client.parseDOM(items, 'a', ret = 'title')[0]
				href = href.encode('utf-8')
				item_title = item_title.encode('utf-8')
				# print("CRAZY4AD LINKS", href,item_title)
				if ep_query.lower() in cleantitle.get(item_title):
					if cleanmovie in cleantitle.get(item_title):
						# print("CRAZY4AD LINKS PASSED", href,item_title)
						self.zen_url.append(href)
			return self.zen_url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			
			for movielink in self.zen_url:
				mylink = client.request(movielink)
				r = client.parseDOM(mylink, 'div', attrs = {'class': 'entry-content'})
				for links in r:
					try:
						match = re.compile('href="([^"]+)[^>]+>([^<]+)').findall(links)
						for url,title in match:
							url = client.replaceHTMLCodes(url)
							url = url.encode('utf-8')	
							title = title.encode('utf-8')							
							if "1080" in title: quality = "1080p"
							elif "720" in title: quality = "HD"				
							else: quality = "SD"
							info = ''
							if "hevc" in title.lower(): info = "HEVC"
							if "3d" in title.lower(): info = "3D"
							# print ("CRAZY4AD FOUND LINKS", url,title)
							if not any(value in title for value in ['uploadkadeh','wordpress','crazy4tv','imdb.com','youtube','userboard','kumpulbagi','mexashare','myvideolink.xyz', 'myvideolinks.xyz' , 'costaction', 'crazydl','.rar', '.RAR',  'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up', 'adf.ly','.jpg','.jpeg']):
								if not any(value in url for value in ['uploadkadeh','wordpress','crazy4tv','imdb.com','youtube','userboard','kumpulbagi','mexashare','myvideolink.xyz', 'myvideolinks.xyz' , 'costaction', 'crazydl','.rar', '.RAR',  'safelinking','linx.2ddl.ag','upload.so','.zip', 'go4up', 'adf.ly','.jpg','.jpeg']):
									try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
									except: host = 'Rapidgator'
									if "sh.st" in url: host = 'SHST'
									url = client.replaceHTMLCodes(url)
									url = url.encode('utf-8')
									sources.append({'source': host, 'quality': quality, 'provider': 'Crazy', 'url': url, 'info': info,'direct': False, 'debridonly': True})
					except:
						pass
			return sources
        except:
            return sources


    def resolve(self, url):

        return url

