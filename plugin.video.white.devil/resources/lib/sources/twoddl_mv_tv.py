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


import re,urllib,urlparse,datetime

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.domains = ['2ddl.cc']
        self.base_link = 'http://2ddl.cc'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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

            if debrid.status() == False: raise Exception()

            dt = int(datetime.datetime.now().strftime('%Y%m%d'))
            mt = {'jan':'1', 'feb':'2', 'mar':'3', 'apr':'4', 'may':'5', 'jun':'6', 'jul':'7', 'aug':'8', 'sep':'9', 'oct':'10', 'nov':'11', 'dec':'12'}

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = ['S%02dE%02d' % (int(data['season']), int(data['episode']))] if 'tvshowtitle' in data else ['%s' % str(data['year'])]

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            query = self.search_link % urllib.quote_plus(query)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = client.parseDOM(result, 'div', attrs = {'id': 'post-\d+'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'a', attrs = {'title': 'posting time.+?'}), client.parseDOM(i, 'a', attrs = {'rel': 'category tag'})) for i in result]
            result = [(i[0][0], i[1][0], i[2][0], i[3]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0 and len(i[3]) > 0]

            result = [(i[0], i[1], i[2], i[3]) for i in result if 'Single Link' in i[3]]
            result = [(i[0], i[1], i[2], i[3]) for i in result if any(x in ['720P', '1080P', 'TV 1080p', 'TV 720p'] for x in i[3])]
            if not 'tvshowtitle' in data: result = [(i[0], i[3], i[1], i[2]) for i in result if 'Movies' in i[3] and not any(x in ['BDRip', 'Cam', 'CAMRip', 'HDCAM', 'HDScr', 'DVDR', 'DVDRip', 'DVDScr', 'R6', 'Telesync', 'Extras', '3D'] for x in i[3])]
            else: result = [(i[0], i[3], i[1], i[2]) for i in result if 'TV Shows' in i[3] and not 'TV Packs' in i[3]]

            result = [(i[0], i[1], i[2], re.findall('(\w+).+?(\d+).+?(\d*)', i[3])) for i in result]
            result = [(i[0], i[1], i[2], '%04d%02d%02d' % (int('20' + i[3][0][2][-2:]), int(mt[i[3][0][0][:3].lower()]), int(i[3][0][1]))) for i in result if len(i[3]) > 0]
            result = [(i[0], i[1], i[2], (abs(dt - int(i[3])) < control.integer * 10)) for i in result]
            result = [(i[0], i[1], i[2]) for i in result if i[3] == True]

            result = [(i[0], i[1], i[2].upper()) for i in result]
            result = [(i[0], i[1], re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s|)(.+|)', '', i[2]), re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s|]', i[2])) for i in result]
            result = [(i[0], i[1], i[2]) for i in result if len(i[3]) > 0 and any(x in i[3][0] for x in hdlr)]
            result = [(i[0], i[1]) for i in result if cleantitle.get(title) == cleantitle.get(i[2])]


            r = [(i[0], '1080p') for i in result if any(x in ['1080P', 'TV 1080p'] for x in i[1])][:2]
            r += [(i[0], 'HD') for i in result if any(x in ['720P', 'TV 720p'] for x in i[1])][:2]
            result = r

            links = []

            for i in result:
                try:
                    r = client.replaceHTMLCodes(i[0])
                    r = client.source(r)
                    r = client.parseDOM(r, 'p')
                    r = [(client.parseDOM(x, 'a', attrs = {'rel': 'nofollow'}), client.parseDOM(x, 'strong')) for x in r]
                    r = [(x[0], len(x[0]), len(x[1])) for x in r]
                    r = [x[0] for x in r if len(x[0]) > 0 and x[1] == x[2]]
                    r = sum(r, [])
                    for url in r: links.append({'url': url, 'quality': i[1]})
                except:
                    pass

            for i in links:
                try:
                    url = i['url']
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostprDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': i['quality'], 'provider': 'twoDDL', 'url': url, 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


