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
        self.base_link = 'http://www.gearscenter.com'
        self.config_link = '/gold-server/gapiandroid206/?option=config'
        self.search_link = '/gold-server/gapiandroid206/?option=search&q=%s&page=1&total=0&block=0'
        self.content_link = '/gold-server/gapiandroid206/?option=content&id=%s&sid=%s'
        self.source_link = '/gold-server/gapiandroid206/?option=filmcontent&id=%s&cataid=%s&sid=%s'

        self.last_call = 0
        self.__request(self.base_link + self.config_link)

        self.vc = urllib.quote_plus(str(206).encode('utf-8'))
        self.vn = urllib.quote_plus('2.0.6')
        self.pn = hashlib.md5('com.gamena.funboxhd').hexdigest().upper()
        self.film_key = hashlib.md5(self.vc + self.vn + self.pn).hexdigest()[0:16]


    def __request(self, url, post=None):
        try:
            now = str(int(time.time()))

            headers = {'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)'}

            url += self.__extra(now)

            while time.time() - self.last_call < 2: time.sleep(.25)

            result = client.source(url, post=post, headers=headers)

            self.last_call = time.time()

            key = hashlib.md5(now).hexdigest()[0:16]

            result = json.loads(result)

            result = self.__decrypt(key, base64.b64decode(result['data']))
            return result
        except:
            return


    def __extra(self, now):
        ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
        COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
        EXTRA_URL = ('&os=android&version=2.0.6&versioncode=206&param_1=EA2C2D2240456D78B2CCE8148B10A674'
             '&deviceid=%s&param_3=0685257cd8bc8108d550c4e948aebf2f&param_4=%s'
             '&param_5=%s&token=%s&time=%s&devicename=Google-Nexus-%s-%s'
             '&sm=%s&si=%s&extra_1=%s&extra_2=%s&extra_3=%s')
        URL_KEY = base64.b64decode('RzRtM2wwZnRfczNjcjN0MA==')

        token = hashlib.md5(now).hexdigest()
        build = random.choice(ANDROID_LEVELS.keys())
        country = random.choice(COUNTRIES)
        device_id = '000000000000000'
        sm = hashlib.md5(str(random.randint(0, 1000))).hexdigest()
        si = hashlib.md5('catoon_206').hexdigest()
        ex_1 = hashlib.md5(str(now) + sm).hexdigest()
        ex_2 = urllib.quote_plus(hashlib.md5(str(now) + si).hexdigest())
        ex_3 = sm[0:5] + hashlib.md5(device_id).hexdigest()[2:7]
        ex_3 = urllib.quote_plus(base64.encodestring(self.__encrypt(URL_KEY, ex_3)))
        url = EXTRA_URL % (device_id, country, country.lower(), token, now, build, ANDROID_LEVELS[build], sm, si, ex_1, ex_2, ex_3)
        return url


    def __decrypt(self, key, txt):
        try:
            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
            txt = decrypter.feed(txt) + decrypter.feed()
            return txt
        except:
            return


    def __encrypt(self, key, txt):
        try:
            encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationECB(key))
            txt = encrypter.feed(txt) + encrypter.feed()
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
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8'), str(i['type_film'])) for i in result]
            result = [i for i in result if i[2] == '0']
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
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8'), str(i['type_film'])) for i in result]
            result = [i for i in result if i[2] == '1']
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
            sid = hashlib.md5('content%scthd' % id).hexdigest()
            query = urlparse.urljoin(self.base_link, self.content_link % (id, sid))

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
                    sid = hashlib.md5('%s%scthd' % (l, id)).hexdigest()

                    url = urlparse.urljoin(self.base_link, self.source_link % (l, id, sid))

                    result = self.__request(url)
                    result = json.loads(result)

                    url = result['videos']
                    url = [self.__decrypt(self.film_key, base64.b64decode(i['film_link'])) for i in url]

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


