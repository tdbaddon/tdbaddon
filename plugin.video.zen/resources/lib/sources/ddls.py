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



import re,urllib,urlparse,random
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client

debridstatus = control.setting('debridsources')
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['ddlseries.net']
        self.base_link = 'http://www.ddlseries.me'
        self.search_link = '/index.php?do=charmap&name=tv-series-list&args=/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return			

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []	
        try:
			if not debridstatus == 'true': raise Exception()
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = cleantitle.getsearch(title)
			title_init = title[0]
			print ("DDL TITLE INIT", title_init)
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			self.zen_url = []
			seasoncheck = "%02d" % (int(data['season']))
			episodecheck = "%02d" % int(data['episode'])
			episodecheck = str(episodecheck)
			query = self.search_link % title_init
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'downpara-list'})
			r = r[0]
			if r:
				match = re.compile('<a href="([^"]+)[^>]*>(.*?)</a>').findall(r)
				for match_url, match_title in match:
					try:
						r_url = match_url.encode('utf-8')
						r_title = match_title.encode('utf-8')
						
						seasonid = re.findall("(?:S|s)eason (\d*)",r_title)[0]
						
						seasonid = seasonid.encode('utf-8')
						if seasonid == season:
							if cleanmovie in cleantitle.get(r_title):
								if not "(Pack)" in r_title:
									# print ("DDLS TV ",match_title)
									quality = quality_tag(r_title)
									# match_url = client.request(match_url, output='geturl')
									print ("PASSED DDLSTV", r_url,quality,episodecheck)
									self.zen_url.append([r_url,quality,episodecheck])
					except:
						pass
			return self.zen_url
        except:
            return		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for links,quality,episodecheck in self.zen_url:
				link = client.request(links)

				match = re.compile('href="([^"]+)[^>]*>\s*Episode\s+(\d+)<').findall(link)
				for url, ep in match:
					if episodecheck == ep:
						# print ("DDLTV", url)
						if "protect-links" in url:
							redirect = client.request(url)
							url = re.findall('<a href="(.+?)" target="_blank">', redirect)
							url = url[0].encode('utf-8')
						if any(x in url for x in ['.rar', '.zip']): continue
						if any(value in url for value in hostprDict):
							
							try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
							except: host = 'none'
							url = client.replaceHTMLCodes(url)
							url = url.encode('utf-8')
							sources.append({'source': host, 'quality': quality, 'provider': 'Ddls', 'url': url, 'direct': False, 'debridonly': True})
			return sources
        except:
            return sources


    def resolve(self, url):

            return url