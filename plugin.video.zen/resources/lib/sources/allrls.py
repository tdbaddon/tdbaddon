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
from resources.lib.modules.common import  random_agent, quality_tag
from BeautifulSoup import BeautifulSoup
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['allrls.eu']
        self.base_link = 'http://allrls.eu'
        self.search_link = '/?s=%s+%s'
			
    def movie(self, imdb, title, year):
		self.zen_url = []
		try:
			if not debridstatus == 'true': raise Exception()			
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			print "%s QUERY %s" % (self.base_link, query)
			r = client.request(query)
			r = BeautifulSoup(r)
			r = r.findAll('h2', attrs = {'class': 'entry-title'})
			
			for item in r:
				try:
					t = item.findAll('a')[0].string
					t = t.encode('utf-8')
					h = item.findAll('a')[0]['href'].encode('utf-8')
					
					if cleanmovie in cleantitle_get(t) and year in t:

						self.zen_url.append([t,h])
					# self.zen_url.append([links,t])
					
				except:
					pass
				
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
			episodecheck = cleanmovie + episodecheck.lower()
			query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),query)
			query = urlparse.urljoin(self.base_link, query)

			r = client.request(query)
			r = BeautifulSoup(r)
			r = r.findAll('h2', attrs = {'class': 'entry-title'})
			
			for item in r:
				try:
					t = item.findAll('a')[0].string
					t = t.encode('utf-8')
					h = item.findAll('a')[0]['href'].encode('utf-8')
					
					if episodecheck in cleantitle_get(t):

						self.zen_url.append([t,h])
					# self.zen_url.append([links,t])
					
				except:
					pass
					
			return self.zen_url
        except:
            return			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for title,url in self.zen_url:
				quality = "SD"
				quality = quality_tag(title)
				if "1080p" in title.lower(): quality = "1080p"
				elif "720p" in title.lower(): quality = "HD"

				info = ''
				if "hevc" in title.lower(): info = "HEVC"	
				r = client.request(url)
				r = BeautifulSoup(r)
				r = r.findAll('div', attrs = {'class': 'entry-content'})
				for item in r:
					href = item.findAll('a')
					for u in href:
						url = u['href'].encode('utf-8')



				
						if any(value in url for value in hostprDict):
							try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
							except: host = 'Videomega'
							url = client.replaceHTMLCodes(url)
							url = url.encode('utf-8')
							sources.append({'source': host, 'quality': quality, 'provider': 'Allrls', 'url': url, 'info': info,'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url