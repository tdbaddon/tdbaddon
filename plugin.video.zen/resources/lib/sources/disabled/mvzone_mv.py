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
        self.search_link = '/?s=%s+%s'

		
    def movie(self, imdb, title, year):
		self.zen_url = []	
		try:
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'boxinfo'})
			for links in r:
				url = client.parseDOM(links, 'a', ret='href')[0]
				info = client.parseDOM(links, 'span', attrs = {'class': 'tt'})[0]
				url = url.encode('utf-8')
				info = info.encode('utf-8')
				# print("MOVIEZONE LINKS", url,info)
				if year in info:
					if cleanmovie == cleantitle.get(info):
					 
						self.zen_url.append(url)
			# print("MOVIEZONE PASSED LINKS", self.zen_url)
			return self.zen_url
		except:
			return
			

    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink in self.zen_url:
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


							sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Mvzone', 'url': url, 'direct': True, 'debridonly': False})
					except:
						pass
			return sources
        except:
            return sources


    def resolve(self, url):
        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
        else: url = url.replace('https://', 'http://')
        return url
