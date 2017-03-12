# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import datetime
import json
import random
import urllib
import urlparse

from ashock.modules import client
from ashock.modules import control
from ashock.modules import logger
from ashock.modules import cleantitle


class source:
    def __init__(self):
        self.base_link_1 = 'http://erosnow.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/search/movies?q=%s&start=0&rows=20&cc=US'
        self.info_link = '/catalog/movie/%s/cc=US'
        self.login_link = 'https://erosnow.com/secured/dologin'
        self.now = datetime.datetime.now()
        self.user = control.setting('eros.user')
        self.password = control.setting('eros.pwd')
        self.srcs = []

    def movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            self.login()
            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link,query)

            result = client.request(query)

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

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            srcs = []

            if url == None: return srcs

            self.login()
            #url = urlparse.urljoin(self.base_link_1, url)
            url = 'http://erosnow.com/profiles/1000218?platform=2&q=auto'
            try: result = client.request(url)
            except: result = ''

            result = json.loads(result)

            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def login(self):
        try :
            post = {'el':self.user, 'pw':self.password, 'mobile':'', 'callingcode':'', 'type':'json', 'fbid':''}
            h = {'Referer':self.base_link_1,
                 'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'}

            result = client.request(self.login_link, post=urllib.urlencode(post), close=False)

            result = json.loads(result)

            t = result['success']
        except:
            pass

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        try:
            post = {'el':self.user, 'pw':self.password, 'mobile':'', 'callingcode':'', 'type':'json', 'fbid':''}
            h = {'Referer':self.base_link}

            result = client.request(self.login_link, post=urllib.urlencode(post))

            result = json.loads(result)

            t = result['success']
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return [url]
        except:
            return False