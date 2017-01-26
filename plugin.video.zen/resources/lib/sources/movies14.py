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
from resources.lib.modules import directstream
class source:
    def __init__(self):
        self.domains = ['hdmovie14.net']
        self.base_link = 'http://hdmovie14.net'
        self.search_link = '/search?key=%s+%s'
        self.tvsearch_link = '/watch/%s-%s-season-%s'

    def movie(self, imdb, title, year):
        self.url = []	
        try:
					
			self.url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			# print ('MOVIES14 query',query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'thumbnail'})
			r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
			# print ('MOVIES14 r1',r)
			r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
			# print ('MOVIES14 r2',r)
			results = [i for i in r if cleanmovie in cleantitle.get(i[0]) and year in i[0]]
			for i in results:
				url = i[0]
				url = client.replaceHTMLCodes(url)
				# print ('MOVIES14 url',url)
				url = url.encode('utf-8')
				url = urlparse.urljoin(self.base_link, url)		
				url = client.request(url, output='geturl')
				return url
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
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            episode = '%01d' % (int(season))
            year = data['year']
            
            
            url = re.sub('[^A-Za-z0-9]', '-', data['tvshowtitle']).lower()
            url = self.tvsearch_link % (url, year, '%01d' % int(season))

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, output='geturl')
            url = r + "/" + episode
            # if not data['year'] in r: raise Exception()

            return url
        except:
            return
			
		
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = client.parseDOM(r, 'div', attrs = {'class': 'player_wraper'})
            r = client.parseDOM(r, 'iframe', ret='src')

            for u in r:
                try:
                    u = urlparse.urljoin(self.base_link, u)
                    u = client.request(u, referer=url)
                    u = re.findall('"(?:url|src)"\s*:\s*"(.+?)"', u)

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Movies14', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return
