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

import re,urllib,urlparse,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['ikshow.net']
        self.base_link = 'http://ikshow.net'

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

                url = '%s/shows/%s/episode-%01d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['episode']))

                url = client.request(url, timeout='10', output='geturl')
                if url == None: raise Exception()

            else:
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, timeout='10')

            r = client.request(url, timeout='10')
            links = client.parseDOM(r, 'iframe', ret='src')

            for link in links:
                if 'vidnow' in link:
                    r = client.request(link, timeout='10')
                    r = re.findall('(https:.*?(openload|redirector).*?)[\'\"]', r)

                    for i in r:
                        if 'openload' in i:
                            try: sources.append({'source': 'openload', 'quality': 'SD', 'language': 'ko', 'url': i[0], 'direct': False, 'debridonly': False})
                            except: pass
                        elif 'google' in i:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'ko', 'url': i[0], 'direct': True, 'debridonly': False})
                            except: pass
                        else: pass
                else: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url


