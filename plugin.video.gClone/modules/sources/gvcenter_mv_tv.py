# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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
from modules.libraries import cleantitle
from modules.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://www.gearscenter.com'
        self.search_link = '/cartoon_control/gapi-202/?param_10=AIzaSyBsxsynyeeRczZJbxE8tZjnWl_3ALYmODs&param_7=2.0.2&param_8=com.appcenter.sharecartoon&os=android&versionCode=202&op_select=search_catalog&q=%s'
        self.source_link = '/cartoon_control/gapi-202/?param_10=AIzaSyBsxsynyeeRczZJbxE8tZjnWl_3ALYmODs&param_7=2.0.2&param_8=com.appcenter.sharecartoon&os=android&versionCode=202&op_select=films&param_15=0&id_select=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(title)))

            result = client.source(query)
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


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(show)))

            result = client.source(query)
            result = json.loads(result)
            result = result['categories']

            shows = [cleantitle.tv(show), cleantitle.tv(show_alt)]
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            result = [(i['catalog_id'], i['catalog_name'].encode('utf-8')) for i in result]
            result = [(i[0], re.compile('(.+?) [(](.+?)[)]$').findall(i[1])[0]) for i in result]
            result = [(i[0], i[1][0], re.compile('(\d{4})').findall(i[1][1])[0]) for i in result]
            result = [i for i in result if any(x == cleantitle.tv(i[1]) for x in shows)]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

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
                query = urlparse.urljoin(self.base_link, self.source_link % url)

                result = client.source(query)
                result = json.loads(result)
                result = result['films'][0]['film_link']
            else:
                url, ep = re.compile('(.+?)\s(S\d*E\d*)$').findall(url)[0]
                query = urlparse.urljoin(self.base_link, self.source_link % url)

                result = client.source(query)
                result = json.loads(result)
                result = result['films']
                result = [i['film_link'] for i in result if ep in i['film_name'].encode('utf-8').upper()][0]

            result = re.compile('(.+?)#(\d*)#').findall(result)

            try:
                url = [i[0] for i in result if str(i[1]) == '1080'][0]
                sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'GVcenter', 'url': url})
            except:
                pass
            try:
                url = [i[0] for i in result if str(i[1]) == '720'][0]
                sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'GVcenter', 'url': url})
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

