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

import re,urllib,urlparse


from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['drama4u.us']
        self.base_link = 'http://drama4u.us'
        self.search_link = '/search?s='


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
                

                if 'tvshowtitle' in data:

                    url = '%s%s' % (self.search_link, cleantitle.getsearch(data['tvshowtitle']))
                    url = urlparse.urljoin(self.base_link, url)
                    r = client.request(url, timeout='10')
                    t = cleantitle.query(data['tvshowtitle'])
                    ref = client.parseDOM(r, 'a', ret='href', attrs = {'title': t }) [0]
                    
                    url = '%s/%s-ep-%01d/' % (ref, cleantitle.geturl(data['tvshowtitle']), int(data['episode']))
                else:
                    url = '%s/movie/%s-engsub/%s-ep-1/' % (self.base_link, cleantitle.geturl(data['title']), cleantitle.geturl(data['title']))

                url = client.request(url, timeout='10', output='geturl')
                if url == None: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, timeout='10')

            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'iframe', ret='src')
            


            for i in r:
                if 'drama4u' in i or 'k-vid' in i:
                    i = client.request(i, timeout='10')
                    i = re.findall('(https:\W.redirector\..*?)[\'\"]', i)
                    for g in i:
                        g = g.replace("\\", "")
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(g)[0]['quality'], 'language': 'ko', 'url': g, 'direct': True, 'debridonly': False})
                        except: pass

                elif 'ads' in i:
                    pass
                           
                else:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')
                    sources.append({'source': host, 'quality': 'SD', 'language': 'ko', 'url': i, 'direct': False, 'debridonly': False})


            return sources
        except:
            return sources


    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url

