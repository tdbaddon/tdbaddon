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
from resources.lib.modules import jsunpack
s = requests.session()
class source:
    def __init__(self):
        self.domains = ['pmovies.to', 'cmovieshd.com']
        self.base_link = 'http://watch5s.to'
        self.search_link = '/search/?q=%s+%s'
		
    def movie(self, imdb, title, year):
		try:
			self.url = []
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})
			for links in r:
				pageurl = client.parseDOM(links, 'a', ret='href')[0]
				info = client.parseDOM(links, 'a', ret='rel')[0]
				title = client.parseDOM(links, 'a', ret='title')[0]
				info = info.encode('utf-8')
				title = title.encode('utf-8')
				# print("CMOVIES LINKS", pageurl,info,title)
				if cleanmovie in cleantitle.get(title):
					infolink = client.request(info)
					match_year = re.search('class="jt-info">(\d{4})<', infolink)
					match_year = match_year.group(1)
					# print("CMOVIES YEAR",match_year)
					if year in match_year:
						# print("CMOVIES PASSED") 
						referer = pageurl.encode('utf-8')
						url = referer + 'watch'
						# print("CMOVIES PASSED",referer,url) 
						link = client.request(url, timeout='5')
						r = client.parseDOM(link, 'div', attrs = {'class': 'les-content'})
						for item in r:
							try:
								vidlinks = client.parseDOM(item, 'a', ret='href')[0]
								vidlinks = vidlinks.encode('utf-8')
								# print('CMOVIES SERVER LINKS',vidlinks)
								self.url.append([vidlinks,referer])
							except:
								pass
			print("CMOVIES PASSED LINKS", self.url)
			return self.url
		except:
			return self.url
			
			
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
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})

			for links in r:
				pageurl = client.parseDOM(links, 'a', ret='href')[0]
				info = client.parseDOM(links, 'a', ret='rel')[0]
				title = client.parseDOM(links, 'a', ret='title')[0]
				info = info.encode('utf-8')
				title = title.encode('utf-8')
				if checktitle == cleantitle.get(title):
					# print("CMOVIES LINKS", pageurl,info,title)
					referer = pageurl.encode('utf-8')
					ep_url = referer + 'watch'
					ep_links = client.request(ep_url)
					r_ep = client.parseDOM(ep_links, 'div', attrs = {'class': 'les-content'})
					for item in r_ep:
						match = re.compile('<a href="(.*?)" class=.*?">Episode (\d+):').findall(item)
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
			for movielink,referer in self.url:
				try:
					# print("CMOVIES SOURCE LINKS", movielink)
					if len(sources) > 2: break
					referer = referer
					pages = client.request(movielink, timeout='3')
					scripts = re.findall('<script src="(.*?)">', pages)
					# print("CMOVIES SERVER SCRIPT", scripts)
					for items in scripts:
						if "slug=" in items:
							if len(sources) > 2: break
							headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}
							result = s.get(items, headers=headers, timeout=3).content
							if jsunpack.detect(result):
								js_data = jsunpack.unpack(result)
								match = re.search('"sourcesPlaylist"\s*:\s*"([^"]+)', js_data)
								video_url = match.group(1).replace('\\','')								
								headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}
								streams = s.get(video_url, headers=headers, timeout=3).json()			
								# print("CMOVIES FOUND PLAYLIST UNPACKED", streams)
								playurl  = streams['playlist'][0]['sources']
								for results in playurl:	
									url = results['file']
									quality = results['label']
									if "1080" in quality: quality = "1080p"
									elif "720" in quality: quality = "HD"
									else: quality = "SD"
									url = url.encode('utf-8')
									if "google" in url:
										print("CMOVIES PLAYABLE LINKS", url, quality)
										sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Watch5s', 'url': url, 'direct': True, 'debridonly': False})

				except:
					pass
			return sources
        except:
            return sources


    def resolve(self, url):
        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
        else: url = url.replace('https://', 'http://')
        return url
