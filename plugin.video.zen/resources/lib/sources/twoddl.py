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
        self.domains = ['2ddl.one']
        self.base_link = control.setting('twoddl_base')
        if self.base_link == '' or self.base_link == None:self.base_link = 'http://iiddl.com'

        self.search_link = '/search/%s+%s/feed/rss2/'
			
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
			posts = client.parseDOM(r, 'item')	
			items = []
			for post in posts:
				try:
					t = client.parseDOM(post, 'title')[0]
					t = t.encode('utf-8')
					if not cleanmovie in cleantitle.get(t) and year in t: continue
					c = client.parseDOM(post, 'content.+?')[0]
					u = client.parseDOM(c, 'p')
					u = [client.parseDOM(i, 'a', ret='href') for i in u]
					u = [i[0] for i in u if len(i) == 1]
					if not u: raise Exception()

					u = [(t, i) for i in u]

					self.zen_url += u
					# self.zen_url.append([links,t])
					
				except:
					pass
			# print ("SCENEDOWN PASSED", self.zen_url)		
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
			episodecheck = episodecheck.lower()
			query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			query = self.search_link % (urllib.quote_plus(title),query)
			query = urlparse.urljoin(self.base_link, query)
			print "%s TV QUERY %s" % (self.base_link, query)
			
			r = client.request(query)
			posts = client.parseDOM(r, 'item')	
			for post in posts:
				try:
					t = client.parseDOM(post, 'title')[0]
					t = t.encode('utf-8')
					if not cleanmovie in cleantitle.get(t) and episodecheck in t.lower(): continue
					c = client.parseDOM(post, 'content.+?')[0]
					u = client.parseDOM(c, 'p')
					u = [client.parseDOM(i, 'a', ret='href') for i in u]
					u = [i[0] for i in u if len(i) == 1]
					if not u: raise Exception()
					u = [(t, i) for i in u]
					self.zen_url += u

				except:
					pass
			print "%s TV QUERY PASSED %s" % (self.base_link, self.zen_url)
			return self.zen_url
        except:
            return			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for title,url in self.zen_url:
				quality = "SD"
				quality = quality_tag(title)
				if "1080p" in url.lower(): quality = "1080p"
				elif "720p" in url.lower(): quality = "HD"

				info = ''
				if "hevc" in title.lower(): info = "HEVC"					
				if any(value in url for value in hostprDict):
					try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
					except: host = 'Videomega'
					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')
					sources.append({'source': host, 'quality': quality, 'provider': 'twoDDL', 'url': url, 'info': info,'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url