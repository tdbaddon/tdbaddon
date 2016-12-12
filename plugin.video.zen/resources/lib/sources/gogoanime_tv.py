# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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
import requests
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag

class source:
    def __init__(self):
        self.domains = ['gogoanimemobile.com', 'gogoanimemobile.net', 'gogoanime.io']
        self.base_link = 'http://gogoanimemobile.net'
        self.fullbase_link = 'http://gogoanime.io'
        self.search_link = '/search.html?keyword=%s'
        self.episode_link = '/%s-episode-%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(tvshowtitle))
            q = urlparse.urljoin(self.base_link, query)
            r = BeautifulSoup(requests.get(q, headers=headers).content)
            r = r.findAll('div', attrs={'class': re.compile('last_episodes.+?')})
            for containers in r:
				# print ("GOGOANIME r1", containers)
				r_url = containers.findAll('a')[0]['href'].encode('utf-8')
				r_title = containers.findAll('a')[0]['title'].encode('utf-8')
				if cleantitle.get(r_title) == cleantitle.get(tvshowtitle):
					url = re.findall('(?://.+?|)(/.+)', r_url)[0]
					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')
					return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            num = base64.b64decode('aHR0cDovL3RoZXR2ZGIuY29tL2FwaS8xRDYyRjJGOTAwMzBDNDQ0L3Nlcmllcy8lcy9kZWZhdWx0LyUwMWQvJTAxZA==')
            num = num % (tvdb, int(season), int(episode))
            num = client.request(num)
            num = client.parseDOM(num, 'absolute_number')[0]
            url = [i for i in url.split('/') if not i == ''][-1]
            url = self.episode_link % (url, num)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': random_agent()}
            if url == None: return sources
            url = urlparse.urljoin(self.base_link, url)
            r = BeautifulSoup(requests.get(url, headers=headers).content)
            r = r.findAll('iframe')
            # print ("GOGOANIME s1",  r)
            for u in r:
                try:
                    u = u['src'].encode('utf-8')
                    # print ("GOGOANIME s2",  u)
                    if not  'vidstreaming' in u: raise Exception()
                    html = BeautifulSoup(requests.get(u, headers=headers).content)
                    r_src = html.findAll('source')
                    for src in r_src:
                        vid_url = src['src'].encode('utf-8')
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(vid_url)[0]['quality'], 'provider': 'Gogoanime', 'url': vid_url, 'direct': True, 'debridonly': False})
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



