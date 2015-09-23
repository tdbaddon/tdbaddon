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


import re,urllib,urlparse

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://moviefarsi2.com'
        self.search_link = '?s=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'article', attrs = {'id': 'post-\d*'})
            result = [i for i in result if imdb in i][0]
            result = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'more-link'})[0]

            url = re.compile('//.+?/(\d*)').findall(result)[0]
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_link % urllib.quote_plus(tvshowtitle)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'article', attrs = {'id': 'post-\d*'})

            match = [i for i in result if imdb in i]

            if len(match) == 0:
                tvshowtitle = cleantitle.tv(tvshowtitle)
                years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

                result = [i for i in result if any(x in i for x in years)]
                result = [(client.parseDOM(i, 'a', ret='title'), i) for i in result]
                result = [(i[0][0], i[1]) for i in result if len(i[0]) > 0]
                result = [(re.sub(r'[^\x00-\x7F]+',' ', i[0]).strip(), i[1]) for i in result]

                match = [i[1] for i in result if tvshowtitle == cleantitle.tv(i[0])]

            result = match[0]
            result = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'more-link'})[0]

            url = re.compile('//.+?/(\d*)').findall(result)[0]
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
                url = urlparse.urljoin(self.base_link, url) + '/'

                result = client.source(url)

                links = re.compile('src=".+?/downloadicon.png".+?href="(.+?)"').findall(result)

                for i in links:
                    try:
                        url = client.replaceHTMLCodes(i)
                        url = url.encode('utf-8')

                        if not url.endswith(('mp4', 'mkv')): raise Exception()

                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', i)
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-|\_', fmt)
                        fmt = [x.lower() for x in fmt]

                        if '1080p' in fmt: quality = '1080p'
                        elif '720p' in fmt or 'hd' in fmt: quality = 'HD'
                        else: quality = 'SD'

                        if '3d' in fmt: info = '3D'
                        else: info = ''

                        sources.append({'source': 'Moviefarsi', 'quality': quality, 'provider': 'Moviefarsi', 'url': url, 'info': info})
                    except:
                        pass


            else:
                url, season, episode = re.compile('(.+?)\sS(\d*)E(\d*)$').findall(url)[0]

                url = urlparse.urljoin(self.base_link, url) + '/'

                result = client.source(url)

                match = re.compile('<span style *= *"color: *#ff0000;">.+?<span style *= *"color: *#333333;" *> *(\d*) *</span>.+?<span style *= *"color: *#333333;" *> *(\d*) *</span>').findall(result)[0]

                if int(season) > int(match[1]): raise Exception()
                if int(season) == int(match[1]) and int(episode) > int(match[0]): raise Exception()

                links = re.compile('src=".+?/folderserial.png".+?href="(.+?)".+? (\d*p) ').findall(result)

                for i in links:
                    try:
                        if not 'S%02d' % int(season) in (i[0].upper()).split('/'): raise Exception()

                        url = '%s?S%02dE%02d' % (i[0], int(season), int(episode))
                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        if i[1] == '1080p': quality = '1080p'
                        elif i[1] == '720p': quality = 'HD'
                        else: quality = 'SD'

                        sources.append({'source': 'Moviefarsi', 'quality': quality, 'provider': 'Moviefarsi', 'url': url})
                    except:
                        pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            content = re.compile('(.+?)\?S\d*E\d*$').findall(url)

            if len(content) == 0: return url

            url, season, episode = re.compile('(.+?)\?S(\d*)E(\d*)$').findall(url)[0]

            match = ['S%sE%s' % (season, episode), 'S%s E%s' % (season, episode)]

            result = client.source(url)
            result = client.parseDOM(result, 'a', ret='href')
            result = [i for i in result if any(x in i for x in match)][0]

            url = '%s/%s' % (url, result)
            return url
        except:
            return


