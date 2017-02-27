import re
import urllib
import requests
import urlparse
import json
import xbmc
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import  random_agent
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
	
        self.base_link = control.setting('watchepisodes_base')
        if self.base_link == '' or self.base_link == None:self.base_link = 'http://www.watchepisodes4.com'
        self.search_link = '/search/ajax_search?q=%s'


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
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            data['season'], data['episode'] = season, episode
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = cleantitle.get(title)
            ep_id = int(episode)
            season_id = int(season)
            html = requests.get(query, headers=headers, timeout=30).json()
            results = html['series']
            for item in results:
				r_title = item['label'].encode('utf-8')
				r_link = item['seo'].encode('utf-8')
				if cleaned_title == cleantitle.get(r_title):
					r_page = self.base_link + "/" + r_link
					print("WATCHEPISODES r1", r_title,r_page)
					r_html = BeautifulSoup(requests.get(r_page, headers=headers, timeout=30).content)
					r = r_html.findAll('div', attrs={'class': re.compile('\s*el-item\s*')})
					for container in r:
						try:
							r_href = container.findAll('a')[0]['href'].encode('utf-8')
							r_title = container.findAll('a')[0]['title'].encode('utf-8')
							print("WATCHEPISODES r3", r_href,r_title)
							episode_check = "[sS]%02d[eE]%02d" % (int(season), int(episode))
							match = re.search(episode_check, r_title)
							if match:
								print("WATCHEPISODES PASSED EPISODE", r_href)
								self.zen_url.append(r_href)
								
							else:
								match2 = re.search(episode_check, r_href)
								if match2:
									self.zen_url.append(r_href)
						except:
							pass
            print ("WATCHEPISODES LIST", self.zen_url)
            return self.zen_url					
        except:
            pass
      
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			count = 0
			for url in self.zen_url:
				headers = {'User-Agent': random_agent()}
				html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
				print ("WATCHEPISODES SOURCES", url)
				r = html.findAll('div', attrs={'class': 'site'})
				for container in r:
					if count > 100: break
					try:
						count += 1
						r_url = container.findAll('a')[0]['data-actuallink'].encode('utf-8')
						print ("WATCHEPISODES r_url", r_url)
						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(r_url.strip().lower()).netloc)[0]
						host = host.encode('utf-8')
						if not host in hostDict: raise Exception()
						sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchepisodes', 'url': r_url, 'direct': False, 'debridonly': False})
					except:
						pass
			return sources
        except:
            return sources


    def resolve(self, url):
            return url