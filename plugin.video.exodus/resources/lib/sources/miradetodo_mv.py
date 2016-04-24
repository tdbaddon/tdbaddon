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


import re,urllib,urllib2,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import cloudflare
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['miradetodo.net']
        self.base_link = 'http://miradetodo.net'
        self.search_link = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwMDc0NjAzOTU3ODI1MDQ0NTkzNTpsMmdrdWtvcnRpZyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            query = '%s %s' % (title, year)
            query = base64.b64decode(self.search_link) % urllib.quote_plus(query)

            result = client.source(query)
            result = json.loads(result)['results']

            result = [(i['url'], i['titleNoFormatting']) for i in result]
            result = [(i[0], re.findall('(?:^Ver Online |^Ver |)(.+?)(?: HD |)\((\d{4})', i[1])) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1]) for i in result if len(i[1]) > 0]

            r = [i for i in result if t == cleantitle.get(i[1]) and year == i[2]]

            if len(r) == 0:
                t = 'http://www.imdb.com/title/%s' % imdb
                t = client.source(t, headers={'Accept-Language':'ar-AR'})
                t = client.parseDOM(t, 'title')[0]
                t = re.sub('(?:\(|\s)\d{4}.+', '', t).strip()
                t = cleantitle.get(t)
                r = [i for i in result if t == cleantitle.get(i[1]) and year == i[2]]

            try: url = re.findall('//.+?(/.+)', r[0][0])[0]
            except: url = r[0][0]
            try: url = re.findall('(/.+?/.+?/)', url)[0]
            except: pass
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            cookie, agent, result = cloudflare.request(r, output='extended')

            f = client.parseDOM(result, 'div', attrs = {'class': 'movieplay'})
            f = [re.findall('(?:\"|\')(http.+?miradetodo\..+?)(?:\"|\')', i) for i in f]
            f = [i[0] for i in f if len(i) > 0]

            links = []
            dupes = []

            for u in f:

                try:
                    id = urlparse.parse_qs(urlparse.urlparse(u).query)['id'][0]

                    if id in dupes: raise Exception()
                    dupes.append(id)

                    try:
                        if 'acd.php' in u: raise Exception()

                        headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': u}

                        post = urllib.urlencode({'link': id})

                        url = urlparse.urljoin(self.base_link, '/stream/plugins/gkpluginsphp.php')
                        url = cloudflare.source(url, post=post, headers=headers)
                        url = json.loads(url)['link']

                        if type(url) is list:
                            url = [{'url': i['link'], 'quality': '1080p'} for i in url if '1080' in i['label']] + [{'url': i['link'], 'quality': 'HD'} for i in url if '720' in i['label']]
                        else:
                            url = [{'url': url, 'quality': 'HD'}]

                        for i in url:
                            try: links.append({'source': 'gvideo', 'quality': i['quality'], 'url': i['url']})
                            except: pass

                        continue
                    except:
                        pass

                    try:
                        result = cloudflare.source(u, headers={'Referer': r})

                        url = re.findall('AmazonPlayer.*?file\s*:\s*"([^"]+)', result, re.DOTALL)[0]

                        class NoRedirection(urllib2.HTTPErrorProcessor):
                            def http_response(self, request, response): return response

                        o = urllib2.build_opener(NoRedirection)
                        o.addheaders = [('User-Agent', agent)]
                        r = o.open(url)
                        url = r.headers['Location']
                        r.close()

                        links.append({'source': 'cdn', 'quality': 'HD', 'url': url})
                    except:
                        pass
                except:
                    pass


            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'MiraDeTodo', 'url': i['url'], 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


