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
from resources.lib.modules import jsunpack
from resources.lib.modules import directstream
class source:
    def __init__(self):
        self.domains = ['moviego.cc']
        self.base_link = 'http://moviego.cc'
        self.search_link = '/index.php?do=search&subaction=search&full_search=1&result_from=1&story=%s+%s'
        self.ep_url = '/engine/ajax/getlink.php?id=%s'

    def movie(self, imdb, title, year):
        self.url = []	
        try:
					
			self.url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			searchquery = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, searchquery)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'short_overlay'})
			r = [(client.parseDOM(i, 'a', ret='href')) for i in r]
			r = [i for i in r if len(i) > 0]
			r = [i[0] for i in r if cleanmovie in cleantitle.get(i[0]) and year in i[0]][0]
			url = r
			url = client.replaceHTMLCodes(url)
			url = url.encode('utf-8')
			# print("MOVIEGO URL r2", url)
			return url
        except:
            return
			

		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			alt_links = []
			play_links = []
			link = client.request(url)
			film_quality = re.findall('<div class="poster-qulabel">(.*?)</div>',link)[0]
			if "1080" in film_quality: quality = "1080p"
			elif "720" in film_quality: quality = "HD"
			else: quality = "SD"
			try:
				iframe = re.findall('<iframe src="([^"]+)"',link)[0]
				if iframe:
					original_frame = iframe
					# print ("MOVIEGO VIDEOURL", iframe)
					videourl = client.request(iframe)
					
					scripts_packs = re.compile('<script>(.+?)</script>', re.DOTALL).findall(videourl)
					for pack in scripts_packs:
						if jsunpack.detect(pack):
							data_script = jsunpack.unpack(pack)
							try:
								alternative_links = re.findall('Alternative (\d+)<', data_script)
								for alts in alternative_links: alt_links.append(alts)
							except:
								pass
							video_src = re.findall('<source src="([^"]+)"', data_script)
							# print ("MOVIEGO data_script", data_script)
							for url in video_src:
								url = url.replace(' ', '')
								if "google" in url:
									play_links.append(url)
			except:
				pass
			try:
					for ids in alt_links:
						newframes = original_frame + "?source=a" + ids
						# print ("MOVIEGO NEW FRAMES", newframes)
						newurl = client.request(newframes)
						scripts_newpacks = re.compile('<script>(.+?)</script>', re.DOTALL).findall(newurl)
						for new_pack in scripts_newpacks:
							if jsunpack.detect(new_pack):
								new_data_script = jsunpack.unpack(new_pack)
								new_video_src = re.findall('<source src="([^"]+)"', new_data_script)
								# print ("MOVIEGO ALT video_src", video_src)
								for new_url in new_video_src:
									new_url = new_url.replace(' ', '')
									if "google" in new_url:
										play_links.append(new_url)
			except:
				pass
				
			try:
				dupes = []
				for url in play_links:
					if not url in dupes:
						dupes.append(url)
						print ("MOVIEGO PLAY url", url)
						quality = directstream.googletag(url)[0]['quality']
						url = client.replaceHTMLCodes(url)
						url = url.encode('utf-8')
						sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Moviego', 'url': url, 'direct': True, 'debridonly': False})
			except:
				pass

				
			try:
				url = re.findall('file:\s+"([^"]+)"',link)[0]
				sources.append({'source': 'cdn', 'quality': quality, 'provider': 'Moviego', 'url': url, 'direct': True, 'debridonly': False})
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