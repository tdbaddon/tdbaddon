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


import re,urllib,urlparse,hashlib,random,string,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['pmovies.to', 'watch5s.to', 'cmovieshd.com']
        self.base_link = 'http://pmovies.to'
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNzg1NzgzNTUyMDY0NTYwNTIyOTphZ3h6a3R0b3R5YyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.search_link = '/ajax/suggest_search'
        self.info_link = '/ajax/movie_qtip/%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = '%s %s' % (title, year)
            q = self.search_link_2.decode('base64') % urllib.quote_plus(q)

            r = client.request(q)
            r = json.loads(r)['results']
            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0], re.findall('(?:^Watch Movies |^Watch |)(.+?)(?:\(|)(\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i for i in r if '/movie/' in i[0] and not '/watch/' in i[0]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

        try:
            t = cleantitle.get(title)

            h = {'X-Requested-With': 'XMLHttpRequest'}

            q = urllib.urlencode({'keyword': title[:-1]})

            u = urlparse.urljoin(self.base_link, self.search_link)

            r = client.request(u, post=q, headers=h)

            r = json.loads(r)['content']
            r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))
            r = [i[0] for i in r if cleantitle.get(t) == cleantitle.get(i[1])][:2]
            r = [(i, i.strip('/').split('/')[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.pmovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass
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
            title = data['tvshowtitle']
            season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            year = re.findall('(\d{4})', premiered)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]

            r = cache.get(self.pmovies_info_season, 720, title, season)
            r = [(i[0], re.findall('(.+?) - season (\d+)$', i[1].lower())) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and season == '%01d' % int(i[2])][:2]
            r = [(i, i.strip('/').split('/')[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.pmovies_info, 9000, i[1])
                    if not y in years: raise Exception()
                    return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                except:
                    pass
        except:
            return


    def pmovies_info_season(self, title, season):
        try:
            h = {'X-Requested-With': 'XMLHttpRequest'}

            q = urllib.urlencode({'keyword': '%s - Season %s' % (title, season)})

            u = urlparse.urljoin(self.base_link, self.search_link)

            r = client.request(u, post=q, headers=h)
            r = json.loads(r)['content']
            r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            return r
        except:
            return


    def pmovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = client.request(u % url)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jt-info jt-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            url = urlparse.urljoin(self.base_link, url)
            url = path = re.sub('/watch$', '', url.strip('/'))
            url = referer = url + '/watch/'

            '''
            quality = cache.get(self.pmovies_info, 9000, path.strip('/').split('/')[-1])[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'
            '''

            r = client.request(url, referer=referer)

            r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
            r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

            if not episode == None:
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0] for i in r]

            r = [i for i in r if '/server-' in i]

            for u in r:
                try:
                    p = client.request(u, referer=referer, timeout='10')
                    p = re.findall('hash\s*:\s*"([^"]+)', p)[0]
                    t = ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 16))
                    k = hashlib.md5('(*&^%$#@!' + p[46:58]).hexdigest()
                    s = hashlib.md5('!@#$%^&*(' + t).hexdigest()
	
                    stream = 'http://streaming.pmovies.to/videoplayback/%s?key=%s' % (p, s)
                    cookie = '%s=%s' % (k, t)

                    u = client.request(stream, referer=u, cookie=cookie, timeout='10')
                    u = json.loads(u)['playlist'][0]['sources']
                    u = [i['file'] for i in u if 'file' in i]

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Pmovies', 'url': i, 'direct': True, 'debridonly': False})
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


