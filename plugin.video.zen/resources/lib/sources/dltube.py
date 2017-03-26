# -*- coding: utf-8 -*-

'''
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


import re,urllib,urlparse,json
from BeautifulSoup import BeautifulSoup
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
# if not debridstatus == 'true': raise Exception()
from schism_commons import quality_tag, google_tag, parseDOM, replaceHTMLCodes ,cleantitle_get, cleantitle_get_2, cleantitle_query, get_size, cleantitle_get_full

class source:
    def __init__(self):
        self.domains = ['mydownloadtube.com']
        self.base_link = 'http://www.mydownloadtube.com'
        self.search_link = '/search/search_val?language=English%20-%20UK&term='
        self.download_link = '/movies/add_download'

    def movie(self, imdb, title, year):
        try:
            if not debridstatus == 'true': raise Exception()

            t = cleantitle.get(title)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            query = self.search_link + urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query, headers=headers)
            r = json.loads(r)

            r = [i for i in r if 'category' in i and 'movie' in i['category'].lower()]
            r = [(i['url'], i['label']) for i in r if 'label' in i and 'url' in i]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year in i[1]][0]
            # print("DLTUBE MOVIES", r)
            # url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(r)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not debridstatus == 'true': raise Exception()

            url = urlparse.urljoin(self.base_link, url)
            # print("DLTUBE MOVIES SOURCES", url)
            r = client.request(url)

            movie_id = re.findall('<input type="hidden" value="(\d+)" name="movie_id"', r)[0]
			
            # print("DLTUBE MOVIES ID", movie_id)
            download_link = urlparse.urljoin(self.base_link, self.download_link)
            p = urllib.urlencode({'movie': movie_id.encode('utf-8')})
            r = client.request(download_link, post=p, XHR=True)
            r = BeautifulSoup(r)
            r = r.findAll('p')
            ext = ['.avi','.mkv','.mov','.mp4','.xvid','.divx']
            locDict = [(i.rsplit('.', 1)[0], i) for i in hostprDict if not i in ext]
			
            # print ("DLTUBE MOVIES SOURCES 2", r)			
            for link in r:
                try:
                    link = str(link)
                    host = re.findall('Downloads-Server(.+?)(?:\'|\")\)', link)[0]
                    # print ("DLTUBE MOVIES SOURCES 3", locDict, host.lower())
					
                    # host = host.strip().lower().split()[-1]
                    if 'fichier' in host.lower(): host = '1fichier'
				
                    host = [x[1] for x in locDict if x[0].lower() in host.lower()][0]
                    # print ("DLTUBE MOVIES SOURCES 4", host)	                   
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    if not any(value in host for value in hostprDict): raise Exception()
                    url = client.parseDOM(link, 'a', ret='href')[0]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    r = client.parseDOM(link, 'a')[0]

                    fmt = r.strip().lower().split()

                    if '1080p' in fmt: quality = '1080p'
                    elif '720p' in fmt: quality = 'HD'

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) [M|G]B)', r)[-1]
                        div = 1 if size.endswith(' GB') else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info = '%.2f GB' % size
                    except:
                        info = ''

                    sources.append({'source': host, 'quality': quality, 'provider': 'DLTube', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            return url
        except:
            return


