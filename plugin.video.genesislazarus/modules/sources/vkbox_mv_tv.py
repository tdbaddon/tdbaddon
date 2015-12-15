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


import zipfile
import urllib2
import urlparse
import json
import StringIO
from modules.libraries import client
from modules.resolvers import vk


class source:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = '/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.movie_link = '/api/serials/get_movie_data/?id=%s'
        self.show_link = '/api/serials/es?id=%s'
        self.episode_link = '/api/serials/e/?h=%s&u=%01d&y=%01d'
        self.vk_link = 'http://vk.com/video_ext.php?oid=%s&id=%s&hash=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.data_link)
            data = urllib2.urlopen(query).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.moviedata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.movie_link % result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = urlparse.urljoin(self.base_link, self.data_link)
            data = urllib2.urlopen(query).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.tvdata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.show_link % result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = url.rsplit('id=', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            headers = {'User-Agent': 'android-async-http/1.4.1 (http://loopj.com/android-async-http)'}

            par = urlparse.parse_qs(urlparse.urlparse(url).query)
            try: num = int(par['h'][0]) + int(par['u'][0]) + int(par['y'][0])
            except: num = int(par['id'][0]) + 537

            result = client.source(url, headers=headers)
            result = json.loads(result)
            try: result = result['langs']
            except: pass
            i = [i for i in result if i['lang'] in ['en', '']][0]

            url = (str(int(i['apple']) + num), str(int(i['google']) + num), i['microsoft'])
            url = vk.resolve(self.vk_link % url)

            for i in url: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url

