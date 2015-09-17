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

            s, e = re.compile('/(.+?)/(\d+)').findall(url)[0]

            sources_url = urlparse.urljoin(self.base_link, url)

            result = client.source(sources_url)

            links = client.parseDOM(result, 'a', ret='onclick', attrs = {'class': 'alterlink'})

            for link in links:
                try:
                    b = re.compile('(\d+)').findall(link)[0]

                    host = re.compile("'(.+?)'").findall(link)[0]

                    if host == 'Roosy':
                        type = host
                        a = 'awQa5s14d5s6s12s'
                        dmg = self.vdmg_link
                    else:
                        url = urlparse.urljoin(self.base_link, self.give_link)
                        post = urllib.urlencode({'i': b, 'n': host, 'p': 0})
                        result = client.source(url, post=post, headers=self.headers, close=False)
                        result = json.loads(result)

                        type = result['p']['tur']
                        a = result['p']['c']
                        dmg = self.idmg_link

                    url = dmg % (type, a, b, s, e, int(time.time() * 1000))
                    url = urlparse.urljoin(self.base_link, url)

                    result = client.source(url, headers=self.headers, close=False)
                    result = result.replace('\n', '')

                    url = re.compile('(var\s+kaynaklar\s*=\s*.+)').findall(result)[0]
                    url = re.compile('file *: *"(.+?)".+?label *: *"(.+?)"').findall(url)
                    url = [('%s|User-Agent=%s&Referer=%s' % (i[0].decode('unicode_escape'), urllib.quote_plus(client.agent()), urllib.quote_plus(sources_url)), i[1]) for i in url]

                    try: sources.append({'source': 'Dizimag', 'quality': '1080p', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '1080p'][0]})
                    except: pass
                    try: sources.append({'source': 'Dizimag', 'quality': 'HD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '720p'][0]})
                    except: pass
                    try: sources.append({'source': 'Dizimag', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '480p'][0]})
                    except: sources.append({'source': 'Dizimag', 'quality': 'SD', 'provider': 'Dizimag', 'url': [i[0] for i in url if i[1] == '360p'][0]})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url



