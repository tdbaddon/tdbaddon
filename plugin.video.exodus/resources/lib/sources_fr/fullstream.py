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

import re, urllib, urlparse, time, sys, os

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['/full-stream.nu']
        self.base_link = 'http://full-stream.nu'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, year):
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

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year'] if 'year' in data else data['year']
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False
            localtitle =  data['localtitle'] if 'localtitle' in data else False

            hostDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]
            locDict = [i[0] for i in hostDict]

            url = 'http://full-stream.nu/index.php?do=search'

            if season and episode:
                post = 'do=search&subaction=search&search_start=0&full_search=1&result_from=1&story=%s&titleonly=3&searchuser=&replyless=0&replylimit=0&searchdate=0&beforeafter=after&sortby=date&resorder=desc&showposts=1&catlist[]=2'  % (urllib.quote_plus(cleantitle.query(title)))
            else:
                post = 'do=search&subaction=search&search_start=0&full_search=1&result_from=1&story=%s&titleonly=3&searchuser=&replyless=0&replylimit=0&searchdate=0&beforeafter=after&sortby=date&resorder=desc&showposts=1&catlist[]=43' % (urllib.quote_plus(cleantitle.query(title)))

            t = cleantitle.get(title)

            r = client.request(url, post=post)
            r = client.parseDOM(r, 'h3', attrs={'class': 'mov-title'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(.+?) \-\s+(?:saison)\s+(\d+)', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = [(i[0], i[1], re.findall('\((.+?)\)$', i[1]), i[2]) for i in r]
            r = [(i[0], i[2][0] if len(i[2]) > 0 else i[1], i[3]) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and int(i[2]) == int(season)][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)

            r = client.request('http://full-stream.nu/' + url)

            if season and episode:
                r = re.compile('<div id=\"episode%s(.+?)</ul>' % episode, re.MULTILINE | re.DOTALL).findall(r)[0]
                r = client.parseDOM(r, 'a', ret='href')
            else:
                r = client.parseDOM(r, 'div', attrs={'class': 'elink'})
                r = client.parseDOM(r, 'a', ret='href')

            for url in r:

                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                host = client.replaceHTMLCodes(host)
                host = host.encode('utf-8')

                langue = 'FR'

                quality2 = 'SD'
                quality2 = re.sub('-', '', quality2)

                if '1080p' in quality2:
                    quality = '1080p'
                elif '720p' in quality2 or 'bdrip' in quality2 or 'hdrip' in quality2:
                    quality = 'HD'
                else:
                    quality = 'SD'

                if 'dvdscr' in quality2 or 'r5' in quality2 or 'r6' in quality2:
                    quality2 = 'SCR'
                elif 'camrip' in quality2 or 'tsrip' in quality2 or 'hdcam' in quality2 or 'hdts' in quality2 or 'dvdcam' in quality2 or 'dvdts' in quality2 or 'cam' in quality2 or 'telesync' in quality2 or 'ts' in quality2:
                    quality2 = 'CAM'

                sources.append({'source': host, 'quality': quality, 'language': langue, 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    def resolve(self, url):
        return url
