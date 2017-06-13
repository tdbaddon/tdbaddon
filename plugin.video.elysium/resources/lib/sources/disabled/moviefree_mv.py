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
from resources.lib.modules import client
from resources.lib.modules import directstream
class source:
    def __init__(self):
        self.domains = ['hdmoviefree.org']

        self.base_link = 'http://www.hdmoviefree.org'
        self.search_link = '/search/%s.html'
        self.server_link = '/ajax/loadsv/%s'
        self.episode_link = '/ajax/loadep/%s'

    def movie(self, imdb, title, year):
        try:
					
			self.elysium_url = []
			cleanmovie = cleantitle.get(title)
			query = urlparse.urljoin(self.base_link, self.search_link % title.replace(' ', '-').replace('.', '-'))
			# print("HDMFREE r1", query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': '[^"]*slideposter[^"]*'})
			r = [(client.parseDOM(i, 'a', ret='href'),client.parseDOM(i, 'img', ret='alt')) for i in r]
			r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
			r = [i[0] for i in r if cleanmovie in cleantitle.get(i[1]) and year in i[1]][0]
			url = r
			url = client.replaceHTMLCodes(url)
			url = "http://www.hdmoviefree.org/" + url
			url = url.encode('utf-8')
			
			return url
        except:
            return
			
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
			# print ("HDMFREE INITIALIZED", url)
            if url == None: return sources

           

            r = client.request(url)

            data_id = client.parseDOM(r, 'img', ret='data-id')[0]
            data_name = client.parseDOM(r, 'img', ret='data-name')[0]

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

            post = {'id': data_id, 'n': data_name}
            post = urllib.urlencode(post)

            url = self.server_link % data_id
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, post=post, headers=headers)

            links = client.parseDOM(r, 'a', ret='data-id')

            for link in links:
                try:
                    url = self.episode_link % link
                    url = urlparse.urljoin(self.base_link, url)

                    post = {'epid': link}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, headers=headers)
                    r = json.loads(r)
                    try: u = client.parseDOM(r['link']['embed'], 'iframe', ret='src')
                    except: u = r['link']['l']

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Moviefree', 'url': i, 'direct': True, 'debridonly': False})
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