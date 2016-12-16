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

from resources.lib.modules.common import  random_agent, quality_tag
rq = requests.session()
class source:
    def __init__(self):
        self.domains = ['watch5s.to','pmovies.to', 'cmovieshd.com']
        self.base_link = 'http://cmovieshd.com'
        self.search_link = '/search/?q=%s+%s'
        self.stream_link = 'http://streaming.cmovieshd.com/videoplayback/%s?key=%s'
    def movie(self, imdb, title, year):
		try:
			self.url = []
			headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			query = self.search_link % (urllib.quote_plus(title),year)
			query = urlparse.urljoin(self.base_link, query)
			# print("CMOVIES query", query)
			link =rq.get(query, headers=headers, timeout=10).text
			# print("CMOVIES url", link)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})
			for links in r:
				# print("CMOVIES LINKS", links)
				pageurl = client.parseDOM(links, 'a', ret='href')[0]
				info = client.parseDOM(links, 'a', ret='rel')[0]
				title = client.parseDOM(links, 'a', ret='title')[0]
				info = info.encode('utf-8')
				title = title.encode('utf-8')
				# print("CMOVIES LINKS", pageurl,info,title)
				if cleanmovie in cleantitle.get(title):
					infolink = rq.get(info, headers=headers, timeout=5).text
					match_year = re.search('class="jt-info">(\d{4})<', infolink)
					match_year = match_year.group(1)
					# print("CMOVIES YEAR",match_year)
					if year in match_year:
						# print("CMOVIES PASSED") 
						pageurl = pageurl.encode('utf-8')
						url = pageurl + 'watch/'
						referer = url
						# print("CMOVIES PASSED",referer,url) 
						link = rq.get(url, headers=headers, timeout=10).text
						r = client.parseDOM(link, 'div', attrs = {'class': 'les-content'})
						for item in r:
							try:
								vidlinks = client.parseDOM(item, 'a', ret='href')[0]
								vidlinks = vidlinks.encode('utf-8')
								# print('CMOVIES SERVER LINKS',vidlinks)
								self.url.append([vidlinks,referer])
							except:
								pass
			# print("CMOVIES PASSED LINKS", self.url)
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
			for movielink,referer in self.url:
				try:
					headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': random_agent()}
					referer = referer
					pages = rq.get(movielink, headers=headers, timeout=10).text
					scripts = re.findall('hash\s*:\s*"([^"]+)', pages)[0]
					# print("CMOVIES SERVER SCRIPT", scripts)
					if scripts:
						token = self.__get_token()
						key = hashlib.md5('(*&^%$#@!' + scripts[46:58]).hexdigest()
						cookie = '%s=%s' % (key, token)	
						stream_url = self.stream_link % (scripts, hashlib.md5('!@#$%^&*(' + token).hexdigest())
						# print("CMOVIES PLAYABLE LINKS", stream_url)
						headers = {'Accept-Language': 'en-US,en;q=0.5', 'Referer': referer, 'User-Agent': random_agent(), 'Cookie': cookie}
						req = rq.get(stream_url, headers=headers, timeout=5).json()
						playlist = req['playlist'][0]['sources']
						for item in playlist:
							url = item['file'].encode('utf-8')
							r_quality =  item['label'].encode('utf-8')
							quality = quality_tag(r_quality)
							# print("CMOVIES playlist", quality ,url)
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

		
    def __get_token(self):
        return ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 16))		
		
