# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 lambda

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
from resources.lib.modules import cloudflare
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.domains = ['tunemovie.is']
        self.base_link = 'http://tunemovie.is'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTo5bGprdnZqMng0aSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            query = '%s %s' % (title.replace(':', ' '), year)
            query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

            result = client.source(query)
            result = json.loads(result)['results']

            title = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            r = [(i['url'], i['titleNoFormatting']) for i in result]
            r = [(i[0], re.compile('(^Watch Full "|^Watch |)(.+? [(]\d{4}[)])').findall(i[1])) for i in r]
            r = [(i[0], i[1][0][-1]) for i in r if len(i[1]) > 0]
            r += [(i['url'], i['richSnippet']['breadcrumb']['title']) for i in result if 'richSnippet' in i and 'breadcrumb' in i['richSnippet'] and 'title' in i['richSnippet']['breadcrumb']]
            result = [i for i in r if title == cleantitle.get(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]
            result = urllib.unquote_plus(result)

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

            result = cloudflare.source(url)

            links = client.parseDOM(result, 'div', attrs = {'class': 'server_line.+?'})

            for link in links:
                try:
                    host = client.parseDOM(link, 'p', attrs = {'class': 'server_servername'})[0]
                    host = host.strip().lower().split(' ')[-1]

                    url = client.parseDOM(link, 'a', ret='href')[0]
                    url = client.replaceHTMLCodes(url)
                    url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    if 'google' in host:
                        url = cloudflare.source(url)
                        url = base64.b64decode(re.compile('decode\("(.+?)"').findall(url)[0])
                        url = re.compile('proxy\.link=([^"&]+)').findall(url)[0]
                        url = url.split('*', 1)[-1]
                        url = self._gkdecrypt(base64.b64decode('Q05WTmhPSjlXM1BmeFd0UEtiOGg='), url)
                        url = directstream.google(url)
                        for i in url: sources.append({'source': 'gvideo', 'quality': i['quality'], 'provider': 'Tunemovie', 'url': i['url'], 'direct': True, 'debridonly': False})

                    elif 'openload' in host:
                        sources.append({'source': 'openload.co', 'quality': 'HD', 'provider': 'Tunemovie', 'url': url, 'direct': False, 'debridonly': False})

                    #elif 'videomega' in host:
                        #sources.append({'source': 'videomega.tv', 'quality': 'HD', 'provider': 'Tunemovie', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if not urlparse.urlparse(url).netloc in self.base_link:
                url = client.request(url, output='geturl')
                if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
                else: url = url.replace('https://', 'http://')

            else:
                result = cloudflare.request(url)
                url = client.parseDOM(result, 'iframe', ret='src')[0]

            return url
        except:
            return


