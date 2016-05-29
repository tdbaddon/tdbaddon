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
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.base_link = 'http://dayt.se'
        self.search_link = '/forum/search.php?do=process'
        self.forum_link = '/forum/forum.php'


    def movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)

            post = {'titleonly': 1, 'securitytoken': 'guest', 'do': 'process', 'q': title, 'B1': ''}
            post = urllib.urlencode(post)

            r = client.request(query, post=post)
            r = re.sub(r'[^\x00-\x7F]+',' ', r)

            t = cleantitle.get(title)

            r = client.parseDOM(r, 'h3', attrs = {'class': 'searchtitle'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs = {'class': 'title'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i for i in r if any(x in i[1] for x in [' 720p ', ' 1080p '])]
            r = [(i[0], re.findall('(.+?) \((\d{4})\)', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.sub('http.+?//.+?/','/', r)
            url = re.findall('(.+?[?]\d*)', url)[0]
            if not url.startswith('/'): url = '/%s' % url
            if not url.startswith('/forum'): url = '/forum%s' % url
            url += '&%s' % imdb
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            t = cleantitle.get(tvshowtitle)

            url = cache.get(self.dayt_tvcache, 120)

            url = [i[0] for i in url if t == i[1]][0]

            url = re.sub('http.+?//.+?/','/', url)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return


    def dayt_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.forum_link)

            r = client.request(url)
            r = re.sub(r'[^\x00-\x7F]+',' ', r)

            r = client.parseDOM(r, 'span', attrs = {'class': 'sectiontitle'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(re.sub('http.+?//.+?/','/', i[0]), i[1]) for i in r]
            r = [(re.findall('(.+?[?]\d*)', i[0]), i[1]) for i in r]
            r = [(i[0][0], i[1]) for i in r if len(i[0]) > 0]
            r = [('/%s' % i[0] if not i[0].startswith('/') else i[0], i[1]) for i in r]
            r = [('/forum%s' % i[0] if not i[0].startswith('/forum/') else i[0], i[1]) for i in r]
            r = [i for i in r if not i[0].endswith('?4')]
            r = [(i[0], cleantitle.get(i[1])) for i in r]

            return r
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            u = urlparse.urljoin(self.base_link, url)

            t = 'S%02dE%02d' % (int(season), int(episode))
            t = cleantitle.get(t).lower()

            r = client.request(u)
            r = re.sub(r'[^\x00-\x7F]+',' ', r)

            r = client.parseDOM(r, 'h3', attrs = {'class': 'threadtitle'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs={'class': 'title'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t in i[1].lower()][0]

            url = re.sub('http.+?//.+?/','/', r)
            url = re.findall('(.+?[?]\d*)', url)[0]
            if not url.startswith('/'): url = '/%s' % url
            if not url.startswith('/forum'): url = '/forum%s' % url
            url += '&%s' % imdb
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url, imdb = re.findall('(.+?)&(tt\d*)$', url)[0]
            except: imdb = '0'

            u = urlparse.urljoin(self.base_link, url)

            result = client.request(u)
            result = re.sub(r'[^\x00-\x7F]+',' ', result)

            if not imdb == '0' and not imdb in result: raise Exception()

            q = client.parseDOM(result, 'title')[0]

            quality = '1080p' if ' 1080' in q else 'HD'

            r = client.parseDOM(result, 'div', attrs = {'id': '5throw'})[0]
            r = client.parseDOM(r, 'a', ret='href', attrs = {'rel': 'nofollow'})

            links = []

            for url in r:
                try:
                    if 'yadi.sk' in url:
                        url = directstream.yandex(url)
                    elif 'mail.ru' in url:
                        url = directstream.cldmailru(url)
                    else:
                        raise Exception()

                    if url == None: raise Exception()
                    links += [{'source': 'cdn', 'url': url, 'quality': quality, 'direct': False}]
                except:
                    pass


            try:
                r = client.parseDOM(result, 'iframe', ret='src')
                r = [i for i in r if 'pasep' in i][0]

                for i in range(0, 4):
                    try:
                        r = client.request(r)
                        r = re.sub(r'[^\x00-\x7F]+',' ', r)
                        r = client.parseDOM(r, 'iframe', ret='src')[0]
                        if 'google' in r: break
                    except:
                        break

                if not 'google' in r: raise Exception()
                url = directstream.google(r)

                for i in url:
                    try: links += [{'source': 'gvideo', 'url': i['url'], 'quality': i['quality'], 'direct': True}]
                    except: pass
            except:
                pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Dayt', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


