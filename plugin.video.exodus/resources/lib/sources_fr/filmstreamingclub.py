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

import re, urllib, urlparse, base64, sys, os

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['film-streaming.club']
        self.base_link = 'http://www.film-streaming.club'
        self.key_link = 'http://www.film-streaming.club/search.php'
        self.search_link = 's=%s'
        self.moviesearch_link = 's=%s'
        self.tvsearch_link = 's=%s'


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
        try:
            print '-------------------------------    -------------------------------'
            sources = []

            if url == None:
                return sources


            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year'] if 'year' in data else data['year']
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False
            localtitle =  data['localtitle'] if 'localtitle' in data else False

            if season and episode:
                aTitle = tvmaze.tvMaze().getTVShowTranslation(data['tvdb'], 'fr')
            else:
                aTitle = trakt.getMovieTranslation(data['imdb'], 'fr')

                if not aTitle == None:
                    print ''
                else :
                    aTitle = title

            query = '%s?s=%s' % (self.key_link, urllib.quote_plus(cleantitle.normalize(aTitle)))
            query = urlparse.urljoin(self.base_link, query)

            print query

            aTitle = cleantitle.get(cleantitle.normalize(aTitle))

            if season and episode:
                post = 'r_serie=%s' % urllib.quote_plus(aTitle)
            else:
                post = 'r_film=%s' % urllib.quote_plus(aTitle)

            t = cleantitle.get(cleantitle.normalize(aTitle))

            r = client.request(query)

            r0 = client.parseDOM(r, 'div', attrs={'class': 'thumbnail thumbnail__portfolio'})
            r0 = client.parseDOM(r, 'div', attrs={'class': 'portfolio_item_holder'})

            r = [x.replace(' en streaming', '') for x in r0]
            r = [x.replace(' en Streaming', '') for x in r0]
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

            try:
                r = [i[0] for i in r if t + year == cleantitle.get(i[1])][0]
            except:
                for i in r:
                    print 't = %s, i[1] = %s' % (t, cleantitle.normalize(cleantitle.get(i[1])))
                    if t == cleantitle.normalize(cleantitle.get(i[1])):
                        r = i[0]

            url = '%s/%s' % (self.base_link , r)
            url = client.replaceHTMLCodes(url)
            #url = url.encode('utf-8')

            print url

            r = client.request(url)

            urls = client.parseDOM(r, 'a', attrs={'target': '_blank'}, ret='href')

            for url in urls:

                if url == '':
                    continue

                url = url.encode('utf-8')
                print url

                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                if not host in hostDict:
                    print ''
                else:
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    langue = 'VF'

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

                    print host, quality, langue, url

                    sources.append({'source': host, 'quality': quality, 'language': langue, 'url': url, 'direct': False, 'debridonly': False})

                print sources

            return sources

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(exc_type, fname, exc_tb.tb_lineno)

            return sources


    def resolve(self, url):
        return url


    def __search(self, title):
        try:
            query = '%s?s=%s' % (self.key_link, urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)

            r = client.request(query)
            r = client.parseDOM(r, 'figure', attrs={'class': 'thumbnail thumbnail__portfolio'})
            r = [x.replace(' en streaming', '') for x in r]
            r = [x.replace(' en Streaming', '') for x in r]
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][0]

            url = '%s/%s' % (self.base_link , r)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return
