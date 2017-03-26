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


import re,urllib,urlparse,hashlib,random,string,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

from schism_net import OPEN_URL

from BeautifulSoup import BeautifulSoup
class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yesmovies.to']
        self.base_link = 'http://solarmovie.lt'
        self.search_link = '/search-query/%s/'
        self.episode_link = '/ajax/v3_movie_get_episodes/%s/%s/%s/%s.html'
        self.playlist_link = '/wp-admin/admin-ajax.php?action=movie_load_embed&episode_id=%s'


    def movie(self, imdb, title, year):
	
        try:
            checktitle = cleantitle_get(title)
            print ("SOLARMOVIE", checktitle)	
            q = self.search_link % (urllib.quote_plus(cleantitle_query(title)))
            q = urlparse.urljoin(self.base_link, q)
            print ("SOLARMOVIE 2", q)	
            r = OPEN_URL(q).content
			
            r = BeautifulSoup(r)
            # print ("SOLARMOVIE 3", r)			
            r = r.findAll('div', attrs = {'class': 'ml-item'})
            for items in r:
                print ("SOLARMOVIE ITEMS", items)
                try:
					h = items.findAll('a')[0]['href'].encode('utf-8')
					t = items.findAll('a')[0]['title'].encode('utf-8')
					if cleantitle_get(t) == checktitle:
						info = items.findAll('a')[0]['data-url'].encode('utf-8')
						info =  urlparse.urljoin(self.base_link, info)
						y , q = self.movies_info(info, year)
						print ("SOLARMOVIE INFOS ", y)						
						if not y == year: raise Exception()
						self.quality = q
						return h
                except:
                    pass
        except:
            return


    # def tvshow(self, imdb, tvdb, tvshowtitle, year):
        # try:
            # url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            # url = urllib.urlencode(url)
            # return url
        # except:
            # return


    # def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        # try:
            # data = urlparse.parse_qs(url)
            # data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            # t = cleantitle.get(data['tvshowtitle'])
            # title = data['tvshowtitle']
            # season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            # year = re.findall('(\d{4})', premiered)[0]
            # years = [str(year), str(int(year)+1), str(int(year)-1)]

            # r = cache.get(self.ymovies_info_season, 720, title, season)
            # r = [(i[0], re.findall('(.+?)\s+(?:-|)\s+season\s+(\d+)$', i[1].lower())) for i in r]
            # r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            # r = [i[0] for i in r if t == cleantitle.get(i[1]) and season == '%01d' % int(i[2])][:2]
            # r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            # for i in r:
                # try:
                    # y, q = cache.get(self.ymovies_info, 9000, i[1])
                    # if not y == year: raise Exception()
                    # return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                # except:
                    # pass
        # except:
            # return


    # def ymovies_info_season(self, title, season):
        # try:
            # q = '%s Season %s' % (cleantitle.query(title), season)
            # q = '/search/%s.html' % (urllib.quote_plus(q))
            # q = urlparse.urljoin(self.base_link, q)

            # for i in range(3):
                # r = client.request(q)
                # if not r == None: break

            # r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            # r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            # r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]

            # return r
        # except:
            # return


    def movies_info(self, url, year):
        try:
            r = OPEN_URL(url).content

            q = client.parseDOM(r, 'div', attrs = {'class': 'jtip-quality'})[0]
            q = quality_tag(q)
            y = client.parseDOM(r, 'div', attrs = {'class': 'jt-info'})
            for items in y: 
				print ("SOLARMOVIES INFOs CHECK", year, y)
				if year in items: y = year
				
            if not y == year: y = '0'
            return (y, q)
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            # try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            # except: episode = None

            url = urlparse.urljoin(self.base_link, url)
            r = OPEN_URL(url).content
            vid_id = re.findall('movie-id="(.+?)"', r)[0]
            # print ("SOLARMOVIES SOURCES", vid_id) 
            '''
            quality = cache.get(self.ymovies_info, 9000, vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'
            '''
            html = re.findall('<a onclick=".+?" href="(.+?)" class="bwac-btn"', r)[0]
            s = self.playlist_link % vid_id
            s = urlparse.urljoin(self.base_link, s)
            s = OPEN_URL(s).content
            p = re.findall('"http(.+?)"', s)
            links = []
            for items in p:
				items = "http"+items
				items = items.replace("\\","")
				links.append(items)
				print ("SOLARMOVIES SOURCES LINKS", links)
            for u in links:
                try:
					if "player.123movies" in u:
						a = OPEN_URL(u).content
						# b = BeautifulSoup(a)
						# print ("SOLARMOVIES 123movies", a)

						c = re.findall('file:\s*"(.+?)",', a)
						for href in c:
							# print ("SOLARMOVIES 123movies", href)
							href = href.encode('utf-8')
							quality = google_tag(href)
							sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Solarmovie', 'url': href, 'direct': True, 'debridonly': False})
					else:
						try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(u.strip().lower()).netloc)[0]
						except: host = 'none'
						

						href = u.encode('utf-8')
						sources.append({'source': host, 'quality': "SD", 'provider': 'Solarmovie', 'url': href, 'direct': False, 'debridonly': False})
                                                
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url



def uncensored(a,b):
    x = '' ; i = 0
    for i, y in enumerate(a):
        z = b[i % len(b) - 1]
        y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
        x += chr(y)
    x = base64.b64encode(x)
    return x


