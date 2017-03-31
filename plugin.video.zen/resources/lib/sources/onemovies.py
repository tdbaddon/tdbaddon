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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
import requests
from BeautifulSoup import BeautifulSoup
from resources.lib.modules import control

from schism_meta import meta_info , meta_quality, meta_gvideo_quality, meta_host
from schism_net import OPEN_URL, random_agent, get_sources, get_files
from schism_commons import parseDOM, replaceHTMLCodes
from schism_titles import title_match, cleantitle_get, cleantitle_get_2, cleantitle_get_full, cleantitle_geturl, cleantitle_get_simple, cleantitle_query, cleantitle_normalize

class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru', '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru', '123movies.unblckd.me']

        self.base_link = 'https://123movieshd.tv'


        self.search_link = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'
        self.session = requests.Session()

    def movie(self, imdb, title, year):
        try:
            self.zen_url = []


            cleaned_title = cleantitle_get(title)
            title = cleantitle_query(title)
                      
            q = self.search_link % (cleantitle_geturl(title))
            r = urlparse.urljoin(self.base_link, q)
            print ("ONEMOVIES EPISODES", r)
            html = BeautifulSoup(OPEN_URL(r).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
                links = result.findAll('a')
                for link in links:
                    link_title = link['title'].encode('utf-8')
                    href = link['href'].encode('utf-8')
                    href = urlparse.urljoin(self.base_link, href)
                    href = re.sub('/watching.html','', href)
                    href = href + '/watching.html'

                    print("ONEMOVIES", link_title, href)
                    if title_match(cleantitle_get(link_title), cleaned_title) == True:
                        
                        html = OPEN_URL(href).content
                        
                        match = re.findall('<strong>Release:</strong>(.+?)</p>', html)[0]
                        if year in match:
							
							s = BeautifulSoup(html)
							
							s = s.findAll('div', attrs={'class': 'les-content'})
							for u in s:
								print("ONEMOVIES PASSED u", u)
								player = u.findAll('a')[0]['player-data'].encode('utf-8')
								
								if not player in self.zen_url:	self.zen_url.append(player)
							

							return self.zen_url
        except:
            return



    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            print ("ONEMOVIES EPISODES STARTED")
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.zen_url = []
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = cleantitle.getsearch(data['tvshowtitle'])
            print ("ONEMOVIES EPISODES STARTED")
            season = '%01d' % int(season)
            episode = '%01d' % int(episode)
            query = cleantitle_geturl(title) + "-season-" + season
            q = self.search_link % (query)
            r = urlparse.urljoin(self.base_link, q)
            cleaned_title = cleantitle_get(title) + "season" + season
            print ("ONEMOVIES EPISODES", q)
            html = BeautifulSoup(OPEN_URL(r).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
                links = result.findAll('a')
                for link in links:
                    link_title = link['title'].encode('utf-8')
                    href = link['href'].encode('utf-8')
                    href = urlparse.urljoin(self.base_link, href)
                    href = re.sub('/watching.html','', href)
                    href = href + '/watching.html'

                    # print("ONEMOVIES", link_title, href)
                    if title_match(cleantitle_get(link_title), cleaned_title) == True:
						print("ONEMOVIES FOUND MATCH", link_title, href)
						html = OPEN_URL(href).content
   						s = BeautifulSoup(html)
							
						s = s.findAll('div', attrs={'class': 'les-content'})
						for u in s:
							print("ONEMOVIES PASSED u", u)
							player = u.findAll('a')[0]['player-data'].encode('utf-8')
							ep_id = u.findAll('a')[0]['episode-data'].encode('utf-8')
							if not ep_id == episode: raise Exception()
								
							if not player in self.zen_url:	self.zen_url.append(player)
							

						return self.zen_url

        except:
            return




    def sources(self, url, hostDict, hostprDict):

        sources = []
        try:
            

            for url in self.zen_url:
				print ("ONEMOVIES SOURCES", url)
				if "embed.123movieshd" in url:
					try:
						r = OPEN_URL(url).content
						r = get_sources(r)
						for u in r:
							h = get_files(u)
							for s in h:
								href = s.encode('utf-8')
								quality = meta_gvideo_quality(href)
								print ("ONEMOVIES SOURCES 2", href)
								sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'onemovies', 'url': href, 'direct': True, 'debridonly': False})
					except:
						pass
				elif "embed2.seriesonline.io" in url:
					try:
						r = OPEN_URL(url).content
						r = BeautifulSoup(r)
						r = r.findAll('source')
						for u in r:
							href = u['src'].encode('utf-8')
							quality = meta_gvideo_quality(href)
							print ("ONEMOVIES SOURCES 2", href)
							sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'onemovies', 'url': href, 'direct': True, 'debridonly': False})
					except:
						pass
						
				else:
					try:
						href = url.encode('utf-8')
						host = meta_host(url)
						quality = "SD"
						if not host in hostDict: raise Exception()
						sources.append({'source': host, 'quality': quality, 'provider': 'onemovies', 'url': href, 'direct': False, 'debridonly': False})
					except:
						pass
				

        except:
            pass
        return sources


    def resolve(self, url):
            return url