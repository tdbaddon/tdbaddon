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


import re,urllib,urlparse,time,datetime

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.domains = ['myvideolinks.xyz']
        self.base_link = 'http://myvideolinks.xyz'
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

            dt = int(datetime.datetime.now().strftime('%Y%m%d'))

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            hdlr = ['%s' % str(data['year']), '%s' % str(int(data['year'])+1), '%s' % str(int(data['year'])-1)]

            query = re.sub('(\\\|/|:|;|\*|\?|"|\'|<|>|\|)', '', title)
            query = self.search_link % urllib.quote_plus(query)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, 'ul', attrs = {'class': 'posts'})[0]

            result = client.parseDOM(result, 'li')
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs = {'title': '.+?'}), client.parseDOM(i, 'a', attrs = {'rel': 'category tag'})) for i in result]
            result = [(i[0][0], i[1][0], i[0][0], i[2]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            result = [(i[0], i[1], i[2]) for i in result if 'MOVIES' in i[3]]

            result = [(i[0], i[1], re.compile('/(\d{4})/(\d+)/(\d+)/').findall(i[2])) for i in result]
            result = [(i[0], i[1], '%04d%02d%02d' % (int(i[2][0][0]), int(i[2][0][1]), int(i[2][0][2]))) for i in result if len(i[2]) > 0]
            result = [(i[0], i[1], (abs(dt - int(i[2])) < control.integer * 30)) for i in result]
            result = [(i[0], i[1]) for i in result if i[2] == True]

            result = [(i[0], re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s|)(.+|)', '', i[1]), re.compile('[\.|\(|\[|\s](1080p|720p)[\.|\)|\]|\s|]').findall(i[1]), re.compile('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s|]').findall(i[1])) for i in result]
            result = [(i[0], i[1], i[2][0], i[3][0]) for i in result if len(i[2]) > 0 and len(i[3]) > 0]
            result = [(i[0], i[2]) for i in result if cleantitle.get(title) == cleantitle.get(i[1]) and any(x in i[3] for x in hdlr)]

            try: result = [[(i[0], '1080p') for i in result if i[1] == '1080p'][0]] + [[(i[0], 'HD') for i in result if i[1] == '720p'][0]]
            except: result = [[(i[0], 'HD') for i in result if i[1] == '720p'][0]]

            links = []

            for i in result:
                try:
                    result = client.replaceHTMLCodes(i[0])
                    result = client.source(result)
                    result = client.parseDOM(result, 'div', attrs = {'class': 'post_content'})[0]
                    result = re.sub('\s\s+', ' ', result)

                    try:
                        size = re.compile('Size\s*:\s*(.+? [M|G]B) ').findall(result)[-1]
                        div = 1 if size.endswith(' GB') else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        info = '%.2f GB' % size
                    except:
                        info = ''

                    result = client.parseDOM(result, 'ul')[0]
                    result = client.parseDOM(result, 'a', ret='href')
                    for url in result: links.append({'url': url, 'quality': i[1], 'info': info})
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

                    sources.append({'source': host, 'quality': i['quality'], 'provider': 'MVlinks', 'url': url, 'info': i['info'], 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


