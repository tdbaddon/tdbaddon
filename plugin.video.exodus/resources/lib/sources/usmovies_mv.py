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
from resources.lib.modules import cloudflare
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['usmovieshd.com']
        self.base_link = 'http://usmovieshd.com'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTplaWFyaGN2dzgxbSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
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

                t = cleantitle.get(data['title'])
                title = data['title']
                year = data['year']

                query = '%s %s' % (title.replace(':', ' '), year)
                query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

                result = client.source(query)
                result = json.loads(result)['results']

                url = [(i['url'], i['titleNoFormatting']) for i in result]

                url = [i for i in url if '.html' in i[0]]
                url = [(i[0], re.findall('(.+?) (?:\(|)(\d{4})(?:\)|)', i[1])) for i in url]
                url = [(i[0], i[1][0][0], i[1][0][1]) for i in url if len(i[1]) > 0]
                url = [i[0] for i in url if t == cleantitle.get(i[1]) and year == i[2]][0]
                url = client.replaceHTMLCodes(url)


            r = urlparse.urljoin(self.base_link, url)
            result = cloudflare.source(r)

            links = []
            headers = {'Referer': r}
            result = client.parseDOM(result, 'div', attrs = {'class': 'video-embed'})[0]

            try:
                post = re.findall('{link\s*:\s*"([^"]+)', result)[0]
                post = urllib.urlencode({'link': post})

                url = urlparse.urljoin(self.base_link, '/plugins/gkpluginsphp.php')
                url = cloudflare.source(url, post=post, headers=headers)
                url = json.loads(url)['link']
                links += [i['link'] for i in url if 'link' in i]
            except:
                pass

            try:
                url = client.parseDOM(result, 'iframe', ret='.+?')[0]
                url = cloudflare.source(url, headers=headers)
                url = url.replace('\n', '')

                url = re.findall('sources\s*:\s*\[(.+?)\]', url)[0]
                url = re.findall('"file"\s*:\s*"(.+?)"', url)
                links += [i.split()[0] for i in url]
            except:
                pass

            for i in links:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'USmovies', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

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


