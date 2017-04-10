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

import re, urllib, urlparse, base64, json, unicodedata, os, sys

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['skstream.org']
        self.base_link = 'http://www.skstream.org'
        self.key_link = '/recherche?'
        self.moviesearch_link = '/recherche/films?s=%s'
        self.tvsearch_link = '/recherche/series?r_serie=%s'

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

            if season and episode:
                aTitle = tvmaze.tvMaze().getTVShowTranslation(data['tvdb'], 'fr')
            else:
                aTitle = trakt.getMovieTranslation(data['imdb'], 'fr')

                if not aTitle == None:
                    print ''
                else :
                    aTitle = title

            if season and episode:
                query = 'http://www.skstream.org/recherche/?s=' + urllib.quote_plus(aTitle)
                query = urlparse.urljoin(self.base_link, query)
            else:
                query = self.key_link + 's=' + urllib.quote_plus(aTitle)
                query = urlparse.urljoin(self.base_link, query)

            print query


            r = client.request(query)

            try:
                r0 = re.compile('<center><h3>(.+?)</h3></center>').findall(r)[0]

                if 'Aucun film à afficher.' in r0:
                    aTitle = re.sub(':', '-', aTitle)
                    query = self.key_link + 'r_film=' + urllib.quote_plus(aTitle)
                    query = urlparse.urljoin(self.base_link, query)

                    r = client.request(query)
            except:
                pass

            print query

            aTitle = cleantitle.get(cleantitle.normalize(aTitle))
            t = cleantitle.get(cleantitle.normalize(aTitle))

            r = client.parseDOM(r, 'div', attrs={'class': 'panel-body'})
            r = client.parseDOM(r, 'div', attrs={'class': 'col-xs-3 col-sm-3 col-md-3 col-lg-3  movie_single'})
            r = [(client.parseDOM(client.parseDOM(i, 'div', attrs={'class': 'text-center'}), 'a', ret='href'), client.parseDOM(i, 'img', attrs={'class': 'img-responsive img-thumbnail'}, ret='title')) for i in r]
            r = [(i[0][0], i[1][0].lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]

            try:
                r = [i[0] for i in r if t + year == cleantitle.get(i[1])][0]
            except:
                for i in r:
                    print 't = %s, i[1] = %s' % (t, cleantitle.normalize(cleantitle.get(i[1])))
                    if t == cleantitle.normalize(cleantitle.get(i[1])):
                        r = i[0]

            if season and episode:
                url = '%s%s' % (self.base_link , r)
            else:
                url = '%s/%s' % (self.base_link, r)

            url = client.replaceHTMLCodes(url)
            #url = url.encode('utf-8')

            url = urlparse.urljoin('http://www.skstream.org', url)

            print url

            r = client.request(url)

            if season and episode:
                r = client.request(url)
                r = r.replace(' = ', '=')

                unChunk = client.parseDOM(r, 'div', attrs={'class': 'jumbotron'})
                desSaisons = client.parseDOM(r, 'i', attrs={'class': 'fa fa-television'}, ret='id')
                desLiens = client.parseDOM(r, 'div', attrs={'class': 'btn-group'})
                desLiens = client.parseDOM(desLiens, 'a',ret='href')

                for unLienTV in desLiens:
                    tempSaisonEpisode = '/saison-%s/episode-%s/' % (season, episode)
                    if '/series/' in unLienTV and tempSaisonEpisode in unLienTV:
                        urlTV = 'http://www.skstream.org/%s' % unLienTV
                        break

                print urlTV

                s = client.request(urlTV)
                urlLoop = urlTV

                s = client.parseDOM(s, 'table', attrs={'class': 'players table table-striped table-hover'})
            else:
                s = client.request(url)
                urlLoop = url

                s = client.parseDOM(r, 'table', attrs={'class': 'players table table-striped table-hover'})


            leVideo = client.parseDOM(s, 'input', attrs={'name': 'levideo'}, ret='value')
            leHost = re.compile('&nbsp;(.+?)</a></form>').findall(s[0])
            #uneLangue = client.parseDOM(s, 'span', attrs={'class': 'badge'})
            #uneQualite = re.compile('</span></td>\n\s+<td>(.+?)</td>', re.MULTILINE | re.DOTALL).findall(s)

            leHost = [x.lower() for x in leHost]
            #uneLangue = [x.lower() for x in uneLangue]
            #uneQualite = [x.lower() for x in uneQualite]

            counter = 0
            for unVideo in leVideo:

                if season and episode:
                    url = urlLoop + '***' + unVideo + '***' + 'TV'
                else:
                    url = urlLoop + '***' + unVideo + '***' + 'Movie'

                url = url.encode('utf-8')

                try:
                    if leHost[counter] == 'openload':
                        host = filter(lambda s: leHost[counter] in str(s), hostDict)[1]
                    else:
                        host = filter(lambda s: leHost[counter] in str(s), hostDict)[0]
                except:
                    counter = counter + 1
                    continue

                host = host.encode('utf-8')

                #langue = uneLangue[counter]

                #quality2 = uneQualite[counter]
                #quality2 = re.sub('-', '', quality2)
                quality2 = ''

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

                sources.append({'source': host, 'quality': quality, 'language': 'FR', 'url': url, 'info': '', 'direct': False, 'debridonly': False})

                counter = counter + 1

            print sources

            return sources
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(exc_type, fname, exc_tb.tb_lineno)

            return sources


    def resolve(self, url):

        url2 = url
        print url2

        parts = url.split('***')
        url = parts[0]
        unVideo = parts[1]

        print url, unVideo

        post = 'levideo=%s' % unVideo
        result3 = client.request(url, post=post)

        if parts[2] == 'TV':
            u1 = client.parseDOM(result3, 'a', attrs={'class': 'btn btn-primary'}, ret='href')[0]
        else:
            u = client.parseDOM(result3, 'div', attrs={'class': 'tab-content'})[0]
            u1 = client.parseDOM(u, 'iframe', ret='src')[0]

        url = client.request(u1, referer='http://www.skstream.org', output='geturl')

        if 'coo5shaine' in url:
            url = re.sub('http://coo5shaine.com', 'http://allvid.ch', url)

        if 'oogh8ot0el' in url:
            url = re.sub('http://oogh8ot0el.com', 'http://youwatch.org', url)

        if 'ohbuegh3ev' in url:
            url = re.sub('http://ohbuegh3ev.com', 'http://exashare.com', url)

        print url

        url = url.encode('utf-8')

        # if url != None:
        #    print url

        if 'http://www.skstream.org' in url:
            result5 = client.request(url)
            url = re.compile('<a href=\"(.+?)\" style=\"', re.MULTILINE | re.DOTALL).findall(result5)[0]
            print url

        return url


    def clean2(title):
        if title == None: return

        title = re.sub('&#(\d+);', '', title)
        title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
        title = title.replace('&quot;', '\"').replace('&amp;', '&')
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()

        try: title = title.encode('utf-8')
        except: pass
        return title
