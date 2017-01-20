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
from resources.lib.modules import client
import requests
s = requests.session()

class source:
    def __init__(self):
        self.domains = ['yesmovies.to']
        self.base_link = 'https://yesmovies.to'
        self.info_link = 'https://yesmovies.to/'
        self.playlist = '/ajax/v2_get_sources/%s.html?hash=%s'
        self.key3 = 'ctiw4zlrn09tau7kqvc153uo'	
        self.key2 = '8qhfm9oyq1ux'
        self.key = 'xwh38if39ucx'
        self.session = requests.Session()
		
    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
			self.zen_url = []
			
			cleanmovie = cleantitle.get(title)
			title = cleantitle.getsearch(title)
			query = "/search/%s.html" % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})
			for links in r:
				# print ("YMOVIES links", links)
				url = client.parseDOM(links, 'a', ret='href')[0]
				r_title = client.parseDOM(links, 'a', ret='title')[0]
				r_title = r_title.encode('utf-8')
				if not cleanmovie == cleantitle.get(r_title): continue
				infolink = client.request(url)
				# print ("YMOVIES REQUEST", url)
				match_year = re.search('<strong>Release:</strong>\s*(\d{4})</p>', infolink)
				match_year = match_year.group(1)
				# print ("YMOVIES match_year", match_year)
				if year in match_year:
					
					playurl = re.findall('<a class="mod-btn mod-btn-watch" href="([^"]+)"', infolink)[0]
					playurl = playurl.encode('utf-8')
					referer = "%s" % playurl
					# print ("YMOVIES MATCH FOUND", referer)
					
					
					headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}
					epurl = s.get(referer, headers=headers,verify=False).content
					i_d = re.findall(r'id: "(.*?)"', epurl, re.I|re.DOTALL)[0]
					server = re.findall(r'server: "(.*?)"', epurl, re.I|re.DOTALL)[0]
					type = re.findall(r'type: "(.*?)"', epurl, re.I|re.DOTALL)[0]
					episode_id = re.findall(r'episode_id: "(.*?)"', epurl, re.I|re.DOTALL)[0]
					
# ################### COOKIE ###################									   
					headers_cookie = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
							   'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}	
					getc = re.findall(r'<img title=.*?src="(.*?)"' , str(epurl), re.I|re.DOTALL)[0]
					# print ("YMOVIES MOVIES COOKIE getc", getc, headers_cookie)
					cookie = s.get(getc,headers=headers_cookie).cookies.get_dict()
					# print ("YMOVIES MOVIES COOKIE" , cookie)
					for i in cookie: cookie =  i + '=' + cookie[i]				
# ################### COOKIE HERE ###################							
					
# ################### AUTH HERE ###################
					token = self.__get_token()
					coookie = self.key + episode_id + self.key2 + '=%s' % token
					cookie = '%s; %s' %(cookie,coookie)
					a = episode_id + self.key3
					b = token
					hash_id = self.__uncensored(a, b)
					hash_id = urllib.quote(hash_id).encode('utf8')
					request_url =  self.base_link + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id)		
					self.zen_url.append([request_url,cookie,referer])
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
			headers = {}
			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			year = data['year'] 
			title = cleantitle.getsearch(title)
			cleanmovie = cleantitle.get(title)
			data['season'], data['episode'] = season, episode
			seasoncheck = "season%s" % season
			checktitle = cleanmovie + seasoncheck
			self.zen_url = []
			showlist = []
			query = "/search/%s.html" % (urllib.quote_plus(title))
			query = urlparse.urljoin(self.base_link, query)
			link = client.request(query)
			r = client.parseDOM(link, 'div', attrs = {'class': 'ml-item'})
			for links in r:
				season_url = client.parseDOM(links, 'a', ret='href')[0]
				title = client.parseDOM(links, 'a', ret='title')[0]
				title = title.encode('utf-8')
				season_url = season_url.encode('utf-8')
				title = cleantitle.get(title)
				# print "YMOVIES check URLS %s %s %s %s" % (seasoncheck, season_url, cleanmovie, title)
				if checktitle in title:
						# print "YMOVIES PASSED %s" % (season_url) 
						showlist.append(season_url)
								
			for seasonlist in showlist:	
				# print ('YMOVIES TV' , seasonlist)
				headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}
				mylink = client.request(seasonlist)
				referer = re.findall('<a class="mod-btn mod-btn-watch" href="([^"]+)"', mylink)[0]
				
				# print ('YMOVIES REFERER' , referer)
				epurl = s.get(referer, headers=headers,verify=False).content
				i_d = re.findall(r'id: "(.*?)"', epurl, re.I|re.DOTALL)[0]
				server = re.findall(r'server: "(.*?)"', epurl, re.I|re.DOTALL)[0]
				type = re.findall(r'type: "(.*?)"', epurl, re.I|re.DOTALL)[0]
				episode_id = re.findall(r'episode_id: "(.*?)"', epurl, re.I|re.DOTALL)[0]
				request_url = self.base_link + '/ajax/v3_movie_get_episodes/' + i_d + '/' + server + '/' + episode_id + '/' + type + '.html'
				headers = {'Referer': referer,
							   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
							   'X-Requested-With':'XMLHttpRequest'}
							   
							   
							   
# ################### COOKIE ###################									   
				headers_cookie = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
						   'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}	
				getc = re.findall(r'<img title=.*?src="(.*?)"' , str(epurl), re.I|re.DOTALL)[0]
				# print ("YMOVIES COOKIE getc", getc, headers_cookie)
				cookie = get_cookie(getc,referer,self.session)
				# print ("YMOVIES COOKIE" , cookie)
				for i in cookie: cookie =  i + '=' + cookie[i]				
# ################### COOKIE HERE ###################						
				
				
				episodelink = client.request(request_url, headers=headers)
				pattern = 'episodes-server-%s"(.+?)/ul>' % server
				match = re.findall(pattern, episodelink, re.DOTALL)[0]
				# print "YMOVIES EPISODELINK %s" % match
				blocks = re.compile('<li(.+?)/li>',re.DOTALL).findall(match)
				for fragment in blocks:
					epnumber = re.findall('title="Episode\s+(\d+):', fragment)[0]
					episode = "%02d" % (int(episode))
					epnumber = "%02d" % (int(epnumber))
					# print "EPISODE NUMBER %s %s" % (epnumber, episode)
					if epnumber == episode:
						epid = re.findall('id="episode-(\d+)"', fragment)[0]
						episode_id = epid
						# print "EPISODE NNUMBER Passed %s %s" % (epnumber, episode)
						# print ("YMOVIES REQUEST", episode_id)
						
# ################### AUTH HERE ###################
						token = self.__get_token()
						coookie = self.key + episode_id + self.key2 + '=%s' % token
						
						cookie = '%s; %s' %(cookie,coookie)
						a = episode_id + self.key3
						b = token
						hash_id = self.__uncensored(a, b)
						hash_id = urllib.quote(hash_id).encode('utf8')
						
						request_url =  self.base_link + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id)						
						# print ("YMOVIES REQUEST", request_url)
						self.zen_url.append([request_url,cookie,referer])
						# print ("YMOVIES SELFURL", self.zen_url)

			return self.zen_url
        except:
            return		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []
			for movielink,cookie,referer in self.zen_url:
				# print ("YMOVIES SOURCES", movielink, cookies, referer)
				headers = {'Referer': referer,
							   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
							   'X-Requested-With':'XMLHttpRequest'}
				result = client.request(movielink, headers=headers, cookie=cookie)
				result = json.loads(result)
				# print ("YMOVIES SOURCE PLAYLIST", result)
				links = result['playlist'][0]['sources']
				for item in links:
					videoq = item['label']
					url = item['file']
					if "1080" in videoq: quality = "1080p" 
					elif "720" in videoq: quality = "HD"
					else: quality = "SD"
					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')
					sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Ymovies', 'url': url, 'direct': True, 'debridonly': False})
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
		
		
    def __get_token(self):
        return ''.join(random.sample(string.digits + string.ascii_lowercase, 6))
    
    def __uncensored(self, a, b):
        c = ''
        i = 0
        for i, d in enumerate(a):
            e = b[i % len(b) - 1]
            d = int(self.__jav(d) + self.__jav(e))
            c += chr(d)
    
        return base64.b64encode(c)
    
    def __jav(self, a):
        b = str(a)
        code = ord(b[0])
        if 0xD800 <= code and code <= 0xDBFF:
            c = code
            if len(b) == 1:
                return code
            d = ord(b[1])
            return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000
    
        if 0xDC00 <= code and code <= 0xDFFF:
            return code
        return code
		
		
def get_cookie(url, referer, session):
    headers = {'Accept'         : 'image/webp,image/*,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-US,en;q=0.8',
               'Referer'        : referer,
               'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
               }
    request = session.get(url, headers=headers)
    cookie = request.cookies.get_dict()
    newcookie = ""
    for i in cookie:
        newcookie = i + '=' + cookie[i]
    return newcookie