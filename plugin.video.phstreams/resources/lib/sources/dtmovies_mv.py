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
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['dayt.se']
        self.base_link = 'http://dayt.se'


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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = base64.b64decode('aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxNjE2OTU5MjY5NTEyNzQ5NTk0OTpsYnB1dGVqbmxrNCZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM=')
            query = query % urllib.quote_plus('%s %s' % (data['title'].replace(':', ' '), data['year']))

            t = cleantitle.get(data['title'])

            r = client.request(query)
            r = json.loads(r)['results']

            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0], cleantitle.get(i[1]), re.findall('\d{4}', i[1])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if len(i[2]) > 0]
            r = [i[0] for i in r if t == i[1] and data['year'] == i[2]][0]

            u = urlparse.urljoin(self.base_link, r)

            result = client.request(u)
            result = re.sub(r'[^\x00-\x7F]+',' ', result)

            q = client.parseDOM(result, 'title')[0]

            quality = '1080p' if ' 1080' in q else 'HD'

            r = client.parseDOM(result, 'div', attrs = {'id': '5throw'})[0]
            r = client.parseDOM(r, 'a', ret='href', attrs = {'rel': 'nofollow'})

            links = []

            for url in r:
                try:
                    if 'yadi.sk' in url:
                        url = directstream.yandex(url)
                    elif 'mail.ru' in url:
                        url = directstream.cldmailru(url)
                    else:
                        raise Exception()

                    if url == None: raise Exception()
                    links += [{'source': 'cdn', 'url': url, 'quality': quality, 'direct': False}]
                except:
                    pass


            try:
                r = client.parseDOM(result, 'iframe', ret='src')
                r = [i for i in r if 'pasep' in i][0]

                for i in range(0, 4):
                    try:
                        r = client.request(r)
                        r = re.sub(r'[^\x00-\x7F]+',' ', r)
                        r = client.parseDOM(r, 'iframe', ret='src')[0]
                        if 'google' in r: break
                    except:
                        break

                if not 'google' in r: raise Exception()
                url = directstream.google(r)

                for i in url:
                    try: links += [{'source': 'gvideo', 'url': i['url'], 'quality': i['quality'], 'direct': True}]
                    except: pass
            except:
                pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Dtmovies', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


