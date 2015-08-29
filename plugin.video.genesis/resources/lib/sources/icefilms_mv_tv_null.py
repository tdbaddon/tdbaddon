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


import re,urllib,urlparse,random

from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://ipv6.icefilms.info'
        self.link_1 = 'http://ipv6.icefilms.info'
        self.link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.icefilms.info'
        self.link_3 = 'https://icefilms.unblocked.pw'
        self.moviesearch_link = '/movies/a-z/%s'
        self.tvsearch_link = '/tv/a-z/%s'
        self.video_link = '/membersonly/components/com_iceplayer/video.php?h=331&w=719&vid=%s&img='
        self.resp_link = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?s=%s&t=%s'
        self.headers = {}


    def get_movie(self, imdb, title, year):
        try:
            query = re.sub('^THE\s+|^A\s+', '', title.strip().upper())[0]
            if not query.isalpha(): query = '1'
            query = self.moviesearch_link % query

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, query), headers=self.headers)
                if 'Donate' in str(result): break

            imdb = re.sub('[^0-9]', '', imdb)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = '%s?%s' % (urlparse.urlparse(url).path, urlparse.urlparse(url).query)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = re.sub('^THE\s+|^A\s+', '', tvshowtitle.strip().upper())[0]
            if not query.isalpha(): query = '1'
            query = self.tvsearch_link % query

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, query), headers=self.headers)
                if 'Donate' in str(result): break

            imdb = re.sub('[^0-9]', '', imdb)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = '%s?%s' % (urlparse.urlparse(url).path, urlparse.urlparse(url).query)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, url), headers=self.headers)
                if 'Donate' in str(result): break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = urllib.unquote_plus(result)

            url = re.compile('(/ip[.]php.+?>%01dx%02d)' % (int(season), int(episode))).findall(result)[0]
            url = re.compile('(/ip[.]php.+?)&').findall(url)[-1]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            t = url.split('v=', 1)[-1].rsplit('&', 1)[0] 
            url = self.video_link % t

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                result = client.source(urlparse.urljoin(base_link, url), headers=self.headers)
                if 'ripdiv' in str(result): break

            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = client.parseDOM(result, 'div', attrs = {'class': 'ripdiv'})

            hd = [i for i in links if '>HD 720p<' in i]
            sd = [i for i in links if '>DVDRip / Standard Def<' in i]
            if len(sd) == 0: sd = [i for i in links if '>DVD Screener<' in i]
            if len(sd) == 0: sd = [i for i in links if '>R5/R6 DVDRip<' in i]

            if len(hd) > 0: hd = hd[0].split('<p>')
            if len(sd) > 0: sd = sd[0].split('<p>')
            links = [(i, 'HD') for i in hd] + [(i, 'SD') for i in sd]

            for i in links:
                try:
                    quality = i[1]

                    host = client.parseDOM(i[0], 'a')[-1]
                    host = re.sub('\s|<.+?>|</.+?>|.+?#\d*:', '', host)
                    host = host.strip().lower()
                    if quality == 'HD' and not host in hosthdDict: raise Exception()
                    if quality == 'SD' and not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = client.parseDOM(i[0], 'a', ret='onclick')[-1]
                    url = re.compile('[(](.+?)[)]').findall(url)[0]
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap= &iqs=&url=' % (url, t, sec, random.randrange(2000, 9999), random.randrange(2000, 9999))
                    url = url.encode('utf-8')
                    sources.append({'source': host, 'quality': quality, 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            links = [self.link_1, self.link_3]
            for base_link in links:
                r = urlparse.urljoin(base_link, self.video_link % urlparse.parse_qs(url)['t'][0])
                u = urlparse.urljoin(base_link, self.resp_link % (urlparse.parse_qs(url)['id'][0], urlparse.parse_qs(url)['t'][0]))
                result = client.request(u, post=url, referer=r, cookie=client.request(r, output='cookie'))
                if 'com_iceplayer' in str(result): break

            url = urlparse.parse_qs(urlparse.urlparse(result).query)['url'][0]
            url = resolvers.request(url)
            return url
        except:
            return


