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

from resources.lib.modules import cleantitle
from resources.lib.modules import cloudflare
from resources.lib.modules import client
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.domains = ['watch1080p.com', 'sefilmdk.com']
        self.base_link = 'http://watch1080p.com'
        self.search_link = '/search.php?q=%s&limit=1'
        self.site_link = '/sitemap.xml'
        self.watch_link = '/watch/%s/'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def watch1080_moviecache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.site_link)
            result = cloudflare.source(url)
            result = client.parseDOM(result, 'loc')
            result = [re.sub('http.+?//.+?/','/', i) for i in result]
            return result
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources


            if not str(url).startswith('http'):
                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['title'] ; year = str(data['year'])
                years = ['(%s)' % year, '( %s)' % year, '(%s )' % year, '( %s )' % year]

                match = title.replace('-', '').replace(':', '').replace('\'', '39').replace(' ', '-').replace('--', '-').lower()
                match = '/%s_' % match


                url = cache.get(self.watch1080_moviecache, 120)
                if url == None: url = []
                url = [i for i in url if match in i]

                if len(url) == 0:
                    url = self.search_link % urllib.quote_plus(title)
                    url = urlparse.urljoin(self.base_link, url)
                    url = cloudflare.source(url)
                    url = re.sub(r'[^\x00-\x7F]+', '', url)
                    url = client.parseDOM(url, 'a', ret='href')
                    url = [i for i in url if match in i]

                url = urlparse.urljoin(self.base_link, url[0])


                url = cloudflare.source(url)
                url = re.sub(r'[^\x00-\x7F]+', '', url)

                atr = client.parseDOM(url, 'span', attrs = {'itemprop': 'title'})
                atr = [i for i in atr if any(x in i for x in years)][0]

                atr = client.parseDOM(url, 'div', attrs = {'class': 'mif'})
                atr = atr[0] if len(atr) > 0 else ''
                if '/film-coming-soon' in atr: raise Exception()

                url = client.parseDOM(url, 'a', ret='href', attrs = {'class': '[^"]*btn_watch_detail[^"]*'})
                url = urlparse.urljoin(self.base_link, url[0])



            result = cloudflare.source(url)
            result = re.sub(r'[^\x00-\x7F]+', '', result)

            result = client.parseDOM(result, 'div', attrs = {'class': 'server'})[0]
            result = result.split('"svname"')
            result = [(zip(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')), i) for i in result]
            result = [i for i in result if len(i[0]) > 0]
            result = [[(x[0], x[1], i[1]) for x in i[0]] for i in result]
            result = sum(result, [])

            result = [(i[0], re.sub('[^0-9]', '', i[1].strip().split(' ')[-1]), i[2].split(':')[0].split('>')[-1].strip()) for i in result]
            result = [(i[0], '720', i[2]) if i[1] == '' else (i[0], i[1], i[2]) for i in result]

            result = [i for i in result if '1080' in i[1] or '720' in i[1]]
            result = [('%s?quality=1080P' % i[0], '1080p', i[2]) if '1080' in i[1] else ('%s?quality=720P' % i[0], 'HD', i[2]) for i in result]

            links = []
            links += [{'source': 'gvideo', 'quality': i[1], 'url': i[0], 'direct': True} for i in result if i[2] in ['Server 1', 'Server 2', 'Server 3']]
            links += [{'source': 'cdn', 'quality': i[1], 'url': i[0], 'direct': True} for i in result if i[2] in ['Server 15']]
            links += [{'source': 'cdn', 'quality': i[1], 'url': i[0], 'direct': False} for i in result if i[2] in ['Server 6', 'Server 8', 'Server 9', 'Server 11', 'Server 16', 'Backup 1']]
            links += [{'source': 'openload.co', 'quality': i[1], 'url': i[0], 'direct': False} for i in result if i[2] in ['Backup 2']]

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Watch1080', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            try: quality = urlparse.parse_qs(urlparse.urlparse(url).query)['quality'][0]
            except: quality = '1080P'
            quality = re.sub('[^0-9]', '', quality)

            url = urlparse.urljoin(self.base_link, url)
            url = url.rsplit('?', 1)[0]

            result = cloudflare.request(url)

            url = client.parseDOM(result, 'div', attrs = {'class': 'player'})[0]
            url = client.parseDOM(url, 'iframe', ret='src')[0]

            result = cloudflare.request(url)

            replace = re.findall("\.replace\('(.*?)'.+?'(.*?)'\)", result)
            for i in replace:
                try: result = result.replace(i[0], i[1])
                except: pass

            count = len(re.findall('window\.atob', result))
            result = re.compile("window\.atob[\([]+'([^']+)").findall(result)[0]
            for i in xrange(count):
                try: result = base64.decodestring(result)
                except: pass

            url = client.parseDOM(result, 'iframe', ret='src')
            if len(url) > 0: return url[0]

            link = []
            link += re.compile('''<source[^>]+src=["']([^'"]+)[^>]+res=['"]([^'"]+)''').findall(result)
            link += re.compile('''\?url=(.+?)["'].+?["'](.+?)["']''').findall(result)

            url = [i for i in link if i[1] == quality]
            if len(url) > 0: url = url[0][0]
            else: url = link[0][0]
            url = url.split()[0]

            return url
        except:
            return


