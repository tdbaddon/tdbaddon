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
from resources.lib.modules import pyaes
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['miradetodo.com.ar']
        self.base_link = 'http://miradetodo.com.ar'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PXBhcnRuZXItcHViLTY1NzkzMDgwNDkzMzkxNzg6NjkyNTk5OTE5NyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            query = '%s %s' % (title.replace(':', ' '), year)
            query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

            result = client.source(query)
            result = json.loads(result)['results']

            title = cleantitle.get(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [(i['url'], i['richSnippet']['metatags']['ogTitle']) for i in result if 'richSnippet' in i and 'metatags' in i['richSnippet'] and 'ogTitle' in i['richSnippet']['metatags']]
            result = [(i[0], re.compile('(.+?) [(](\d{4})[)]').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0].rsplit('(', 1)[-1].replace(')' , ''), i[1][0][1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.get(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            url = urlparse.urljoin(self.base_link, result)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def _gkdecrypt(self, key, str):
        try:
            key += (24 - len(key)) * '\0'
            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
            str = decrypter.feed(str.decode('hex')) + decrypter.feed()
            str = str.split('\0', 1)[0]
            return str
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            links = []

            try:
                try: url = re.compile('proxy\.link=([^"&]+)').findall(result)[0]
                except: url = client.source(re.compile('proxy\.list=([^"&]+)').findall(result)[0])

                url = url.split('*', 1)[-1].rsplit('<')[0]

                dec = self._gkdecrypt(base64.b64decode('aUJocnZjOGdGZENaQWh3V2huUm0='), url)
                if not 'http' in dec: dec = self._gkdecrypt(base64.b64decode('QjZVTUMxUms3VFJBVU56V3hraHI='), url)

                url = directstream.google(dec)

                links += [(i['url'], i['quality']) for i in url]
            except:
                pass

            try:
                url = 'http://miradetodo.com.ar/gkphp/plugins/gkpluginsphp.php'

                post = client.parseDOM(result, 'div', attrs = {'class': 'player.+?'})[0]
                post = post.replace('iframe', 'IFRAME')
                post = client.parseDOM(post, 'IFRAME', ret='.+?')[0]
                post = urlparse.parse_qs(urlparse.urlparse(post).query)

                result = ''
                try: result += client.source(url, post=urllib.urlencode({'link': post['id'][0]}))
                except: pass
                try: result += client.source(url, post=urllib.urlencode({'link': post['id1'][0]}))
                except: pass
                try: result += client.source(url, post=urllib.urlencode({'link': post['id2'][0]}))
                except: pass

                result = re.compile('"?link"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?"').findall(result)
                result = [(i[0].replace('\\/', '/'), i[1])  for i in result]

                links += [(i[0], '1080p') for i in result if int(i[1]) >= 1080]
                links += [(i[0], 'HD') for i in result if 720 <= int(i[1]) < 1080]
                links += [(i[0], 'SD') for i in result if 480 <= int(i[1]) < 720]
                if not 'SD' in [i[1] for i in links]: links += [(i[0], 'SD') for i in result if 360 <= int(i[1]) < 480]
            except:
                pass

            for i in links: sources.append({'source': 'gvideo', 'quality': i[1], 'provider': 'MiraDeTodo', 'url': i[0], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


