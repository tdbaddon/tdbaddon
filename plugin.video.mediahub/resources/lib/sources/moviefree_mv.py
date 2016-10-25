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


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['hdmoviefree.org']
        self.base_link = 'https://www.hdmoviefree.org'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNDk5MjgxMTY0MjUzNzEzMzcwNzp3cGhoaWhsZmZncSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.data_link = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vZXhvZHVzL2luZm8vbW92aWVmcmVlLmRlYg=='
        self.server_link = '/ajax/loadsv/%s'
        self.episode_link = '/ajax/loadep/%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = '%s %s' % (title, year)
            q = base64.b64decode(self.search_link) % urllib.quote_plus(q)

            r = self.moviefree_mvcache(q)
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]

            url = urlparse.urljoin(self.base_link, r)
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = url.encode('utf-8')
            return url
        except:
            return


    def moviefree_mvcache(self, q):
        try:
            r = client.request(q)

            self.data_link = base64.b64decode(self.data_link)

            try: exec(base64.b64decode(client.request(self.data_link)))
            except: pass

            r = json.loads(r)['results']
            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0], re.findall('(?:^Watch |)(.+?)(?: HD |)(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i for i in r if not '/search/' in i[0]]

            return r
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            data_id = client.parseDOM(r, 'img', ret='data-id')[0]
            data_name = client.parseDOM(r, 'img', ret='data-name')[0]

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

            post = {'id': data_id, 'n': data_name}
            post = urllib.urlencode(post)

            url = self.server_link % data_id
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, post=post, headers=headers)

            links = client.parseDOM(r, 'a', ret='data-id')

            for link in links:
                try:
                    url = self.episode_link % link
                    url = urlparse.urljoin(self.base_link, url)

                    post = {'epid': link}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, headers=headers)
                    r = json.loads(r)

                    try: u = client.parseDOM(r['link']['embed'], 'iframe', ret='src')
                    except: u = r['link']['l']

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Moviefree', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

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


