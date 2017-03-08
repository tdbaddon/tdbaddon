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
        self.domains = ['voirfilms.co']
        self.base_link = 'http://www.voirfilms.co'


    def movie(self, imdb, title, localtitle, year):
        try:
            url = {'imdb': imdb, 'title': title, 'localtitle': localtitle, 'year': year}
            url = urllib.urlencode(url)
            print 'MOVIE    url = %s' % url
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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            print data

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year'] if 'year' in data else data['year']
            season = data['season'] if 'season' in data else False
            episode = data['episode'] if 'episode' in data else False
            localtitle =  data['localtitle'] if 'localtitle' in data else False

            '''
            if season and episode:
                aTitle = tvmaze.tvMaze().getTVShowTranslation(data['tvdb'], 'fr')
            else:
                aTitle = trakt.getMovieTranslation(data['imdb'], 'fr')

                if not aTitle == None:
                    print ''
                else:
                    aTitle = title
            '''

            if season and episode:
                query = 'http://www.voirfilms.co/series-tv-streaming/?action=recherche&story=%s' % data['tvshowtitle']
                url = 'http://www.voirfilms.co/rechercher/'
                referer='http://www.voirfilms.co/series-tv-streaming/'
            else:
                query = 'http://www.voirfilms.co/rechercher/?action=recherche&story=%s' % title
                url = 'http://www.voirfilms.co/rechercher/'

            post = 'action=recherche&story=%s' % title

            if season and episode:
                r = client.request(url, post=post, referer='http://www.voirfilms.co/series-tv-streaming/')
            else:
                #r = client.request(query)
                r = client.request(url, post=post)

            print query

            aTitle = cleantitle.get(cleantitle.normalize(title))

            if season and episode:
                post = 'r_serie=%s' % urllib.quote_plus(data['tvshowtitle'])
            else:
                post = 'r_film=%s' % urllib.quote_plus(title)

            t = cleantitle.get(cleantitle.normalize(title))

            r = client.parseDOM(r, 'div', attrs={'class': 'imagefilm'})

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

            if season and episode:
                try:
                    r = [i[0] for i in r if 'film' + t + year == cleantitle.get(i[1])][0]
                except:
                    for i in r:
                        print 't = %s, i[1] = %s' % ( 'film' + t , cleantitle.normalize(cleantitle.get(i[1])))
                        if 'film' + t == cleantitle.normalize(cleantitle.get(i[1])):
                            url = i[0]
            else:
                try:
                    r = [i[0] for i in r if 'film' + t + year == cleantitle.get(i[1])][0]
                except:
                    for i in r:
                        print 't = %s, i[1] = %s' % ( 'film' + t, cleantitle.normalize(cleantitle.get(i[1])))
                        if 'film' + t == cleantitle.normalize(cleantitle.get(i[1])):
                            url = i[0]

            url = client.replaceHTMLCodes(url)

            #r = client.request(url, XHR=True, referer=url)
            r = client.request(url)

            if season and episode:
                #<div class="unepetitesaisons">
                #<a href="http://www.voirfilms.co/blindspot-saison-2-9046.htm" title="Blindspot saison 2">
                r = client.parseDOM(r, 'div', attrs={'id': 'listedessaisons'})[0]
                r = client.parseDOM(r, 'div', attrs={'class': 'unepetitesaisons'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

                t = cleantitle.get(cleantitle.normalize(title + 'saison' + season))

                for i in r:
                    print 't = %s, r = %s' % ( t , cleantitle.normalize(cleantitle.get(i[1])))
                    if t == cleantitle.normalize(cleantitle.get(i[1])):
                        url = i[0]

                r = client.request(url)
                r = client.parseDOM(r, 'li', attrs={'class': 'description132'})
                r = [(client.parseDOM(i, 'a', attrs={'class': 'n_episode[0-9]{1,4}'}, ret='href'),client.parseDOM(i, 'a', attrs={'class': 'n_episode[0-9]{1,4}'})) for i in r]
                r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

                t = cleantitle.get(cleantitle.normalize('pisode' + episode))

                for i in r:
                    print 't = %s, i[1] = %s' % ('pisode' + episode, cleantitle.get(cleantitle.normalize(i[1][1:])))
                    if t == cleantitle.get(cleantitle.normalize(i[1][1:])):
                        url = i[0]

                r6 = client.request('http://www.voirfilms.co/' + url)

                links = client.parseDOM(r6, 'div', attrs={'class': 'link_list'})
                links = client.parseDOM(links, 'a', ret='href')

                for url in links:

                    '''
                    if 'www.voirfilms.co' in r6:

                        #url = 'http://www.voirfilms.co/video.php?%s' % url
                        #<iframe name="filmPlayer"
                        r7 = client.parseDOM(url, 'iframe', attrs={'name': 'filmPlayer'}, ret='src')

                        try:
                            r7 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                            r7 = client.request(r7, XHR=True)
                            r6 = client.parseDOM(r7, 'a', attrs={'class': 'button_upload green'}, ret='href')[0]
                        except:
                            r7 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                            r7 = client.request(r7, XHR=True)
                            r6 = client.parseDOM(r7, 'a', ret='href')[0]
                    else:
                        #try:
                        #    r6 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                        #    r6 = re.sub('"', '', r6)
                        #except:
                        r6 = client.parseDOM(r6, 'a', ret='href')[0]
                        '''

                    # url = r6

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
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

                    sources.append({'source': host, 'quality': quality, 'language': langue, 'url': url, 'direct': False,
                                    'debridonly': False})

            else:
                r4 = re.compile('http://www.voirfilms.co/video.php(.+?)\"', re.MULTILINE | re.DOTALL).findall(r)

                r4 = sorted(set(r4))

                for r5 in r4:
                    url = 'http://www.voirfilms.co/video.php%s' % r5
                    r6 = client.request(url)

                    if 'www.voirfilms.co' in r6:
                        try:
                            r7 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                            r7 = client.request(r7)
                            r6 = client.parseDOM(r7, 'a', attrs={'class': 'button_upload green'}, ret='href')[0]
                        except:
                            r7 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                            r7 = client.request(r7)
                            r6 = client.parseDOM(r7, 'a', ret='href')[0]
                    else:
                        try:
                            r6 = client.parseDOM(r6, 'meta', attrs={'http-equiv': 'refresh'}, ret='url')[0]
                            r6 = re.sub('"', '', r6)
                        except:
                            r6 = client.parseDOM(r6, 'a', ret='href')[0]

                    url = r6

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
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

                    sources.append({'source': host, 'quality': quality, 'language': langue, 'url': url, 'direct': False, 'debridonly': False})

            print sources

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


