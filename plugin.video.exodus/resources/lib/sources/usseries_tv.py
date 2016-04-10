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
from resources.lib.modules import cloudflare
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['seriestv.us']
        self.base_link = 'http://seriestv.us'
        self.search_link = '/categoryy'


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
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


    def usseries_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            result = cloudflare.source(url)
            result = client.parseDOM(result, 'div', attrs = {'class': 'tagindex'})[0]
            result = re.findall('href="(.+?)">(.+?)<', result)
            result = [i for i in result if not (i[1].strip()).endswith('(0)')]

            result = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('\s+\(\d+\)$', '', i[1])) for i in result]
            result = [(i[0], i[1], re.findall('(.+?)\s+Season\s+(\d+)$', i[1])) for i in result]
            result = [(i[0], i[2] if len(i[2]) > 0 else [(i[1], '1')]) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1]) for i in result]
            result = [(client.replaceHTMLCodes(i[0]), client.replaceHTMLCodes(i[1]), i[2]) for i in result]
            result = [(i[0], cleantitle.get(i[1]), '%01d' % int(i[2])) for i in result]

            return result
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = cleantitle.get(data['tvshowtitle'])
                season = data['season']
                episode = data['episode']

                year = data['year']
                years = ['%s' % str(int(year)+1), '%s' % str(int(year)-1)]

                url = cache.get(self.usseries_tvcache, 120)

                url = [i[0] for i in url if title == i[1] and season == i[2]][-1]
                url = [i for i in url.split('/') if not i == ''][-1]
                url = '/%s-episode-%01d' % (url.replace('/', ''), int(episode))
                url = urlparse.urljoin(self.base_link, url)


            try:
                result = cloudflare.source(url)
                r = client.parseDOM(result, 'link', ret='href', attrs = {'rel': 'canonical'})[0]
            except:
                url = url.replace('/the-', '/')
                result = cloudflare.source(url)
                r = client.parseDOM(result, 'link', ret='href', attrs = {'rel': 'canonical'})[0]


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
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'USseries', 'url': i, 'direct': True, 'debridonly': False})
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


