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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from schism_net import OPEN_URL, OPEN_CF, get_sources, get_files
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from BeautifulSoup import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviefree.to']
        self.base_link = 'http://chillnflix.to'
        self.movie_link = '/%s-%s-watch-online-for-free/'
        self.shows_link = '/tvshows/%s-season-%s-watch-online-free/?action=watching&server=1&movie=%s-%s&auto=true'	



    def movie(self, imdb, title, year):
        try:
			
            url = self.movie_link % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url, timeout='10')
            print("Chillflix url", url)

            r = re.findall('<a href="(.+?)" class="bwac-btn"', r)[0]
            url = r.encode('utf-8')
            print("Chillflix url", url)
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
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            ep_id = "%01dx%01d" % (int(season), int(episode))
            url = self.shows_link % (cleantitle.geturl(title), season, cleantitle.geturl(title), ep_id)
            url = urlparse.urljoin(self.base_link, url)

            url = url.encode('utf-8')
            print("Chillflix shows url", url)
            return url
        except:
            return			
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
            r = client.request(url)
            try:
				s = re.compile('file"?:\s*"([^"]+)"').findall(r)

				for u in s:
					try:
						quality = google_tag(u)
						
						url = u.encode('utf-8')
						if quality == 'ND': quality = "SD"
						# if ".vtt" in url: raise Exception()
						sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Chillflix', 'url': url, 'direct': True, 'debridonly': False})

					except:
						pass
            except:
				pass
				
            try:
				
				r = BeautifulSoup(r)
				
				iframe = r.findAll('iframe')[0]['src'].encode('utf-8')
				print ("CHILLFLIX IFRAME CHECK 2", iframe)
				if "wp-embed.php" in iframe:
					if iframe.startswith('//'): iframe = "http:" + iframe
					
					s = client.request(iframe)
					print ("CHILLFLIX IFRAME CHECK 3", s)
					s = get_sources(s)
					

					for u in s:
						try:
							files = get_files(u)
							for url in files:
								url = url.replace('\\','')
								quality = google_tag(url)
								
								url = url.encode('utf-8')
								if quality == 'ND': quality = "SD"
								# if ".vtt" in url: raise Exception()
								sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Chillflix', 'url': url, 'direct': True, 'debridonly': False})

						except:
							pass
            except:
				pass
					
			# try:
				
				# r = BeautifulSoup(r)
				
				# iframe = r.findAll('iframe')[0]['src'].encode('utf-8')
				
				# if "wp-embed.php" in iframe:
					# if iframe.startswith('//'): iframe = "http:" + iframe

					# s = client.request(iframe)
					# s = get_sources(s)

			   

					# for u in s:
						# try:
							# files = get_files(u)
							# for url in files:
								# quality = google_tag(url)
								
								# url = url.encode('utf-8')
								# if quality == 'ND': quality = "SD"
								# # if ".vtt" in url: raise Exception()


							   
								# sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Chillflix', 'url': url, 'direct': True, 'debridonly': False})

						# except:
							# pass
			# except:
				# pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


