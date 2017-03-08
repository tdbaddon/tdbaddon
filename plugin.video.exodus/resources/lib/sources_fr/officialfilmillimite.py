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

import re, urllib, urlparse, base64, json, unicodedata

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['official-film-illimite.net']
        self.base_link = 'http://official-film-illimite.net/'
        self.key_link = '?'
        self.moviesearch_link = 's=%s'
        self.tvsearch_link = 's=%s'

    def movie(self, imdb, title, localtitle, year):
        try:
            url = {'imdb': imdb, 'title': title, 'localtitle':localtitle, 'year': year}
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
        try:
            print '-------------------------------    -------------------------------'
            sources = []

            print url

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            print data

            title = data['title']
            year = data['year'] if 'year' in data else data['year']
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False
            localtitle = data['localtitle'] if 'localtitle' in data else False


            self.search_link = 'http://official-film-illimite.net/?s=%s'

            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            print query

            aTitle = cleantitle.get(cleantitle.normalize(title))

            t = cleantitle.get(cleantitle.normalize(aTitle))

            r = client.request(query)
            r0 = client.parseDOM(r, 'div', attrs={'class': 'boxinfo'})
            r = [x.replace(' streaming hd', '') for x in r0]
            r = [x.replace(' Streaming HD', '') for x in r0]
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs={'class': 'tt'})) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = sorted(set(r))

            try:
                r = [i[0] for i in r if t + year == cleantitle.get(i[1])][0]
            except:
                for i in r:
                    print 't = %s, i[1] = %s' % (t, cleantitle.normalize(cleantitle.get(i[1])))

                    if season and episode:
                        if t + 'saison' + season == cleantitle.normalize(cleantitle.get(i[1])):
                            r = i[0]
                            print ''
                    else:
                        if t == cleantitle.normalize(cleantitle.get(i[1])):
                            r = i[0]

            if season and episode:
                url = r
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                s = client.request(url)

            else:
                url = r
                url = client.replaceHTMLCodes(url)

                s = client.request(url)

            urls = client.parseDOM(s, 'iframe', ret='data-lazy-src')


            for url in urls:

                url = url.encode('utf-8')

                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                ##if not host in hostDict: continue
                host = client.replaceHTMLCodes(host)
                host = host.encode('utf-8')


                langue = 'VF' #uneLangue[counter]

                quality = 'SD'
                quality2 = 'SD' #uneQualite[counter]
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

                ##counter = counter + 1

            print sources

            return sources
        except:
            return sources


    def resolve(self, url):
        return url