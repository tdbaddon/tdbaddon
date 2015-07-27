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


import re
import urllib
import urlparse
import json
import base64
from modules.libraries import cleantitle
from modules.libraries import pyaes
from modules.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://playboxhd.com'
        self.search_link = '/api/box?type=search&os=Android&v=2.0.1&k=0&keyword=%s'
        self.detail_link = '/api/box?type=detail&os=Android&v=2.0.1&k=0&id=%s'
        self.stream_link = '/api/box?type=stream&os=Android&v=2.0.1&k=0&id=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = json.loads(result)
            result = result['data']['films']

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(i['id'], i['title'].encode('utf-8')) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])][:2]
            result = [(i[0], self.base_link + self.detail_link % i[0]) for i in result]
            result = [(i[0], client.source(i[1])) for i in result]
            result = [(i[0], json.loads(i[1])['data']['state']) for i in result]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = str(result)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = self.search_link % (urllib.quote_plus(show))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = json.loads(result)
            result = result['data']['films']

            shows = [cleantitle.tv(show), cleantitle.tv(show_alt)]
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            result = [(i['id'], i['title'].encode('utf-8')) for i in result]
            result = [i for i in result if any(x == cleantitle.tv(i[1]) for x in shows)][:2]
            result = [(i[0], self.base_link + self.detail_link % i[0]) for i in result]
            result = [(i[0], client.source(i[1])) for i in result]
            result = [(i[0], json.loads(i[1])['data']['state']) for i in result]
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

            content = re.compile('(.+?)\sS\d*E\d*$').findall(url)

            if len(content) == 0:
                query = urlparse.urljoin(self.base_link, self.detail_link % url)

                result = client.source(query)
                result = json.loads(result)
                result = result['data']['chapters'][0]['id']
            else:
                url, s, e = re.compile('(.+?)\sS(\d*)E(\d*)$').findall(url)[0]
                ep = 'S%02dE%03d' % (int(s), int(e))

                query = urlparse.urljoin(self.base_link, self.detail_link % url)

                result = client.source(query)
                result = json.loads(result)
                result = result['data']['chapters']
                result = [i['id'] for i in result if ep in i['title'].encode('utf-8').upper()][0]

            url = urlparse.urljoin(self.base_link, self.stream_link % result)
            result = client.source(url)
            result = json.loads(result)['data']

            for i in result:
                try:
                    if not i['server'] == 'ggvideo': raise Exception()

                    quality = i['quality'].replace('720p', 'HD')
                    if not quality in ['1080p', 'HD']: quality = 'SD'

                    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(base64.urlsafe_b64decode('cXdlcnR5dWlvcGFzZGZnaGprbHp4YzEyMzQ1Njc4OTA='), '\0' * 16))
                    url = base64.decodestring(i['stream'])
                    url = decrypter.feed(url) + decrypter.feed()

                    sources.append({'source': 'GVideo', 'quality': quality, 'provider': 'PlayBox', 'url': url})
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

