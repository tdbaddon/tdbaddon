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
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full


class source:
    def __init__(self):
        self.domains = ['onwatchseries.to']
        self.base_link = control.setting('watchseries_base')
        if self.base_link == '' or self.base_link == None:self.base_link = 'http://onwatchseries.to'
		
        self.search_link = 'http://onwatchseries.to/show/search-shows-json'
        self.search_link_2 = 'http://onwatchseries.to/search/%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            t = cleantitle.get(tvshowtitle)

            q = urllib.quote_plus(cleantitle.query(tvshowtitle))
            p = urllib.urlencode({'term': q})
            h = {'X-Requested-With': 'XMLHttpRequest'}

            r = client.request(self.search_link, post=p, headers=h)
            try: r = json.loads(r)
            except: r = None
            print ("WATCHSERIES RESULT", r)
            r = [(i['seo_url'], i['value'], i['label']) for i in r if 'value' in i and 'label' in i and 'seo_url' in i]

            r = [(i[0], i[1], re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            print ("WATCHSERIES RESULT 4", r, year)
            url = r[0][0]
            print ("WATCHSERIES RESULT 5", r, url)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass

            url = url.strip('/').split('/')[-1]
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = '%s/serie/%s' % (self.base_link, url)

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


