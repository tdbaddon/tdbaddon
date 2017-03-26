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
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

import re,urllib,urlparse,hashlib,random,string,json,base64
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules.common import  random_agent
import requests
from BeautifulSoup import BeautifulSoup
alluc_debrid = control.setting('debrid_service')
alluc_status = control.setting('enable_alluc')
alluc_user = control.setting('alluc_username')
alluc_pw = control.setting('alluc_password')
max_items = int(control.setting('alluc_max_results'))
host_string = 'host%3Arapidgator.net%2Cuploaded.net%2Cfilefactory.com'
max_result_string = '&count=%s' % max_items
# %s&query=%s+host%3Arapidgator.net%2Cuploaded.net%2Cfilefactory.com&count=%s'
class source:
    def __init__(self):
        self.base_link = 'https://www.alluc.ee'
        if alluc_debrid == 'true': self.api_link = 'http://www.alluc.ee/api/search/download/?user=%s&password=%s&query=%s' 
        else: self.api_link = 'http://www.alluc.ee/api/search/stream/?user=%s&password=%s&query=%s'  

		
    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
            if not alluc_status == 'true': raise Exception()
            print ("ALLUC STARTED" , alluc_user, alluc_pw, max_items)
            headers = {'User-Agent': random_agent()}
            search_title = cleantitle.getsearch(title)
            cleanmovie = cleantitle.get(title) + year
            query = "%s+%s" % (urllib.quote_plus(search_title),year)
            print ("ALLUC r1", query)
            query =  self.api_link % (alluc_user, alluc_pw, query)
            if alluc_debrid == 'true': query =	query + max_result_string
            else: query = query + '+%23newlinks' + max_result_string
            print ("ALLUC r2", query)
            html = requests.get(query, headers=headers, timeout=15).json()
            for result in html['result']:
				if len(result['hosterurls']) > 1: continue
				if result['extension'] == 'rar': continue
				stream_url = result['hosterurls'][0]['url'].encode('utf-8')
				stream_title = result['title'].encode('utf-8')
				stream_title = cleantitle.getsearch(stream_title)
				if cleanmovie in cleantitle.get(stream_title): 
					self.zen_url.append([stream_url,stream_title])		
					print ("ALLUC r3", self.zen_url)
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
            if not alluc_status == 'true': raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            cleanmovie = cleantitle.get(title)
            data['season'], data['episode'] = season, episode
            year = data['year']
            ep_id = int(episode)
            season_id = int(season)
            ep_check =season_id + ep_id
            headers = {'User-Agent': random_agent()}
            search_title = cleantitle.getsearch(title)
            ep_check = "s%02de%02d" % (season_id,ep_id)
            cleanmovie = cleantitle.get(title) + ep_check
            query = "%s+%s" % (urllib.quote_plus(search_title),ep_check)
            print ("ALLUC r1", query)
            query =  self.api_link % (alluc_user, alluc_pw, query)
            if alluc_debrid == 'true': query = query + max_result_string
            else: query = query + '+%23newlinks' + max_result_string
            print ("ALLUC r2", query)
            html = requests.get(query, headers=headers, timeout=15).json()
            for result in html['result']:
				if len(result['hosterurls']) > 1: continue
				if result['extension'] == 'rar': continue
				stream_url = result['hosterurls'][0]['url'].encode('utf-8')
				stream_title = result['title'].encode('utf-8')
				stream_title = cleantitle.getsearch(stream_title)
				
				if cleanmovie in cleantitle.get(stream_title): 
					self.zen_url.append([stream_url,stream_title])		
					print ("ALLUC r3", self.zen_url)		
            return self.zen_url
        except:
            return		
	
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for url, quality in self.zen_url:
				if "1080" in quality: quality = "1080p"
				elif "720" in quality: quality = "HD"
				else: quality = "SD"
				try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
				except: host = 'alluc'
				print ("ALLUC SOURCES", url, quality)
				# if not host in hostDict: continue
				if alluc_debrid == 'true': sources.append({'source': host, 'quality': quality, 'provider': 'Alluc', 'url': url, 'direct': False, 'debridonly': True})
				else: sources.append({'source': host, 'quality': quality, 'provider': 'Alluc', 'url': url, 'direct': False, 'debridonly': False})
			return sources
        except:
            return sources


    def resolve(self, url):
            return url
