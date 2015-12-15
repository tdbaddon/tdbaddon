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
from modules.libraries import cleantitle
from modules.libraries import client
from modules.resolvers import googledocs


class source:
    def __init__(self):
        self.base_link = 'http://movietube.vc'
        self.tvbase_link = 'http://kissdrama.net'
        self.index_link = '/index.php'
        self.docs_link = 'https://docs.google.com/file/d/%s/'


    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % title})

            result = client.source(query, post=post)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "tr")

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [client.parseDOM(i, "h1")[0] for i in result]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a")[0]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = result.split('v=', 1)[-1]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            query = self.tvbase_link + self.index_link
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % url})

            result = client.source(query, post=post)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "tr")

            show = cleantitle.tv(url)
            season = '%01d' % int(season)
            episode = '%02d' % int(episode)
            result = [client.parseDOM(i, "h1")[0] for i in result]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a")[0]) for i in result]
            result = [(i[0], re.sub('\sSeason(|\s)\d*.+', '', i[1]), re.compile('\sSeason *(\d*) *').findall(i[1])[0]) for i in result]
            result = [i for i in result if show == cleantitle.tv(i[1])]
            result = [i[0] for i in result if season == i[2]][0]

            url = result.split('v=', 1)[-1]
            url = '%s|%s' % (url, episode)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            content = re.compile('(.+?)\|\d*$').findall(url)

            if len(content) == 0:
                query = self.base_link + self.index_link
                post = urllib.urlencode({'a': 'getmoviealternative', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
                result = client.source(query, post=post)
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [i for i in result if any(x in i for x in ['0000000008400000.png', '0000000008110000.png'])]
                links = [i for i in links if any(x in i for x in ['>1080p<', '>720p<'])]
                links = [client.parseDOM(i, "a", ret="href")[0] for i in links][:3]
                links = [i.split('?v=')[-1] for i in links]

                for u in links:
                    try:
                        query = self.base_link + self.index_link
                        post = urllib.urlencode({'a': 'getplayerinfo', 'c': 'result', 'p': '{"KeyWord":"%s"}' % u})
                        result = client.source(query, post=post)

                        url = client.parseDOM(result, "source", ret="src", attrs = { "data-res": "1080" })
                        if len(url) > 0:
                            sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'Movietube', 'url': url[0]})

                        url = client.parseDOM(result, "source", ret="src", attrs = { "data-res": "720" })
                        if len(url) > 0:
                            sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'Movietube', 'url': url[0]})

                        url = client.parseDOM(result, "iframe", ret="src")
                        url = [i for i in url if 'docs.google.com' in i]
                        if not len(url) == 2: raise Exception()

                        u1 = googledocs.resolve(url[0]) ; u2 = googledocs.resolve(url[1])

                        for i in range(0, len(u1)): sources.append({'source': 'GVideo', 'quality': u1[i]['quality'], 'provider': 'Movietube', 'url': 'stack://%s , %s' % (u1[i]['url'], u2[i]['url'])})
                    except:
                        pass

            else:
                query = self.tvbase_link + self.index_link
                url, episode = re.compile('(.+?)\|(\d*)$').findall(url)[0]
                post = urllib.urlencode({'a': 'getpartlistinfo', 'c': 'result', 'p': '{"KeyWord":"%s","Episode":"%s"}' % (url, episode)})
                result = client.source(query, post=post)
                result = re.compile('(<a.+?</a>)').findall(result)

                links = [client.parseDOM(i, "a", ret="data") for i in result]
                links = [i[0] for i in links if len(i) > 0]
                links = [i for i in links if i.startswith('--MP4') or i.startswith('--Doc')]

                for u in links:
                    try:
                        if u.startswith('--Doc'):
                            url = self.docs_link % u.split('--', 2)[-1]
                            url = googledocs.resolve(url)

                            for i in url: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
                        else:
                            url = u.split('--', 2)[-1]
                            i = googledocs.tag(url)[0]

                            sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Movietube', 'url': i['url']})
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

