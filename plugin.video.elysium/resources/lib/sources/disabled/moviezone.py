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
import re,urllib,urlparse
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
class source:
    def __init__(self):
        self.domains = ['moviezone.ch']

        self.base_link = 'http://moviezone.ch'
        self.movie_link = '/%s/'
        self.ep_link = '/episode/%s/'
		
    def movie(self, imdb, title, year):
		self.elysium_url = []	
		try:
			self.elysium_url = []
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			query = self.movie_link % (title)
			query = urlparse.urljoin(self.base_link, query)
			self.elysium_url.append(query)
			# print("MOVIEZONE PASSED LINKS", self.elysium_url)
			return self.elysium_url
		except:
			return



    def tvshow(self, imdb, tvdb, tvshowtitle, year):
		self.elysium_url = []	
		try:
			url = {'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			# print("MOVIEZONE PASSED LINKS", self.elysium_url)
			return url
		except:
			return			

			
			
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		self.elysium_url = []	
		try:
			self.elysium_url = []
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			data['season'], data['episode'] = season, episode
			
			title = cleantitle.getsearch(title)
			title = title.replace(' ','-')
			query = title .lower() + "-season-" + season + "-episode-" + episode
			query= self.ep_link % query
			query = urlparse.urljoin(self.base_link, query)
			self.elysium_url.append(query)
			# print("MOVIEZONE PASSED LINKS", self.elysium_url)
			return self.elysium_url
		except:
			return


    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink in self.elysium_url:
				referer = movielink
				link = client.request(movielink)
				
				r = client.parseDOM(link, 'iframe', ret='src', attrs = {'class': 'movieframe'})
				for item in r:
					try:
						iframe = item.encode('utf-8')
						# print('MOVIEZONE IFRAMES',iframe)
						redirect = client.request(iframe, timeout='10')
						frame2 = client.parseDOM(redirect, 'iframe', ret='src')[0]
						frame2 = frame2.encode('utf-8')
						# print('MOVIEZONE IFRAMES2',frame2)
						finalurl = client.request(frame2, timeout='5')
						gv_frame = client.parseDOM(finalurl, 'source', ret='src')
						for items in gv_frame:
							url = items.encode('utf-8')
							url = client.replaceHTMLCodes(url)
							# print ('MOVIEZONE players', url)
							quality = directstream.googletag(url)[0]['quality']
							# print ('MOVIEZONE', quality, url)


							sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Moviezone', 'url': url, 'direct': True, 'debridonly': False})
					except:
						pass
			return sources
        except:
            return sources


    def resolve(self, url):
        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
        else: url = url.replace('https://', 'http://')
        return url
