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


import re,urllib,urllib2,urlparse,json,base64,time

from resources.lib.modules import control
from resources.lib.modules import pyaes
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['moviesplanet.is']
        self.base_link = 'http://www.moviesplanet.is'
        self.search_link = '/ajax/search.php'
        self.user = control.setting('moviesplanet.user')
        self.password = control.setting('moviesplanet.pass')


    def movie(self, imdb, title, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)

            post = {'q': title.rsplit(':', 1)[0], 'limit': '100', 'timestamp': int(time.time() * 1000), 'verifiedCheck': ''}
            post = urllib.urlencode(post)

            result = client.source(url, post=post, headers=headers)
            result = json.loads(result)

            title = cleantitle.get(title)

            result = [i for i in result if i['meta'].strip().split(' ')[0].lower() == 'movie']
            result = [i for i in result if title == cleantitle.get(i['title'])][:2]

            if len(result) > 1:
                result = [(i, urlparse.urljoin(self.base_link, i['permalink'])) for i in result]
                result = [(i[0], str(client.source(i[1]))) for i in result]
                result = [(i[0], re.compile('/(tt\d+)').findall(i[1])) for i in result]
                result = [i[0] for i in result if len(i[1]) > 0 and imdb == i[1][0]]

            result = result[0]['permalink']

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = urlparse.urljoin(self.base_link, self.search_link)

            post = {'q': tvshowtitle.rsplit(':', 1)[0], 'limit': '100', 'timestamp': int(time.time() * 1000), 'verifiedCheck': ''}
            post = urllib.urlencode(post)

            result = client.source(url, post=post, headers=headers)
            result = json.loads(result)

            tvshowtitle = cleantitle.get(tvshowtitle)

            result = [i for i in result if i['meta'].strip().split(' ')[0].lower() == 'tv']
            result = [i for i in result if tvshowtitle == cleantitle.get(i['title'])][:2]

            if len(result) > 1:
                result = [(i, urlparse.urljoin(self.base_link, i['permalink'])) for i in result]
                result = [(i[0], str(client.source(i[1]))) for i in result]
                result = [(i[0], re.compile('/(tt\d+)').findall(i[1])) for i in result]
                result = [i[0] for i in result if len(i[1]) > 0 and imdb == i[1][0]]

            result = result[0]['permalink']

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            if url == None: return

            url = '%s/season/%01d/episode/%01d' % (url, int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def _gkdecrypt(self, key, str):
        try:
            key += (24 - len(key)) * '\0'
            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
            str = decrypter.feed(str.decode('hex')) + decrypter.feed()
            str = str.split('\0', 1)[0]
            return str
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if (self.user == '' or self.password == ''): raise Exception()

            class NoRedirection(urllib2.HTTPErrorProcessor):
                def http_response(self, request, response): return response


            headers = {'X-Requested-With': 'XMLHttpRequest'}
            login = urlparse.urljoin(self.base_link, '/login')
            post = {'username': self.user, 'password': self.password, 'action': 'login'}
            post = urllib.urlencode(post)

            cookie = client.source(login, post=post, headers=headers, output='cookie')


            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url, cookie=cookie)

            url = re.compile("embeds\[\d+\]\s*=\s*'([^']+)").findall(result)[0]
            url = client.parseDOM(url, 'iframe', ret='src')[0]
            url = url.replace('https://', 'http://')

            links = []

            try:
                url = re.compile('mplanet\*(.+)').findall(url)[0]
                url = url.rsplit('&')[0]
                dec = self._gkdecrypt(base64.b64decode('MllVcmlZQmhTM2swYU9BY0lmTzQ='), url)
                dec = directstream.google(dec)

                links += [(i['url'], i['quality'], 'gvideo') for i in dec]
            except:
                pass

            try:
                result = client.source(url)

                result = re.compile('sources\s*:\s*\[(.*?)\]', re.DOTALL).findall(result)[0]
                result = re.compile('''['"]*file['"]*\s*:\s*['"]*([^'"]+).*?['"]*label['"]*\s*:\s*['"]*([^'"]+)''', re.DOTALL).findall(result)
            except:
                pass

            try:
                u = result[0][0]
                if not 'download.php' in u and not '.live.' in u: raise Exception()
                o = urllib2.build_opener(NoRedirection)
                o.addheaders = [('User-Agent', client.randomagent()), ('Cookie', cookie)]
                r = o.open(u)
                try: u = r.headers['Location']
                except: pass
                r.close()
                links += [(u, '1080p', 'cdn')]
            except:
                pass
            try:
                u = [(i[0], re.sub('[^0-9]', '', i[1])) for i in result]
                u = [(i[0], i[1]) for i in u if i[1].isdigit()]
                links += [(i[0], '1080p', 'gvideo') for i in u if int(i[1]) >= 1080]
                links += [(i[0], 'HD', 'gvideo') for i in u if 720 <= int(i[1]) < 1080]
                links += [(i[0], 'SD', 'gvideo') for i in u if 480 <= int(i[1]) < 720]
            except:
                pass


            for i in links: sources.append({'source': i[2], 'quality': i[1], 'provider': 'Moviesplanet', 'url': i[0], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            return url
        except:
            return


