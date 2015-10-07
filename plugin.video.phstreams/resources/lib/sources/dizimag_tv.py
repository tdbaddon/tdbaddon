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


import re,urllib,urlparse,json,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://dizimag.co'
        self.headers = {'X-Requested-With' : 'XMLHttpRequest'}

        self.give_link = '/service/givevideo'
        self.vdmg_link = '/service/vdmg?type=%s&a=%s&b=1%s&s=%s&e=%s&_=%s'
        self.idmg_link = '/service/idmg?type=%s&a=%s&b=1%s&s=%s&e=%s&_=%s'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            result = client.source(self.base_link)
            result = client.parseDOM(result, 'div', attrs = {'id': 'fil'})[0]
            result = zip(client.parseDOM(result, 'a', ret='href'), client.parseDOM(result, 'a'))

            tvshowtitle = cleantitle.tv(tvshowtitle)

            result = [i[0] for i in result if tvshowtitle == cleantitle.tv(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            result = client.parseDOM(result, 'a', ret='href')
            result = [i for i in result if '/%01d-sezon-%01d-bolum-' % (int(season), int(episode)) in i][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            sources_url = urlparse.urljoin(self.base_link, url)

            result = client.source(sources_url)

            links = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'alterlink'})
            links = [i for i in links if not i.endswith('=0')]

            for link in links:
                try:
                    url = sources_url + link

                    result = client.source(url, close=False)
                    result = re.compile('<script[^>]*>(.*?)</script>', re.DOTALL).findall(result)
                    result = [re.compile('var\s+kaynaklar\s*=\s*\[([^]]+)').findall(i) for i in result]
                    result = [i[0] for i in result if len(i) > 0]
                    result = [re.compile('file\s*:\s*"([^"]+)"\s*,\s*label\s*:\s*"(\d+)p?"').findall(i) for i in result]
                    result = [i for i in result if len(i) > 0][0]

                    try: 
                        url = [i for i in result if not 'google' in i[0]]
                        url = [('%s|User-Agent=%s&Referer=%s' % (i[0].decode('unicode_escape'), urllib.quote_plus(client.agent()), urllib.quote_plus(sources_url)), i[1]) for i in url]

                        try: sources.append({'source': 'Dizimag', 'quality': '1080p', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '1080'][0]})
                        except: pass
                        try: sources.append({'source': 'Dizimag', 'quality': 'HD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '720'][0]})
                        except: pass
                        try: sources.append({'source': 'Dizimag', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '480'][0]})
                        except: sources.append({'source': 'Dizimag', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '360'][0]})
                    except:
                        pass

                    try: 
                        url = [i for i in result if 'google' in i[0]]

                        try: sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '1080'][0]})
                        except: pass
                        try: sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '720'][0]})
                        except: pass
                        try: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '480'][0]})
                        except: sources.append({'source': 'GVideo', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '360'][0]})
                    except:
                        pass

                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if not 'google' in url: return url
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


