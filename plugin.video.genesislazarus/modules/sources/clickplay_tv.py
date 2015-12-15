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


import re
import urllib
import urlparse
import base64
from modules.libraries import cleantitle
from modules.libraries import gkplugins
from modules.libraries import client
from modules.resolvers import googleplus
from modules import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://clickplay.to'
        self.search_link = '/search/%s'
        self.episode_link = '%sseason-%01d/episode-%01d'


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = ' '.join([i for i in show.split() if i not in ['The','the','A','a']])
            query = self.search_link % urllib.quote_plus(query)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')
            result = [(client.parseDOM(i, "span", attrs = { "class": "article-title" }), client.parseDOM(i, "a", ret="href")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if not (len(i[0]) == 0 or len(i[1]) == 0)]

            shows = [cleantitle.tv(show), cleantitle.tv(show_alt)]
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [i for i in result if any(x == cleantitle.tv(i[0]) for x in shows)]
            result = [i[1] for i in result if any(x in i[0] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = self.episode_link % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            u = client.parseDOM(result, "meta", ret="content", attrs = { "property": "og:url" })[0]
            links = re.compile('<a href="([?]link_id=.+?)".+?>(.+?)</a>').findall(result)
            links = [u + i[0]  for i in links if 'server' in i[1].lower()]

            for u in links[:3]:
                try:
                    result = client.source(u)

                    url = client.parseDOM(result, "source", ret="src", attrs = { "type": "video/.+?" })
                    if len(url) > 0:
                        i = googleplus.tag(url[0])[0]
                        sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})

                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = gkplugins.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]

                    if 'google' in url: source = 'GVideo'
                    elif 'vk.com' in url: source = 'VK'
                    else: raise Exception()

                    url = resolvers.request(url)
                    for i in url: sources.append({'source': source, 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
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

