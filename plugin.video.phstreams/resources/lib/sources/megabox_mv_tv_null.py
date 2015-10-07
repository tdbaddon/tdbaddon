# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda
    Copyright (C) 2015 tknorris

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


import re,sys,urllib,urlparse,json,time,random,hashlib,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import pyaes
from resources.lib.libraries import client
from resources.lib.resolvers import googleplus


class source:
    def __init__(self):
        self.base_link = 'http://www.megaboxhd.com'
        self.config_link = '/megaboxhd/android_api_100/index.php?select=config'
        self.search_link = '/megaboxhd/android_api_100/index.php?select=search&q=%s&page=1&total=0&total=0'
        self.content_link = '/megaboxhd/android_api_100/index.php?select=detail&id=%s'
        self.source_link = '/megaboxhd/android_api_100/index.php?select=stream&id=%s&cataid=%s'

        self.film_key = base64.b64decode('OTBlOTdkYzUyMWNmMDIwZQ==')
        self.data_key = base64.b64decode('MzkzNmI5MGU5N2RjNTIxYw==')


    def __request(self, url, post=None):
        try:
            headers = {'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)'}

            url += self.__extra()

            result = client.source(url, post=post, headers=headers)

            result = self.__decrypt(self.data_key, base64.b64decode(result))
            return result
        except:
            self.__config()


    def __config(self):
        try:
            headers = {'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)'}

            url = self.base_link + self.config_link + self.__extra()

            client.source(url, headers=headers)
        except:
            return


    def __extra(self):
        ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
        COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
        EXTRA_URL = ('&os=android&version=1.0.0&versioncode=100&extra_1=26EB5D5D9DC010629E21A8A6076D86CF&'
             'deviceid=%s&extra_3=6de97ad519993642d91de9b577f75b36&extra_4=%s'
             '&extra_5=%s&token=%s&time=%s&devicename=Google-Nexus-%s-%s')

        now = str(int(time.time()))
        build = random.choice(ANDROID_LEVELS.keys())
        device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
        country = random.choice(COUNTRIES)
        url = EXTRA_URL % (device_id, country, country.lower(), hashlib.md5(now).hexdigest(), now, build, ANDROID_LEVELS[build])
        return url


    def __decrypt(self, key, txt):
        try:
            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
            txt = decrypter.feed(txt) + decrypter.feed()
            return txt
        except:
            return


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(title)))

            result = self.__request(query)
            result = json.loads(result)
            result = result['categories']

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8')) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = str(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(tvshowtitle)))

            result = self.__request(query)
            result = json.loads(result)
            result = result['categories']

            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8')) for i in result]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = str(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            id = re.compile('(\d*)').findall(url)[0]
            query = urlparse.urljoin(self.base_link, self.content_link % (id))

            result = self.__request(query)
            result = json.loads(result)
            result = result['listvideos']

            content = re.compile('(.+?)\sS\d*E\d*$').findall(url)

            if len(content) == 0:
                links = [i['film_id'] for i in result]
            else:
                ep = re.compile('.+?\s(S\d*E\d*)$').findall(url)[0]
                links = [i['film_id'] for i in result if ep in i['film_name'].encode('utf-8').upper()]

            for l in links[:3]:
                try:
                    url = urlparse.urljoin(self.base_link, self.source_link % (l, id))

                    result = self.__request(url)
                    result = json.loads(result)

                    url = result['videos']
                    url = [self.__decrypt(self.film_key, base64.b64decode(i['film_link'])) for i in url]

                    url = '#'.join(url)
                    url = url.split('#')
                    url = [i for i in url if 'http' in i and 'google' in i]
                    url = [googleplus.tag(i)[0] for i in url]

                    for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'MegaBox', 'url': i['url']})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


