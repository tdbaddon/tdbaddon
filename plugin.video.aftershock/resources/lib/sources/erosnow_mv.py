# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

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


import re,urllib,urlparse,random, datetime, json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://erosnow.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/search/movies?q=%s&start=0&rows=20&cc=US'
        self.info_link = '/catalog/movie/%s/cc=US'
        self.login_link = 'https://erosnow.com/secured/dologin'
        self.now = datetime.datetime.now()
        self.user = control.setting('eros_user')
        self.password = control.setting('eros_pwd')
        self.list = []

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            self.login()
            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link,query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = json.loads(result)

            result = result['rows']

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = cleantitle.movie(item['title'])
                if title == searchTitle:
                    url = self.info_link % item['asset_id']
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('%s SOURCES URL %s' % (self.__class__, url))
        try:
            quality = ''
            sources = []

            if url == None: return sources

            self.login()
            #url = urlparse.urljoin(self.base_link_1, url)
            url = 'http://erosnow.com/profiles/1000218?platform=2&q=auto'
            try: result = client.source(url)
            except: result = ''

            result = json.loads(result)

            #try :
            #     sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'Hotstar', 'url': url, 'direct':True})
            #except:
            #    client.printException('')
            #    pass
            logger.debug('%s SOURCES [%s]' % (__name__,sources))
            return sources
        except:
            return sources

    def login(self):
        try :
            post = {'el':self.user, 'pw':self.password, 'mobile':'', 'callingcode':'', 'type':'json', 'fbid':''}
            h = {'Referer':self.base_link_1}

            result = client.source(self.login_link, post=urllib.urlencode(post), close=False)

            result = json.loads(result)

            t = result['success']
        except:
            pass

    def resolve(self, url, resolverList):
        logger.debug('%s ORIGINAL URL [%s]' % (__name__, url))
        try:
            post = {'el':self.user, 'pw':self.password, 'mobile':'', 'callingcode':'', 'type':'json', 'fbid':''}
            h = {'Referer':self.base_link}

            result = client.source(self.login_link, post=urllib.urlencode(post))

            result = json.loads(result)

            t = result['success']
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return [url]
        except:
            return False