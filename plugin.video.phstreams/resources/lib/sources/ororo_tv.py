# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import re,urllib,urlparse,base64,datetime

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://ororo.tv'
        self.headers = {'User-Agent' : 'Mozilla/%s' % datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            result = client.source(self.base_link, headers=self.headers)
            if not "'index show'" in result:
                cookie = client.source(self.sign_link, headers=self.headers, post=self.key_link, output='cookie')
                result = client.source(self.base_link, headers=self.headers, cookie=cookie)

            result = client.parseDOM(result, 'div', attrs = {'class': 'index show'})
            result = [(client.parseDOM(i, 'a', attrs = {'class': 'name'})[0], client.parseDOM(i, 'span', attrs = {'class': 'value'})[0], client.parseDOM(i, 'a', ret='href')[0]) for i in result]

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if any(x in i[1] for x in years)]
            result = [i[2] for i in result if tvshowtitle == cleantitle.tv(i[0])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url, headers=self.headers)
            if not 'menu season-tabs' in result:
                cookie = client.source(self.sign_link, headers=self.headers, post=self.key_link, output='cookie')
                result = client.source(url, headers=self.headers, cookie=cookie)

            result = client.parseDOM(result, 'a', ret='data-href', attrs = {'href': '#%01d-%01d' % (int(season), int(episode))})[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            match = re.compile('(.+?)#(\d*)-(\d*)$').findall(url)
            if len(match) > 0:
                url = self.get_episode(match[0][0], '', '', '', '', match[0][1], match[0][2])

            url = urlparse.urljoin(self.base_link, url)
            sources.append({'source': 'Ororo', 'quality': 'SD', 'provider': 'Ororo', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            result = client.request(url, headers=self.headers)
            if not 'my_video' in result:
                cookie = client.request(self.sign_link, headers=self.headers, post=self.key_link, output='cookie')
                result = client.request(url, headers=self.headers, cookie=cookie)

            url = None
            try: url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video/webm'})[0]
            except: pass
            try: url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video/mp4'})[0]
            except: pass

            if url == None: return
            url = urlparse.urljoin(self.base_link, url)

            url = '%s|User-Agent=%s&Cookie=%s' % (url, urllib.quote_plus(self.headers['User-Agent']), urllib.quote_plus('video=true'))

            return url
        except:
            return

