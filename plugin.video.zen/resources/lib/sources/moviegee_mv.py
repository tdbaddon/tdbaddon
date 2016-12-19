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



import re,urllib,urlparse,random,json
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client, directstream

class source:
    def __init__(self):
        self.domains = ['mvgee.com']
        self.base_link = 'http://mvgee.com'
        self.search_link = '/search?q=%s+%s'
        self.api_link = 'http://mvgee.com/io/1.0/stream?imdbId=%s&season=%s&provider=%s&name=%s'
		



    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
				
			self.zen_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			checktitle = cleanmovie+year
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			
			link = client.request(query)
			result = json.loads(link)
			items = result['suggestions']
			for item in items:
				href = item['data']['href']
				value = item['value']
				url = href.encode('utf-8')
				value = value.encode('utf-8')
				if checktitle == cleantitle.get(value):
					if not self.base_link in url: url = urlparse.urljoin(self.base_link, url)
					print ("MVGEE PASSED", url)
					return url
					
        except:
            return
		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
            h = {'User-Agent': client.agent()}

            r = client.request(url, headers=h, output='extended')

            s = client.parseDOM(r[0], 'ul', attrs = {'class': 'episodes'})
            s = client.parseDOM(s, 'a', ret='data.+?')
            s = [client.replaceHTMLCodes(i).replace(':', '=').replace(',', '&').replace('"', '').strip('{').strip('}') for i in s]

            for u in s:
                try:
                    url = '/io/1.0/stream?%s' % u
                    url = urlparse.urljoin(self.base_link, url)

                    r = client.request(url)
                    r = json.loads(r)

                    url = [i['src'] for i in r['streams']]

                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Moviegee', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources



    def resolve(self, url):
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
