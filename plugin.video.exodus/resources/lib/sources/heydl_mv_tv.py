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


import re,urllib,urlparse,random

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['dl2.heydl.com']
        self.base_link = 'http://dl2.heydl.com'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, year):
        self.super_url = []	
        try:
			self.super_url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.base_link + "/film/"
			link = client.request(query)
			r = client.parseDOM(link, 'a', ret = 'href')
			for items in r:
				try:
					items = items.encode('utf-8')
					items_full = query + items
					# print ("HEYDL ITEMS", items_full)
					pages = client.request(items_full)
					file_links = client.parseDOM(pages, 'a', ret = 'href')
					for movie_links in file_links:
						movie_links = movie_links.encode('utf-8')
						# print ("HEYDL LINKS", movie_links)
						if year in movie_links:
							if cleanmovie in cleantitle.get(movie_links):
								movielink = items_full + movie_links
								self.super_url.append([movielink,movielink])
				except:
					pass

			# print ("HEYDL PASSED ITEMS", self.super_url)
			return self.super_url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.super_url = []	
        try:
            self.super_url = []
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year'] 
           
            cleanmovie = cleantitle.get(title)
            title = title.replace(' ','.')
			
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
            checkepisode = "s" + season + "e" + episode
            query = "/serial/%s/S%s/720p/" %(title, season)
            # print("HEYDL EPISODES", query)
            query = self.base_link + query
            link = client.request(query)
            r = client.parseDOM(link, 'a', ret = 'href')
            for items in r:
				try:
					items = items.encode('utf-8')
					if checkepisode in cleantitle.get(items):
						movielink = query + items
						title = items
						self.super_url.append([movielink,title])

				except:
					pass
						
            # print("HEYDL passed EPISODES", items)
            return self.super_url
        except:
            return			
			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []


			for movielink,title in url:

						if "1080" in title: quality = "1080p"
						elif "720" in title: quality = "HD"				
						else: title = "SD"
						info = ''
						if "3d" in title.lower(): info = "3D"
						if "hevc" in title.lower(): info = "HEVC"
						url = movielink

						url = client.replaceHTMLCodes(url)
						url = url.encode('utf-8')
						sources.append({'source': 'cdn', 'quality': quality, 'provider': 'Heydl', 'url': url, 'info': info,'direct': False, 'debridonly': False})

			sources = [i for i in sources if i['url'].split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower() in ['avi','mkv','mov','mp4','xvid','divx']]

			return sources
        except:
            return sources


    def resolve(self, url):
        try:
            content = client.request(url, output='headers')['Content-Type']
            if not 'html' in content: return url
        except:
            return


