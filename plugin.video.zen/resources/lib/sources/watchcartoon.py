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
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['www.animetoon.org']
		
        self.cartoon_link = ['http://www.watchcartoononline.io/cartoon-list', 'http://www.watchcartoononline.io/subbed-anime-list', 'http://www.watchcartoononline.io/dubbed-anime-list']
		
    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            headers = {'User-Agent': random_agent()}
            # print("WATCHCARTOON")
            title = cleantitle.get(tvshowtitle)
            for url in self.cartoon_link:
				r = requests.get(url, headers=headers).text
				match = re.compile('<a href="(.+?)" title=".+?">(.+?)</a>').findall(r)
				for url, name in match:
					if title == cleantitle.get(name):
						print("WATCHCARTOON PASSED", url)
						return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = url.replace('https', 'http')
            num = base64.b64decode('aHR0cDovL3RoZXR2ZGIuY29tL2FwaS8xRDYyRjJGOTAwMzBDNDQ0L3Nlcmllcy8lcy9kZWZhdWx0LyUwMWQvJTAxZA==')
            num = num % (tvdb, int(season), int(episode))
            num = client.request(num)
            num = client.parseDOM(num, 'absolute_number')[0]
            absolute_id = num.encode('utf-8')
            print("WATCHCARTOON EPISODES", season, episode, absolute_id)
            headers = {'User-Agent': random_agent()}
            r = requests.get(url, headers=headers).text
            r = re.compile('<a href="(.+?)" rel="bookmark" title=".+?"').findall(r)
            for ep_href in r:
                    # print("WATCHCARTOON EPISODES", ep_href)
                    if "-season-" in ep_href:
						# print("WATCHCARTOON SEASON MATCHING")
						checkseason = re.search("-season-(\d+)-", ep_href)
						if checkseason:
							checkseason = checkseason.group(1)
							if checkseason == season:
								checkepisode = re.search("-episode-(\d+)", ep_href)
								if checkepisode:
										checkepisode = checkepisode.group(1)
										if checkepisode == episode:
											print("WATCHCARTOON PASSED", ep_href)
											url = ep_href
											return url

                    else:
						# print("WATCHCARTOON ABSOLUTEID MATCHING")
						checkepisode = re.search("-episode-(\d+)", ep_href)
						if checkepisode:
								checkepisode = checkepisode.group(1)
								if checkepisode == absolute_id:
									# print("WATCHCARTOON PASSED", ep_href)
									url = ep_href
									return url
										
           
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': random_agent()}
            if url == None: return sources
            url = url.replace('https', 'http')
            # print("ANIMETOON SOURCES", url)
            mobile_url = url.replace('www', 'm')
           
            html = requests.get(mobile_url, verify=False).text
           
            match_playlink = re.compile('<source src="(.+?)"').findall(html)
            for playlink in match_playlink:
                    url = playlink.encode('utf-8')
                    sources.append({'source': 'cdn', 'quality': 'SD', 'provider': 'Watchcartoon', 'url': url, 'direct': True, 'debridonly': False})



            return sources
        except:
            return sources


    def resolve(self, url):
        return url



