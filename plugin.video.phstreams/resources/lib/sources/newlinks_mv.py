# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,json,base64

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.domains = ['newmyvideolink.xyz', 'beta.myvideolinks.xyz']
        self.base_link = 'http://beta.myvideolinks.xyz'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = re.sub('(\\\|/|:|;|\*|\?|"|\'|<|>|\|)', '', data['title'])
            query = self.search_link % urllib.quote_plus(query)
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(data['title'])

            r = client.request(query)
            r = client.parseDOM(r, 'ul', attrs = {'class': 'posts'})[0]

            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs = {'title': '.+?'}), client.parseDOM(i, 'a', attrs = {'rel': 'category tag'})) for i in r]
            r = [(i[0][0], i[1][0], i[2]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            r = [(i[0], i[1]) for i in r if 'MOVIES' in i[2]]

            r = [(i[0], re.sub('(\.|\(|\[|\s)(\d{4}|3D)(\.|\)|\]|\s|)(.+|)', '', i[1]), re.findall('[\.|\(|\[|\s](\d{4}|)([\.|\)|\]|\s|].+)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0][0], i[2][0][1]) for i in r if len(i[2]) > 0]
            r = [(i[0], i[1], i[2], re.split('\.|\(|\)|\[|\]|\s|\-', i[3])) for i in r]

            r = [i for i in r if t == cleantitle.get(i[1]) and data['year'] == i[2]]

            r = [i for i in r if not any(x in i[3] for x in ['HDCAM', 'CAM', 'DVDR', 'DVDRip', 'DVDSCR', 'HDTS', 'TS', '3D'])]
            r = [i for i in r if urlparse.urlparse(self.base_link).netloc in i[0]]

            l = [(i[0], '1080p') for i in r if '1080p' in i[3]]
            l += [(i[0], 'HD') for i in r if '720p' in i[3]]
            l = l[:4]

            links = []

            for i in l:
                try:
                    r = urlparse.urljoin(self.base_link, i[0])
                    r = client.replaceHTMLCodes(r)
                    r = client.request(r)
                    r = client.parseDOM(r, 'div', attrs = {'class': 'post_content'})[0]
                    r = re.sub('\s\s+', ' ', r)

                    try:
                        size = re.findall('Size\s*:\s*(.+? [M|G]B) ', r)[-1]
                        div = 1 if size.endswith(' GB') else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info = '%.2f GB' % size
                    except:
                        info = ''

                    r = client.parseDOM(r, 'ul')[0]
                    r = client.parseDOM(r, 'a', ret='href')
                    for url in r: links.append({'url': url, 'quality': i[1], 'info': info})
                except:
                    pass

            for i in links:
                try:
                    url = i['url']
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': i['quality'], 'provider': 'Newlinks', 'url': url, 'info': i['info'], 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


