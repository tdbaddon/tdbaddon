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
import re,urllib,urlparse,hashlib,random,string,json,base64
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
class source:
    def __init__(self):
        self.domains = ['watchoverhere.tv']
        self.base_link = 'http://oneclickmovies.tv'
        self.search_link = '/ajax/search.php?q=%s'		
		
    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = json.loads(link)
			for items in r:
				href = items['permalink'].encode('utf-8')
				infotitle = items['title'].encode('utf-8')
				if cleanmovie == cleantitle.get(infotitle):
					result = client.request(href)
					checkimdb = re.findall(r'IMDB\(\["([^"]+)"\]\)', result)[0]
					checkimdb = checkimdb.replace('"','')
					# print ("watchover REQUEST", href, infotitle, checkimdb)
					if checkimdb == imdb:
						iframe = re.findall('SRC="/play.php?([^"]+)', result)
						# print ("watchover IFRAME", iframe)
						for frames in iframe:
							# print ("watchover redirect", frames)
							redirect = re.findall('&url=(.+?)&domain=', frames)[0]
							redirect  = str(redirect)
							# print ("watchover redirect", redirect)
							vid_url = base64.b64decode(redirect)
							self.zen_url.append(vid_url)
							# print ("watchover PASSED", vid_url)
			return self.zen_url
        except:
            return
			
			
    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb':imdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return			

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []	
        try:
			headers = {}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			year = data['year'] 
			imdb = data['imdb']
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			season = '%01d' % int(data['season'])
			episode = '%01d' % int(data['episode'])
			ep_query = '/season/%s/episode/%s' % (season,episode)
			# print ("watchover ep_query", ep_query)
			query = self.search_link % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = json.loads(link)
			for items in r:
				href = items['permalink'].encode('utf-8')
				infotitle = items['title'].encode('utf-8')
				if cleanmovie == cleantitle.get(infotitle):
					result = client.request(href)
					checkimdb = re.findall(r'IMDB\(\["([^"]+)"\]\)', result)[0]
					checkimdb = checkimdb.replace('"','')
					# print ("watchover REQUEST", href, infotitle, checkimdb)
					if checkimdb == imdb:
						ep_page = href + ep_query
						ep_links = client.request(ep_page)
						iframe = re.findall('SRC="/play.php?([^"]+)', ep_links)
						# print ("watchover IFRAME", iframe)
						for frames in iframe:
							# print ("watchover redirect", frames)
							redirect = re.findall('&url=(.+?)&domain=', frames)[0]
							redirect  = str(redirect)
							# print ("watchover redirect", redirect)
							vid_url = base64.b64decode(redirect)
							self.zen_url.append(vid_url)
							# print ("watchover PASSED", vid_url)

			return self.zen_url
        except:
            return	
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for links in self.zen_url:
				# print ("YMOVIES SOURCES", movielink, cookies, referer)

					result = client.request(links)
					match = re.compile("file:\s*'(.*?)',.+?abel:\s*'(.*?)',", re.DOTALL).findall(result)
					for url,quality in match: 
						# print ("WATCHOVER SOURCES", url)
						if "1080" in quality: quality = "1080p"
						elif "720" in quality: quality = "HD"
						else: quality = "SD"
						url = client.replaceHTMLCodes(url)
						url = url.encode('utf-8')
						sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Watchover', 'url': url, 'direct': True, 'debridonly': False})
				
			return sources
        except:
            return sources


    def resolve(self, url):

        return url
	