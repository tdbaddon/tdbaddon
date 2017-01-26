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
import re,urllib,urlparse,hashlib,random,string,json,base64,requests
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent, quality_tag
rq = requests.session()


class source:
    def __init__(self):
        self.domains = ['afdah.tv']
        self.base_link = 'http://afdah.tv'
        self.search_link = '/?s=%s'
        
		
		
    def movie(self, imdb, title, year):
		try:
			self.zen_url = []
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			headers = {'User-Agent': random_agent(), 'X-Requested-With':'XMLHttpRequest'}
			search_url = urlparse.urljoin(self.base_link, '/wp-content/themes/afdah/ajax-search.php')
			data = {'search': title, 'type': 'title'}
			# print("AFMOVIE query", search_url)
			moviesearch = requests.post(search_url, headers=headers, data=data)
			moviesearch = moviesearch.content
			match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(moviesearch)
			for href, movietitle in match:
				if year in movietitle and cleanmovie == cleantitle.get(movietitle):
					# print("AFMOVIE FOUND MATCH moviesearch", href, movietitle)
					url = href.encode('utf-8')
					if not "http" in url: url = urlparse.urljoin(self.base_link, url)
					return url
		except:
			return
			
			
		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			
			try:
				headers = {'User-Agent': random_agent()}
				html = rq.get(url, headers=headers, timeout=10).text				
				try:

					for match in re.finditer('href="([^"]+/embed\d*/[^"]+)', html):
						iframe = match.group(1)
						# print ("AFMOVIES match", url)
						iframe = iframe.encode('utf-8')
						embed_html = client.request(iframe)
						r = re.search('salt\("([^"]+)', embed_html)						
						if r:
							# print ("AFMOVIES FOUND SALT", r)
							plaintext = self.__caesar(self.__get_f(self.__caesar(r.group(1), 13)), 13)
							# print ("AFMOVIES PLAINTEXT", plaintext)
							match = re.search('sources\s*:\s*\[(.*?)\]', plaintext, re.DOTALL)
							if not match:
								match = re.search('sources\s*:\s*\{(.*?)\}', plaintext, re.DOTALL)
							if match:
								for match in re.finditer('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', match.group(1), re.DOTALL):
									stream_url, label = match.groups()
									stream_url = stream_url.replace('\/', '/')
									# print ("AFMOVIES stream_url", stream_url)
									quality = quality_tag(label)
									stream_url = "gvideo_link" + stream_url
									sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Afmovies', 'url': stream_url,  'direct': True, 'debridonly': False})
				except:
					pass
				try:
					pattern = 'href="([^"]+)[^>]*>\s*<[^>]+play_video.gif'
					for match in re.finditer(pattern, html, re.I):
						stream_url = match.group(1)
						try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(stream_url.strip().lower()).netloc)[0]
						except: host = 'Afmovies'
						host = client.replaceHTMLCodes(host)
						host = host.encode('utf-8')		
						if not host in hostDict: continue
						sources.append({'source': host, 'quality': 'SD', 'provider': 'Afmovies', 'url': stream_url,  'direct': True, 'debridonly': False})
				except:
					pass
			except:
				pass
			return sources
        except:
            return sources


    def resolve(self, url):
		if "gvideo_link" in url:
			url = url.replace('gvideo_link','')
			if not "google" in url: url = client.request(url, output='geturl', timeout='10')
		return url
		
		
    def __caesar(self, plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))

    def __get_f(self, s):
        i = 0
        t = ''
        l = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
        while i < len(s):
            try:
                c1 = l.index(s[i])
                c2 = l.index(s[i + 1])
                t += chr(c1 << 2 & 255 | c2 >> 4)
                c3 = l.index(s[i + 2])
                t += chr(c2 << 4 & 255 | c3 >> 2)
                c4 = l.index(s[i + 3])
                t += chr(c3 << 6 & 255 | c4)
                i += 4
            except:
                break
    
        return t