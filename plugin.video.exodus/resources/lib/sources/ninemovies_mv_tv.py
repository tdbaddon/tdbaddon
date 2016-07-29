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


class source:
    def __init__(self):
        self.domains = ['fmovies.to']
        self.base_link = 'http://fmovies.to'
        self.info_link = '/ajax/episode/info?id=%s&update=0&film=%s'
        self.search_link = '/ajax/film/search?keyword=%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % urllib.quote_plus(title)

            r = client.request(url, headers=headers)

            r = json.loads(r)['html']
            r = client.parseDOM(r, 'div', attrs = {'class': 'info'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'span', attrs = {'class': '.+?'})) for i in r]
            r = [(i[0][0], i[1][0], [x.strip() for x in i[2] if x.strip().isdigit() and len(x.strip()) == 4]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            t = cleantitle.get(data['tvshowtitle'])
            year = re.findall('(\d{4})', premiered)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            season = '%01d' % int(season)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % urllib.quote_plus('%s %s' % (data['tvshowtitle'], season))

            r = client.request(url, headers=headers)

            r = json.loads(r)['html']
            r = client.parseDOM(r, 'div', attrs = {'class': 'info'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'span', attrs = {'class': '.+?'})) for i in r]
            r = [(i[0][0], i[1][0], [x.strip() for x in i[2] if x.strip().isdigit() and len(x.strip()) == 4]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]

            r = [(i[0], re.findall('(.+?) (\d*)$', i[1]), i[2]) for i in r]
            r = [(i[0], i[1][0][0], i[2], i[1][0][1]) for i in r if len(i[1]) > 0]

            r = [i for i in r if t == cleantitle.get(i[1]) and season == i[3]]
            r = [i[0] for i in r if any(x in i[2] for x in years)][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url += '?episode=%01d' % int(episode)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            r = client.request(url)

            try: quality = client.parseDOM(r, 'span', attrs = {'class': 'quality'})[0].lower()
            except: quality = 'hd'
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd' or 'hd ' in quality: quality = 'HD'
            else: quality = 'SD'

            category = client.parseDOM(r, 'div', ret='data-id', attrs = {'id': '.+?'})[0]

            servers = client.parseDOM(r, 'div', attrs = {'id': 'servers'})
            servers = client.parseDOM(r, 'div', attrs = {'data-type': 'iframe'})
            servers = zip(client.parseDOM(servers, 'a', ret='data-id'), client.parseDOM(servers, 'a'))
            servers = [(i[0], re.findall('(\d+)', i[1])) for i in servers]
            servers = [(i[0], ''.join(i[1][:1])) for i in servers]

            if not episode == None:
                servers = [i for i in servers if '%01d' % int(i[1]) == '%01d' % int(episode)]

            servers = [i[0] for i in servers]


            for s in servers:
                try:
                    headers = { 'X-Requested-With': 'XMLHttpRequest', 'Age': '130', 'Referer': urlparse.urljoin(url, s) }

                    url = urlparse.urljoin(self.base_link, self.info_link % (s, category))

                    url = client.request(url, headers=headers)
                    url = json.loads(url)['target']

                    if 'openload.' in url: host = 'openload.co'
                    elif 'videomega.' in url: host = 'videomega.tv'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Ninemovies', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


