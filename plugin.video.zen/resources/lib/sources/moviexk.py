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
import re,urllib,urlparse,hashlib,random,string,json,base64
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules.common import  random_agent
import requests
from BeautifulSoup import BeautifulSoup

class source:
    def __init__(self):
        self.base_link = 'http://moviexk.com'
        self.search_link = '/search/%s+%s'
		
    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title),year)
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = cleantitle.get(title)
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
           
            containers = html.findAll('div', attrs={'class': 'name'})
            for container in containers:
                # print ("MOVIEXK r1", container)
                r_href = container.findAll('a')[0]["href"]
                r_href = r_href.encode('utf-8')
                # print ("MOVIEXK r2", r_href)
                r_title = re.findall('</span>(.*?)</a>', str(container))[0]
                # print ("MOVIEXK r3", r_title)
                r_title = r_title.encode('utf-8')
                # print ("MOVIEXK RESULTS", r_title, r_href)
                if year in r_title:

					if cleaned_title == cleantitle.get(r_title):
						redirect = requests.get(r_href, headers=headers, timeout=30).text
						try:
							r_url_trailer = re.search('<dd>[Tt]railer</dd>', redirect)
							if r_url_trailer: continue
						except:
							pass
						r_url = re.findall('<a href="(.+?)" class="btn-watch"',redirect)[0]
						r_url = r_url.encode('utf-8')
						print ("MOVIEXK PLAY URL", r_url)
						self.zen_url.append(r_url)
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
        self.zen_url = []	
        try:
            # print ("MOVIEXK")
            headers = {'User-Agent': random_agent()}
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.getsearch(title)
            cleanmovie = cleantitle.get(title)
            data['season'], data['episode'] = season, episode
            year = data['year']
            query = self.search_link % (urllib.quote_plus(title),year)
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = cleantitle.get(title)
            ep_id = int(episode)
            season_id = int(season)
            season_check = "%02d" % (int(data['season']))
            ep_check =season_id + ep_id
            # print("MOVIEXK EPISODE CHECK", ep_check)
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
            containers = html.findAll('div', attrs={'class': 'name'})
            for container in containers:
                # print ("MOVIEXK r1", container)
                r_href = container.findAll('a')[0]["href"]
                r_href = r_href.encode('utf-8')
                # print ("MOVIEXK r2", r_href)
                r_title = re.findall('</span>(.*?)</a>', str(container))[0]
                # print ("MOVIEXK r3", r_title)
                r_title = r_title.encode('utf-8')
                if cleaned_title in cleantitle.get(r_title):
						redirect = requests.get(r_href, headers=headers, timeout=30).text
						r_url = re.findall('<a href="(.+?)" class="btn-watch"',redirect)[0]
						r_url = r_url.encode('utf-8')
						r_episode = re.findall('<a href=".+?" class="btn-watch" title="(.+?)">',redirect)[0]
						r_episode = r_episode.encode('utf-8')
						seasonid = re.findall("(?:S|s)eason (\d*)",r_episode)[0]
						seasonid = int(seasonid)
						seasonid = "%02d" % (int(seasonid))
						# print ("MOVIEXK seasonid", seasonid)
						if seasonid != season_check: continue
						links = BeautifulSoup(requests.get(r_url, headers=headers, timeout=30).content)
						ep_items = links.findAll('ul', attrs={'class': 'episodelist'})
						for items in ep_items:
								ep_links = items.findAll('a')
								for r in ep_links:
									# print ("MOVIEXK r5", r)
									ep_url = r['href'].encode('utf-8')
									ep_title = r['title'].encode('utf-8')
									clean_ep_title = cleantitle.get(ep_title)
									# print ("MOVIEXK clean_ep_title", clean_ep_title)
									if "s%02de%02d" % (season_id, ep_id) in clean_ep_title: self.zen_url.append(ep_url)
									elif "s%02d%02d" % (season_id, ep_id) in clean_ep_title: self.zen_url.append(ep_url)
									elif "ep%02d" % (ep_id) in clean_ep_title: self.zen_url.append(ep_url)
            return self.zen_url
        except:
            return		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for url in self.zen_url:
				
				headers = {'User-Agent': random_agent()}
				html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
				r = html.findAll('source')
				for r_source in r:
					url = r_source['src'].encode('utf-8')
					quality = r_source['data-res'].encode('utf-8')
					if "1080" in quality: quality = "1080p"
					elif "720" in quality: quality = "HD"
					else: quality = "SD"
					print ("MOVIEXK SOURCES", url,quality)
					sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Moviexk', 'url': url, 'direct': True, 'debridonly': False})
			return sources
        except:
            return sources


    def resolve(self, url):
            return url
