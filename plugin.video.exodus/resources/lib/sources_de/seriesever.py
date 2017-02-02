# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Viper2k4

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

import re, urllib, urlparse, json, base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import control

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['seriesever.net']
        self.base_link = 'http://seriesever.net'
        self.search_link = 'service/search?q=%s'
        self.part_link = 'service/get_video_part'

        self.login_link = 'service/login'
        self.user = control.setting('seriesever.user')
        self.password = control.setting('seriesever.pass')


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
        try:
            url = self.__search(tvshowtitle)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(localtvshowtitle)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            return url + '/staffel-%s-episode-%s.html' % (season, episode)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            cookie = self.__get_premium_cookie()

            r = client.request(url, mobile=True, cookie=cookie)

            query = urlparse.urljoin(self.base_link, self.part_link)
            id = re.compile('var\s*video_id\s*=\s*"(\d+)"').findall(r)[0]

            p = client.parseDOM(r, 'a', attrs={'class': 'changePart', 'data-part': '\d+p'}, ret='data-part')

            for i in p:
                r = urllib.urlencode({'video_id': id, 'part_name': i, 'page': '0'})
                r = client.request(query, cookie=cookie, mobile=True, XHR=True, post=r , referer=url)

                try:
                    r = json.loads(r)
                    r = r.get('part', {})

                    s = r.get('source', '')
                    url = r.get('code', '')

                    if s == 'url' and 'http' not in url:
                        url = self.__decode_hash(url)
                    elif s == 'other':
                        url = client.parseDOM(url, 'iframe', ret='src')
                        if len(url) < 1: continue
                        url = url[0]
                        if '/old/seframer.php' in url: url = self.__get_old_url(url)

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict and not 'google' in host: continue

                    if i in ['720p', 'HD']: quali = 'HD'
                    elif i in ['1080p', '1440p']: quali = i
                    elif i in ['2160p']: quali = '4K'
                    else: quali = 'SD'

                    if 'google' in url: host = 'gvideo'; direct = True; urls = directstream.google(url)
                    elif 'ok.ru' in url: host = 'vk'; direct = True; urls = directstream.odnoklassniki(url)
                    elif 'vk.com' in url: host = 'vk'; direct = True; urls = directstream.vk(url)
                    else: direct = False; urls = [{'quality': quali, 'url': url}]

                    for i in urls: sources.append({'source': host, 'quality': i['quality'], 'language': 'de', 'url': i['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        if directstream.googletag(url): url = directstream.googlepass(url)
        return url

    def __search(self, title):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query, XHR=True)

            if r and r.startswith('{'): r = '[%s]' % r

            r = json.loads(r)
            r = [(i['url'], i['name']) for i in r if 'name' in i and 'url' in i]
            r = [i[0] for i in r if cleantitle.get(i[1]) == t][0]

            url = re.findall('(?://.+?|)(/.+).html?', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            url = url.replace('serien/', '')
            return url
        except:
            return

    def __decode_hash(self, hash):
        hash = hash.replace("!BeF", "R")
        hash = hash.replace("@jkp", "Ax")
        hash += '=' * (-len(hash) % 4)
        try: return base64.b64decode(hash)
        except: return

    def __get_old_url(self, url):
        try:
            r = client.request(url, mobile=True)
            url = re.findall('url="(.*?)"', r)

            if len(url) == 0:
                url = client.parseDOM(r, 'iframe', ret='src')[0]
                if "play/se.php" in url:
                    r = client.request(url, mobile=True)
                    return self.__decode_hash(re.findall('link:"(.*?)"', r)[0])
            else:
                return url[0]
        except:
            return

    def __get_premium_cookie(self):
        try:
            if (self.user == '' or self.password == ''): raise Exception()
            login = urlparse.urljoin(self.base_link, self.login_link)
            post = urllib.urlencode({'username': self.user, 'password': self.password})
            cookie = client.request(login, mobile=True, post=post, XHR=True, output='cookie')
            r = client.request(urlparse.urljoin(self.base_link, 'api'), mobile=True, cookie=cookie)
            return cookie if r == '1' else ''
        except:
            return ''


