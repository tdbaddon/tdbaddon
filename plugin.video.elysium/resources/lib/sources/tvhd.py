import re
import urllib
import requests
import urlparse
import json
import xbmc
import datetime

from BeautifulSoup import BeautifulSoup
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from schism_net import OPEN_URL

debridstatus = control.setting('debridsources')

class source:
    def __init__(self):
	
        self.base_link = 'http://tvshows-hdtv.org'
        self.search_link = '/_new.episodes.%s.html'


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            if not debridstatus == 'true': raise Exception()	
            url = {'tvshowtitle': tvshowtitle}
            url = urllib.urlencode(url)
            return url
        except:
            return	
			
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.elysium_url = []
        try:
            if not debridstatus == 'true': raise Exception()	
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            data['season'], data['episode'] = season, episode
            today = datetime.datetime.today().date()
            today = today.strftime('%Y.%m.%d')
            
            title = cleantitle_get(title)
            titlecheck = "s%02de%02d" % (int(data['season']), int(data['episode']))
            titlecheck = title + titlecheck
            premiered = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(premiered)[0]
            year = premiered[0]
            days = premiered[-1] 
            month	= premiered[1]	
            next_day = int(days) + 1			
            
            ep_date = "%s.%02d.%02d" % (year,int(month),int(days))
            # print ("HDTV PREMIERE", ep_date , today)   
            if int(re.sub('[^0-9]', '', str(ep_date))) > int(re.sub('[^0-9]', '', str(today))): raise Exception()
            ep_next_date = "%s.%02d.%02d" % (year,int(month),int(next_day))
            # print ("HDTV PREMIERE", ep_date, ep_next_date) 			
            # print ("HDTV PREMIERE", today, ep_date, ep_next_date)
            for day in [ep_date, ep_next_date]:
				html = self.search_link % day
				html = urlparse.urljoin(self.base_link, html)
				# print ("HDTV PREMIERE 2 ", html)
				r = OPEN_URL(html).content
				for match in re.finditer('<center>\s*<b>\s*(.*?)\s*</b>.*?<tr>(.*?)</tr>', r, re.DOTALL):
					release, links = match.groups()
					release = re.sub('</?[^>]*>', '', release)
					release = cleantitle_get(release)
					if titlecheck in release:
						# print ("HDTV PREMIERE 3 FOUND", release , links)
						self.elysium_url.append([release,links])
						
            return self.elysium_url					
        except:
            pass
      
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			count = 0
			for title,url in self.elysium_url:
				quality = quality_tag(title)
				for match in re.finditer('href="([^"]+)', url):
					url = match.group(1)
					try: host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
					except: host = "none"
					if any(value in url for value in hostprDict):
						# print ("HDTV SOURCES", quality, url)
						url = url.encode('utf-8')
						sources.append({'source': host, 'quality': quality, 'provider': 'tvhd', 'url': url, 'direct': False, 'debridonly': True})

			return sources
        except:
            return sources


    def resolve(self, url):
            return url