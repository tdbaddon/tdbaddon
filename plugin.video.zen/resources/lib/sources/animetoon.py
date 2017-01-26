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
        self.domains = ['www.animetoon.org']
        self.base_link = 'http://www.animetoon.org'
        self.search_link = '/toon/search?key=%s'
        self.episode_link = '/%s-episode-%s'
		
    def movie(self, imdb, title, year):
        try:
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title))
            q = urlparse.urljoin(self.base_link, query)
            r = BeautifulSoup(requests.get(q, headers=headers).content)
            r = r.findAll('div', attrs={'class': 'right_col'})
            for containers in r:
				r_block = containers.findAll('a')[0]
				r_title = r_block.text
				r_title = r_title.encode('utf-8')
				r_href = r_block['href'].encode('utf-8')
				if cleantitle.get(title) == cleantitle.get(r_title):
					# print("ANIMETOON FOUND", r_title)
					r2 = BeautifulSoup(requests.get(r_href, headers=headers).content)
					r2 = r2.findAll('div', attrs={'id': 'videos'})
					for containers in r2:
						r_video = containers.findAll('a')[0]['href']
						url = r_video.encode('utf-8')
						# print("ANIMETOON PASSED", url)
						return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(tvshowtitle))
            q = urlparse.urljoin(self.base_link, query)
            r = BeautifulSoup(requests.get(q, headers=headers).content)
            r = r.findAll('div', attrs={'class': 'right_col'})
            for containers in r:
				r_block = containers.findAll('a')[0]
				r_title = r_block.text
				r_title = r_title.encode('utf-8')
				r_href = r_block['href'].encode('utf-8')
				if cleantitle.get(tvshowtitle) == cleantitle.get(r_title):
					# print("ANIMETOON PASSED", r_title)
					url = r_href
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
            absolute_id = num.encode('utf-8')
            # print("ANIMETOON EPISODES", season, episode, num)
            headers = {'User-Agent': random_agent()}
            r = BeautifulSoup(requests.get(url, headers=headers).content)
            r = r.findAll('div', attrs={'id': 'videos'})
            for containers in r:
                r_block = containers.findAll('a')
                for links in r_block:
                    ep_href = links['href'].encode('utf-8')
                    # print("ANIMETOON", ep_href)
                    if "-season-" in ep_href:
						# print("ANIMETOON SEASON MATCHING")
						checkseason = re.search("-season-(\d+)-", ep_href)
						if checkseason:
							checkseason = checkseason.group(1)
							if checkseason == season:
								checkepisode = re.search("-episode-(\d+)", ep_href)
								if checkepisode:
										checkepisode = checkepisode.group(1)
										if checkepisode == episode:
											# print("ANIMETOON PASSED", ep_href)
											url = ep_href
											return url

                    else:
						# print("ANIMETOON ABSOLUTEID MATCHING")
						checkepisode = re.search("-episode-(\d+)", ep_href)
						if checkepisode:
								checkepisode = checkepisode.group(1)
								if checkepisode == absolute_id:
									# print("ANIMETOON PASSED", ep_href)
									url = ep_href
									return url
										
           
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': random_agent()}
            if url == None: return sources
            # print("ANIMETOON SOURCES", url)
            r = BeautifulSoup(requests.get(url, headers=headers).content)
            r = r.findAll('iframe')
            # print ("ANIMETOON s1",  r)
            for u in r:
                try:
                    u = u['src'].encode('utf-8')
                    # print ("ANIMETOON s2",  u)
                    
                    html = requests.get(u, headers=headers).text
                    r_src = re.compile("url:\s*'(.+?)'").findall(html)
                    for src in r_src:
                        # print ("ANIMETOON s3",  src)
                        vid_url = src.encode('utf-8')
                        sources.append({'source': 'cdn', 'quality': 'SD', 'provider': 'Animetoon', 'url': vid_url, 'direct': True, 'debridonly': False})
                       
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url



