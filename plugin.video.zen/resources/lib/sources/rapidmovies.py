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
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
from schism_net import OPEN_URL
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from BeautifulSoup import BeautifulSoup

class source:
    def __init__(self):
        self.domains = ['http://rmz.cr']
        self.base_link = 'http://rmz.cr'
        self.movie_link = '/search/%s+%s/all/exact/m'
        self.shows_link = '/search/%s+%s/all/exact/s'
        self.count = 0
		
		


    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
			if not debridstatus == 'true': raise Exception()
			self.zen_url = []
			cleanmovie = cleantitle_get(title)
			title = cleantitle_query(title)
			titlecheck = cleanmovie+year
			query = self.movie_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			link = OPEN_URL(query).text
			match = re.compile('<a class="title" href="(.+?)">(.+?)</a>').findall(link)
			for h,t in match:
				print ("RAPIDMOVIES", h,t)
				h = h.encode('utf-8')
				t = t.encode('utf-8')
				check = cleantitle_get_2(t)
				print ("RAPIDMOVIES check", check)
				if h.startswith("/"): h = self.base_link + h
				if year in t:
					if titlecheck in check:
						info = get_size(t)
						quality = quality_tag(t)
						if "1080" in quality or "HD" in quality:
							self.count += 1
							if not self.count >6:
								print ("RAPIDMOVIES PASSED", t,quality,info)
								self.zen_url.append([h,quality,info])
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

			query = self.shows_link % (urllib.quote_plus(title),episodecheck)
			query = urlparse.urljoin(self.base_link, query)
			link = OPEN_URL(query).text
			match = re.compile('<a class="title" href="(.+?)">(.+?)</a>').findall(link)
			for h,t in match:
				print ("RAPIDMOVIES", h,t)
				h = h.encode('utf-8')
				t = t.encode('utf-8')
				check = cleantitle_get_2(t)
				print ("RAPIDMOVIES check", check)
				if h.startswith("/"): h = self.base_link + h
				if titlecheck in check:
						info = get_size(t)
						quality = quality_tag(t)
						if "1080" in quality or "HD" in quality:
							self.count += 1
							if not self.count > 6:
								print ("RAPIDMOVIES PASSED", t,quality,info)
								self.zen_url.append([h,quality,info])
			return self.zen_url
        except:
            return

			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for link,quality,info in self.zen_url:
				html = OPEN_URL(link)
				r = BeautifulSoup(html.content)
				r = r.findAll('pre', attrs={'class': 'links'})
				for u in r:
					url = u.string
					if any(value in url for value in hostprDict):
							
								try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
								except: host = 'noe'
								host = client.replaceHTMLCodes(host)
								host = host.encode('utf-8')							
								url = client.replaceHTMLCodes(url)
								url = url.encode('utf-8')								
								sources.append({'source': host, 'quality': quality, 'provider': 'Rapidmovies', 'url': url, 'info': info, 'direct': False, 'debridonly': True})

			return sources
        except:
            return sources


    def resolve(self, url):
            return url