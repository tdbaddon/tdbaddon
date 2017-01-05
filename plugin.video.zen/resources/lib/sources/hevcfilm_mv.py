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
        self.domains = ['hevcbluray.info']
        self.base_link = 'http://www.hevcbluray.info'
        self.search_link = '/?s=%s'
        
		
		
    def movie(self, imdb, title, year):
		try:
			self.zen_url = []
			headers = {'User-Agent': random_agent()}

			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			query = self.search_link % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			print("HEVC query", query)
			html = BeautifulSoup(rq.get(query, headers=headers, timeout=10).content)
			
			containers = html.findAll('div', attrs={'class': 'item'})
			
			for result in containers:
				print("HEVC containers", result)
				match_year = re.findall('<span class="year">(.+?)</span>', str(result))[0]
				if match_year == year:
					print("HEVC FOUND MOVIE YEAR", match_year)
					r_title = re.findall('<span class="tt">(.+?)</span>', str(result))[0]
					r_href = result.findAll('a')[0]["href"]
					r_href = r_href.encode('utf-8')
					r_title = r_title.encode('utf-8')
					if cleanmovie in cleantitle.get(r_title):
						self.zen_url.append([r_href,r_title])
						print("HEVC PASSED MOVIE ", r_title, r_href)
			return self.zen_url
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
			self.url = []
			headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			year = data['year'] 
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			seasoncheck = "season%s" % season
			episode = "%01d" % int(episode)
			checktitle = cleanmovie + seasoncheck
			seasonquery = "season+%s" % season
			query = self.search_link % (urllib.quote_plus(title),seasonquery)
			query = urlparse.urljoin(self.base_link, query)
			# print("CMOVIES query", query)
			link = rq.get(query, headers=headers, timeout=10).text
			# print("CMOVIES LINKS", link)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})
			for links in r:
				pageurl = client.parseDOM(links, 'a', ret='href')[0]
				info = client.parseDOM(links, 'a', ret='rel')[0]
				title = client.parseDOM(links, 'a', ret='title')[0]
				info = info.encode('utf-8')
				title = title.encode('utf-8')
				if checktitle == cleantitle.get(title):
					# print("CMOVIES LINKS", pageurl,info,title)
					pageurl = pageurl.encode('utf-8')
					ep_url = pageurl + 'watch/'
					referer = ep_url
					ep_links = rq.get(ep_url, headers=headers, timeout=5).text
					r_ep = client.parseDOM(ep_links, 'div', attrs = {'class': 'les-content'})
					for item in r_ep:
						match = re.compile('<a href="(.*?)" class=.*?">Episode\s*(\d+)').findall(item)
						for href, ep_items in match:
							ep_items = '%01d' % int(ep_items)
							if ep_items == episode:
								# print("CMOVIES SHOWS",href,ep_items) 
								self.url.append([href,referer])
			# print("CMOVIES PASSED LINKS", self.url)
			return self.url
		except:
			return
		
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,title in self.zen_url:
				try:
					headers = {'User-Agent': random_agent()}
					html = BeautifulSoup(rq.get(movielink, headers=headers, timeout=10).content)
					
					containers = html.findAll('li', attrs={'class': 'elemento'})
					for result in containers:
						print("HEVC result", result)
						quality_info = re.findall('<span class="d">(.+?)</span>', str(result))[0]
						url = result.findAll('a')[0]["href"]
						url = url.encode('utf-8')
						quality_info = quality_info.encode('utf-8')
						
						if "3d" in quality_info.lower():
							info = "3D"
							quality = quality_tag(title)
						else:
							info = "HEVC"
							quality = quality_tag(quality_info)
							print("HEVC quality url", quality, info)
						
						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
						host = host.encode('utf-8')
						if not host in hostDict: continue
						sources.append({'source': host, 'quality': quality, 'provider': 'Hevcfilm', 'url': url, 'info':info, 'direct': False, 'debridonly': False})

				except:
					pass
			return sources
        except:
            return sources


    def resolve(self, url):
        return url