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


import re
import sys
import urllib
import urlparse
import json
import time
import random
import hashlib
import base64
from modules.libraries import cleantitle
from modules.libraries import pyaes
from modules.libraries import client
from modules.resolvers import googleplus


class source:
    def __init__(self):
        self.base_link = 'http://www.gearscenter.com'
        self.search_link = '/gold-server/gapiandroid205/?option=search&page=1&total=0&block=0&q=%s'
        self.content_link = '/gold-server/gapiandroid205/?option=content&id=%s'
        self.source_link = '/gold-server/gapiandroid205/?option=filmcontent&cataid=0&id=%s'
        self.data_key = 'M2FiYWFkMjE2NDYzYjc0MQ=='
        self.film_key = 'MmIyYTNkNTNkYzdiZjQyNw=='


    def __extra(self):
        ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
        COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
        EXTRA_URL = ('&os=android&version=2.0.5&versioncode=205&param_1=F2EF57A9374977FD431ECAED984BA7A2&'
             'deviceid=%s&param_3=7326c76a03066b39e2a0b1dc235c351c&param_4=%s'
             '&param_5=%s&token=%s&time=%s&devicename=Google-Nexus-%s-%s')

        now = str(int(time.time()))
        build = random.choice(ANDROID_LEVELS.keys())
        device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
        country = random.choice(COUNTRIES)
        return EXTRA_URL % (device_id, country, country.lower(), hashlib.md5(now).hexdigest(), now, build, ANDROID_LEVELS[build])


    def __decrypt(self, key, txt):
        try:
            key = base64.b64decode(key)
            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
            txt = base64.decodestring(txt)
            txt = decrypter.feed(txt) + decrypter.feed()
            return txt
        except:
            return


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(title)))
            query += self.__extra()

            result = client.source(query)
            result = json.loads(result)
            result = self.__decrypt(self.data_key, result['data'])
            result = json.loads(result)
            result = result['categories']

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8'), str(i['type_film'])) for i in result]
            result = [i for i in result if i[2] == '0']
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = str(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(show)))
            query += self.__extra()

            result = client.source(query)
            result = json.loads(result)
            result = self.__decrypt(self.data_key, result['data'])
            result = json.loads(result)
            result = result['categories']

            shows = [cleantitle.tv(show), cleantitle.tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8'), str(i['type_film'])) for i in result]
            result = [i for i in result if i[2] == '1']
            result = [i for i in result if any(x == cleantitle.tv(i[1]) for x in shows)]
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

            query = re.compile('(\d*)').findall(url)[0]
            query = urlparse.urljoin(self.base_link, self.content_link % query)
            query += self.__extra()

            result = client.source(query)
            result = json.loads(result)
            result = self.__decrypt(self.data_key, result['data'])
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
                    url = urlparse.urljoin(self.base_link, self.source_link % l)
                    url += self.__extra()

                    url = client.source(url)
                    url = json.loads(url)

                    url = self.__decrypt(self.data_key, url['data'])
                    url = json.loads(url)['videos']
                    url = [self.__decrypt(self.film_key, i['film_link']) for i in url]

                    url = '#'.join(url)
                    url = url.split('#')
                    url = [i for i in url if 'http' in i and 'google' in i]
                    url = [googleplus.tag(i)[0] for i in url]

                    for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'GVcenter', 'url': i['url']})
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

