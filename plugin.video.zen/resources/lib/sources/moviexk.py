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
from resources.lib.modules import control, client
from resources.lib.modules import cleantitle
from resources.lib.modules.common import  random_agent
import requests
from BeautifulSoup import BeautifulSoup
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full
from schism_net import OPEN_URL
class source:
    def __init__(self):
        self.base_link = 'http://moviexk.com'
        self.search_link = '/search/%s+%s'
		
    def movie(self, imdb, title, year):
        self.zen_url = []	
        try:
            query = self.search_link % (urllib.quote_plus(title),year)
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = cleantitle.get(title)
            html = BeautifulSoup(OPEN_URL(query, mobile=True).content)
           
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
					r_title = re.sub('^(watch movies)|(watch movie)|(watch)', '', r_title.lower())
					if cleaned_title in cleantitle.get(r_title):
						redirect = OPEN_URL(r_href, mobile=True).content
						try:
							r_url_trailer = re.search('<dd>[Tt]railer</dd>', redirect)
							if r_url_trailer: continue
						except:
							pass
						try:
							p = client.parseDOM(redirect, 'div', attrs = {'class': 'btn-groups.+?'})
							r = client.parseDOM(p, 'a', ret='href')[0]
							r_url = r.encode('utf-8')
							print ("MOVIEXK PLAY BUTTON 1", r_url)
							url =r_url
							return url
						except:
							p = client.parseDOM(redirect, 'div', attrs = {'id': 'servers'})
							r = client.parseDOM(p, 'li')
							r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
							r = [i[0] for i in r]
							r = r[0]
							r_url = r.encode('utf-8')
							print ("MOVIEXK PLAY BUTTON 2", r_url)
							url =r_url
							return url
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
            html = BeautifulSoup(OPEN_URL(query, mobile=True).content)
            containers = html.findAll('div', attrs={'class': 'name'})
            for container in containers:
                # print ("MOVIEXK r1", container)
                r_href = container.findAll('a')[0]["href"]
                r_href = r_href.encode('utf-8')
                # print ("MOVIEXK r2", r_href)
                r_title = re.findall('</span>(.*?)</a>', str(container))[0]
                # print ("MOVIEXK r3", r_title)
                r_title = r_title.encode('utf-8')

                r_title = re.sub('^(watch movies)|(watch movie)|(watch)', '', r_title.lower())
                # print ("MOVIEXK RESULTS", r_title, r_href)
                if cleaned_title in cleantitle.get(r_title):
						redirect = OPEN_URL(r_href, mobile=True).text
						try:
							r_url_trailer = re.search('<dd>[Tt]railer</dd>', redirect)
							if r_url_trailer: continue
						except:
							pass
						try:
							p = client.parseDOM(redirect, 'div', attrs = {'class': 'btn-groups.+?'})
							r_url = client.parseDOM(p, 'a', ret='href')[0]
							print ("MOVIEXK PLAY BUTTON 1", r_url)
							url = '%s?season=%01d&episode=%01d' % (r_url.encode('utf-8'), int(season), int(episode))
							return url
						except:
							p = client.parseDOM(redirect, 'div', attrs = {'id': 'servers'})
							r = client.parseDOM(p, 'li')
							r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
							r = [i[0] for i in r]
							r = r[0]
							r_url = r.encode('utf-8')
							print ("MOVIEXK PLAY BUTTON 2", r)
							url = '%s?season=%01d&episode=%01d' % (r_url, int(season), int(episode))
							return url
        except:
            return		
			
			
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            f = urlparse.urljoin(self.base_link, url)
            print("MOVIEXK SOURCES", f)
            url = f.rsplit('?', 1)[0]
            direct = url
            print("MOVIEXK SOURCES 2", url)
            r = OPEN_URL(url, mobile=True).content
            # print("MOVIEXK SOURCES 3", r)
            p = client.parseDOM(r, 'div', attrs = {'id': 'servers'})

            if not p:
                p = client.parseDOM(r, 'div', attrs = {'class': 'btn-groups.+?'})
                p = client.parseDOM(p, 'a', ret='href')[0]

                p = OPEN_URL(p, mobile=True).content
                p = client.parseDOM(p, 'div', attrs = {'id': 'servers'})

            servers = client.parseDOM(p, 'li')

            links = []
            try:
                s = urlparse.parse_qs(urlparse.urlparse(f).query)['season'][0]
                e = urlparse.parse_qs(urlparse.urlparse(f).query)['episode'][0]
                check_ep =  ["e%02d" % (int(e)), "s%02d%02d" % (int(s), int(e)), "ep%02d" % (int(e))]
                check_s = ["-season-%02d-" % (int(s)), "-season-%01d-" % (int(s))]
                for items in servers:
					h = client.parseDOM(items, 'a', ret='href')[0]
					h = h.encode('utf-8')
					t = client.parseDOM(items, 'a', ret='title')[0]
					clean_ep_title = cleantitle.get(t.encode('utf-8'))
					if any(value in clean_ep_title for value in check_ep) and  any(value in h for value in check_s) :
							links.append(h)			
										

            except:
				links.append(direct)
					
						

            for u in links:
                try:
                    url = OPEN_URL(u, mobile=True).content
                    url = client.parseDOM(url, 'source', ret='src')
                    url = [i.strip().split()[0] for i in url]
                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': google_tag(i), 'provider': 'Moviexk', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
            return url
