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


import re,urllib,urlparse,json
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy

from BeautifulSoup import BeautifulSoup
from schism_titles import title_match, cleantitle_get, cleantitle_get_2, cleantitle_get_full, cleantitle_geturl, cleantitle_get_simple, cleantitle_query, cleantitle_normalize
from schism_meta import meta_info , meta_quality, meta_gvideo_quality, meta_host
from schism_net import OPEN_URL, OPEN_POST, random_agent, get_sources, get_files
from schism_commons import parseDOM, replaceHTMLCodes

class source:
    def __init__(self):
        self.domains = ['onwatchseries.to']
        self.base_link = 'http://mywatchseries.to'
        # self.base_link = control.setting('watchseries_base')
        # if self.base_link == '' or self.base_link == None:self.base_link = 'http://mywatchseries.to'
		
        self.search_link = 'http://mywatchseries.to/show/search-shows-json'
        self.search_link_2 = self.base_link + "/search/%s"


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            # title = geturl(tvshowtitle)
            check = cleantitle.get(tvshowtitle)

            q = urllib.quote_plus(cleantitle_query(tvshowtitle))
            
            q =  self.search_link_2 % q
            print ("WATCHSERIES SEARCH", q, year)

            r = client.request(q, timeout='10')
            
            
            r = re.compile('<a href="(.+?)" title="(.+?)" target="_blank">(.+?)</a>').findall(r)
            for u,t,t2 in r:
				
				u = u.encode('utf-8')
				t = t.encode('utf-8')
				t2 = t2.encode('utf-8')
				print ("WATCHSERIES SEARCH 2", u,t,t2)
				# if not year in t2:
					# if not year in t: raise Exception()
				if not title_match(cleantitle_get(t), check, amount=0.9) == True: raise Exception()
				print ("WATCHSERIES PASSED", u)
				
				
				url = u.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = client.parseDOM(r, 'li', attrs = {'itemprop': 'episode'})

            t = cleantitle.get(title)

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'itemprop': 'name'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in r]
            r = [(i[0], i[1][0].split('&nbsp;')[-1], i[2]) for i in r if i[1]] + [(i[0], None, i[2]) for i in r if not i[1]]
            r = [(i[0], i[1], i[2][0]) for i in r if i[2]] + [(i[0], i[1], None) for i in r if not i[2]]
            r = [(i[0][0], i[1], i[2]) for i in r if i[0]]

            url = [i for i in r if t == cleantitle.get(i[1]) and premiered == i[2]][:1]
            if not url: url = [i for i in r if t == cleantitle.get(i[1])]
            if len(url) > 1 or not url: url = [i for i in r if premiered == i[2]]
            if len(url) > 1 or not url: raise Exception() 

            url = client.replaceHTMLCodes(url[0][0])
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            links = client.parseDOM(r, 'a', ret='href', attrs = {'target': '.+?'})
            links = [x for y,x in enumerate(links) if x not in links[:y]]

            for i in links:
                print ("WATCHSERIES LINKS", i)
                try:
                    url = i
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['r'][0]
                    url = url.decode('base64')
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url
		
def geturl(title):
    if title == None: return
    title = title.lower()
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', ' ', title).lower()
    title = ' '.join(title.split())
    title = title.replace('/', '_')
    title = title.replace(' ', '_')
    title = title.replace('--', '_')
    print ("WATCHSERIES TITLE", title)
    return title
	
def get_simple(title):
    if title == None: return
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


