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

import re
import urllib
import urlparse

from resources.lib import resolvers
from ashock.modules import client
from ashock.modules import logger
from ashock.modules import cleantitle


class source:
    def __init__(self):
        self.base_link_1 = 'http://www.desi-tashan.ms'
        self.base_link_2 = 'http://www.desitashan.me'
        self.base_link_3 = 'http://www.desitashan.me'

        self.search_link = '/feed/?s=%s+Watch&submit=Search'

        self.srcs = []

    def tvshow(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowtitle

    def episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):

        query = {'imdb': imdb, 'title': title}
        query = urllib.urlencode(query)

        #query = '%s %s' % (imdb, title)
        #query = self.search_link % (urllib.quote_plus(query))
        ep_url = query
        if ep_url :
            return ep_url

    def sources(self, url):
        try:
            logger.debug('SOURCES URL %s' % url, __name__)
            quality = ''
            srcs = []

            result = ''

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = '%s %s' % (data['imdb'], data['title'])
            url = self.search_link % (urllib.quote_plus(url))

            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try: result = client.request(base_link + '/' + url)
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','').replace('\t','')

            items = client.parseDOM(result, 'item')

            for item in items :
                title = client.parseDOM(item, 'title')[0]
                title = title.replace('Video Watch Online', '')
                title = cleantitle.get(title)
                ctitle = cleantitle.get('%s %s' % (data['imdb'], data['title']))
                if title == ctitle :
                    links = client.parseDOM(item, 'p', attrs={'style':'text-align: center;'})
                    for link in links:
                        if 'span' in link:
                            if 'HD' in link:
                                quality = 'HD'
                            else:
                                quality = 'SD'
                            continue
                        urls = client.parseDOM(link, 'a', ret='href')
                        if len(urls) > 0 :
                            for i in range(0, len(urls)) :
                                urls[i] = client.urlRewrite(urls[i])
                            host = client.host(urls[0])
                            url = "##".join(urls)
                            srcs.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'DesiTashan','url':url, 'direct':False})
                            urls = []

            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        try:
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
                url = links
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False