# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,json


from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
# http://search.rlsbb.ru/lib/search526049.php?phrase=avengers+2016&pindex=1&content=true&rand=0.43580461427300077
class source:
    def __init__(self):
        self.domains = ['rlsbb.com']
        self.base_link = 'http://rlsbb.ru'
        self.search_base_link = 'http://search.rlsbb.ru'
        self.search_header_link = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': 'serach_mode=light'}
        self.search_link = '/lib/search526049.php?phrase=%s&pindex=1&content=true'
        self.search_link2 = '/search/%s'


    def movie(self, imdb, title, year):
        try:
            if not debridstatus == 'true': raise Exception()
            self.zen_url = []
            query = cleantitle_query(title)
            cleanmovie = cleantitle_get(title)
            query = "%s+%s" % (urllib.quote_plus(query), year)
            query = self.search_link % query
            query = urlparse.urljoin(self.search_base_link, query)
            r = client.request(query, headers=self.search_header_link, referer=query)
            posts = []
            dupes = []
            print ("RELEASEBB QUERY", r)
			
            try: posts += json.loads(re.findall('({.+?})$', r)[0])['results']
            except: pass			
            for post in posts:
				try:
					name = post['post_title'].encode('utf-8')
					url = post['post_name'].encode('utf-8')
					if url in dupes: raise Exception()
					dupes.append(url)
					print ("RELEASEBB 2", name,url)
					t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)
					
					if not cleanmovie in cleantitle_get(name) or not year in name: raise Exception()
					print ("RELEASEBB 3 PASSED", t)
					content = post['post_content']
					url = [i for i in client.parseDOM(content, 'a', ret='href')]
					
					size = get_size(content)
					quality = quality_tag(name)
					self.zen_url.append([size,quality,url])
				
					
				except:
					pass
            print("RELEASEBB PASSED", self.zen_url)
            return self.zen_url

        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.zen_url = []
            if not debridstatus == 'true': raise Exception()
            if url == None: return
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle_query(title)
            cleanmovie = cleantitle.get(title)
            data['season'], data['episode'] = season, episode
            ep_query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            
            titlecheck = cleanmovie+ep_query.lower()
			
            query = "%s+%s" % (urllib.quote_plus(title), ep_query)
            query = self.search_link % query
            query = urlparse.urljoin(self.search_base_link, query)
            r = client.request(query, headers=self.search_header_link, referer=query)
            posts = []
            dupes = []
            print ("RELEASEBB QUERY", r)
			
            try: posts += json.loads(re.findall('({.+?})$', r)[0])['results']
            except: pass			
            for post in posts:
				try:
					name = post['post_title'].encode('utf-8')
					url = post['post_name'].encode('utf-8')
					if url in dupes: raise Exception()
					dupes.append(url)
					print ("RELEASEBB 2", name,url)
					t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)
					print ("RELEASEBB 3 TV", t)					
					if not titlecheck in cleantitle_get(name): raise Exception()
					print ("RELEASEBB 3 PASSED", t)
					content = post['post_content']
					url = [i for i in client.parseDOM(content, 'a', ret='href')]
					
					size = get_size(content)
					quality = 'getbyurl'
					self.zen_url.append([size,quality,url])
				
					
				except:
					pass
            print("RELEASEBB PASSED", self.zen_url)
            return self.zen_url

        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if not debridstatus == 'true': raise Exception()
            for size, q, urls in self.zen_url:
				for url in urls:
					try:
						print ("RELEASEBB SOURCES", size, q, url)
						url = url.encode('utf-8')
						if q == 'getbyurl': quality = quality_tag(url)
						else: quality = q
						host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
						if not any(value in url for value in hostprDict): raise Exception()
						host = client.replaceHTMLCodes(host)
						host = host.encode('utf-8')
						sources.append({'source': host, 'quality': quality, 'provider': 'Releasebb', 'url': url, 'info': size, 'direct': False, 'debridonly': True})
					except:
						pass
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


