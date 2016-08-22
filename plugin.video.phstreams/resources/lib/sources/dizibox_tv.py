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


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['dizibox1.com', 'dizibox.com']
        self.base_link = 'http://www.dizibox.com'
        self.search_link = '/categoryy'


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def dizibox_tvcache(self):
        try:
            result = client.request(self.base_link)

            result = client.parseDOM(result, 'input', {'id': 'filterAllCategories'})[0]
            result = client.parseDOM(result, 'li')
            result = zip(client.parseDOM(result, 'a', ret='href'), client.parseDOM(result, 'a'))
            result = [(re.sub('http.+?//.+?/','/', i[0]), cleantitle.get(i[1])) for i in result]

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

                title = cleantitle.get(data['tvshowtitle'])
                season, episode = '%01d' % int(data['season']), '%01d' % int(data['episode'])
                year = re.findall('(\d{4})', data['premiered'])[0]

                url = cache.get(self.dizibox_tvcache, 120)

                url = [i[0] for i in url if title == i[1]][-1]
                url = urlparse.urljoin(self.base_link, url)

                result = client.request(url)

                if not season == '1':
                    url = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'season-.+?'})
                    url = [i for i in url if '/%s-sezon-' % season in i][0]
                    result = client.request(url)

                url = client.parseDOM(result, 'a', ret='href')
                url = [i for i in url if '%s-sezon-%s-bolum-' % (season, episode) in i][0]

                atr = re.findall('%s.+?\s+(\d{4})' % url, result)[0]
                if not atr == year: raise Exception()


            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url)
            result = re.sub(r'[^\x00-\x7F]+','', result)

            url = re.compile('(<a.*?</a>)', re.DOTALL).findall(result)
            url = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in url]
            url = [(i[0][0], i[1][0]) for i in url if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in url if i[1] == 'Altyazsz'][0]

            result = client.request(url)
            result = re.sub(r'[^\x00-\x7F]+','', result)
 
            headers = {'Referer': url}

            url = client.parseDOM(result, 'span', attrs = {'class': 'object-wrapper'})[0]
            url = client.parseDOM(url, 'iframe', ret='src')[0]
            url = client.replaceHTMLCodes(url)

            url = client.request(url, headers=headers)
            url = client.parseDOM(url, 'param', ret='value', attrs = {'name': 'flashvars'})[0]
            url = urllib.unquote_plus(url)
            url = 'http://ok.ru/video/%s' % urlparse.parse_qs(urlparse.urlparse(url).query)['mid'][0]
            url = directstream.odnoklassniki(url)

            for i in url: sources.append({'source': 'vk', 'quality': i['quality'], 'provider': 'Dizibox', 'url': i['url'], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


