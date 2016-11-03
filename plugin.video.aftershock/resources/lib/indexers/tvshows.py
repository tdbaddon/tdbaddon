# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

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


import os,sys,re,json,urllib,urlparse,base64,datetime

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None


from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import metacache
from resources.lib.libraries import workers
from resources.lib.libraries import views
from resources.lib.libraries import logger

class tvshows:
    def __init__(self):
        self.list = []

        self.tmdb_link = 'http://api.themoviedb.org'
        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=')
        self.tvdb_key = base64.urlsafe_b64decode('OUZDQkM2MjlEQzgyRjA4Qw==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.info_lang = control.setting('infoLang') or 'en'

        self.tmdb_info_link = 'http://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=credits,content_ratings,external_ids' % ('%s', self.tmdb_key, self.info_lang)
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key, '%s', re.sub('bg', 'en', self.info_lang))
        self.tvdb_search_link = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tmdb_search_link = 'http://api.themoviedb.org/3/search/tv?api_key=%s&query=%s' % (self.tmdb_key, '%s')
        self.tmdb_by_imdb = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ('%s', self.tmdb_key)
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s'
        self.imdb_by_title = 'http://www.omdbapi.com/?t=%s'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.network = ''

    def get(self, url, idx=True, provider=None,network=None):
        try:
            self.list = cache.get(self.get_shows, 168, url, provider, network, table='rel_shows')
            if idx == True: self.tvshowDirectory(self.list)
            return self.list
        except Exception as e:
            logger.error(e.message)
            pass

    def get_shows(self, url, provider=None, network=None):
        try:

            # change the implementation to get shows from all providers as save to DB
            if not provider == None:
                call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
                self.list = call.get_shows(network, url)
                self.network = network
                self.list = self.predb(self.list)
                self.worker()
                self.network = ''
            return self.list
        except Exception as e:
            logger.error(e.message)
            pass

    def predb(self, items):
        for i in range(0, len(self.list)):
            try: imdb = self.list[i]['imdb']
            except: imdb = '0'
            try: tmdb = self.list[i]['tmdb']
            except: tmdb = '0'
            try: tvdb = self.list[i]['tvdb']
            except: tvdb = '0'

            if imdb == '0' and tmdb == '0' and tvdb == '0':
                title = self.list[i]['title'].lower()
                if 'season' in title:
                    title = title[:title.index('season')-1]
                origSeriesName = title
                title = urllib.quote_plus(title)

                try :
                    # try searching the id from tvdb
                    url = self.tvdb_search_link % title
                    result = client.source(url)
                    series = client.parseDOM(result, "Series")
                    for show in series:
                        seriesName = client.parseDOM(show, "SeriesName")[0]
                        if origSeriesName == seriesName.lower():
                            tvdb = client.parseDOM(show, "seriesid")[0]
                            break
                except:
                    pass
                if tmdb == '0' :
                    try:
                        # try searching in tmdb
                        url = self.tmdb_search_link % title
                        result = client.source(url)
                        result = json.loads(result)
                        result = result['results']

                        for j in range(0, len(result)):
                            seriesName = result[j]['name']
                            if origSeriesName == seriesName.lower():
                                tmdb = result[j]['id']
                                break ;
                    except:
                        pass

                if imdb == '0':
                    try :
                        # searching in imdb
                        url = self.imdb_by_title % (urllib.quote_plus(self.list[i]['title']))
                        item3 = client.request(url, timeout='10')
                        item3 = json.loads(item3)
                        imdb = item3['imdbID']
                        if imdb == None or imdb == '' or imdb == 'N/A': imdb = '0'
                        else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                        imdb = imdb.encode('utf-8')
                    except:
                        pass

            self.list[i].update({"tmdb":tmdb, "imdb":imdb, "tvdb":tvdb})
        return self.list

    def worker(self):
        self.meta = []
        total = len(self.list)

        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.info_lang)

        for r in range(0, total, 25):
            threads = []
            for i in range(r, r+25):
                if i < total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        #self.list = [i for i in self.list if not i['tvdb'] == '0']

        if len(self.meta) > 0: metacache.insert(self.meta)

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            try: imdb = self.list[i]['imdb']
            except: imdb = '0'
            try: tmdb = self.list[i]['tmdb']
            except: tmdb = '0'
            try: tvdb = self.list[i]['tvdb']
            except: tvdb = '0'
            try: tvrage = self.list[i]['tvrage']
            except: tvrage = '0'


            if not tmdb == '0':
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                url = self.tmdb_info_link % tmdb

                item = client.request(url, timeout='10')
                if item == None: raise Exception()
                item = json.loads(item)

                if tvdb == '0':
                    tvdb = item['external_ids']['tvdb_id']
                    if tvdb == '' or tvdb == None: tvdb = '0'
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                    tvdb = tvdb.encode('utf-8')
                    self.list[i].update({'tvdb': tvdb})

                if tvrage == '0':
                    tvrage = item['external_ids']['tvrage_id']
                    if tvrage == '' or tvrage == None: tvrage = '0'
                    tvrage = re.sub('[^0-9]', '', str(tvrage))
                    tvrage = tvrage.encode('utf-8')
                    self.list[i].update({'tvrage': tvrage})

                if imdb == '0':
                    imdb = item['external_ids']['imdb_id']
                    if imdb == '' or imdb == None: imdb = '0'
                    if not imdb == '0': imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                    self.list[i].update({'imdb': imdb})


            elif not imdb == '0':
                try :
                    url = self.tmdb_by_imdb % imdb
                    result = client.request(url, timeout='10')
                    result = json.loads(result)

                    tmdb = result['tv_results'][0]['id']
                    if tmdb == '' or tmdb == None: tmdb = '0'
                    tmdb = re.sub('[^0-9]', '', str(tmdb))
                    tmdb = tmdb.encode('utf-8')
                    self.list[i].update({'tmdb': tmdb})

                    if not tmdb == '0':
                        url = self.tmdb_info_link % tmdb

                        item = client.request(url, timeout='10')
                        if item == None: raise Exception()
                        item = json.loads(item)

                        tvdb = item['external_ids']['tvdb_id']
                        if tvdb == '' or tvdb == None: tvdb = '0'
                        tvdb = re.sub('[^0-9]', '', str(tvdb))
                        tvdb = tvdb.encode('utf-8')
                        self.list[i].update({'tvdb': tvdb})

                        tvrage = item['external_ids']['tvrage_id']
                        if tvrage == '' or tvrage == None: tvrage = '0'
                        tvrage = re.sub('[^0-9]', '', str(tvrage))
                        tvrage = tvrage.encode('utf-8')
                        self.list[i].update({'tvrage': tvrage})
                except:
                    pass


            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb

                result = client.request(url, timeout='10')

                try: tvdb = client.parseDOM(result, 'seriesid')[0]
                except: tvdb = '0'

                try: name = client.parseDOM(result, 'SeriesName')[0]
                except: name = '0'
                dupe = re.compile('[***]Duplicate (\d*)[***]').findall(name)
                if len(dupe) > 0: tvdb = str(dupe[0])

                if tvdb == '': tvdb = '0'
                self.list[i].update({'tvdb': tvdb})


            if not tvdb == '0':
                url = self.tvdb_info_link % tvdb
                item2 = client.request(url, timeout='10')

                if imdb == '0':
                    try: imdb = client.parseDOM(item2, 'IMDB_ID')[0]
                    except: pass
                    if imdb == '': imdb = '0'
                    imdb = imdb.encode('utf-8')
                    self.list[i].update({'imdb': imdb})


            if imdb == '0':
                try :
                    url = self.imdb_by_query % (urllib.quote_plus(self.list[i]['title']), self.list[i]['year'])
                    item3 = client.request(url, timeout='10')
                    item3 = json.loads(item3)
                    imdb = item3['imdbID']
                    if imdb == None or imdb == '' or imdb == 'N/A': imdb = '0'
                    else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                    self.list[i].update({'imdb': imdb})
                except:
                    pass


            try: poster = item['poster_path']
            except: poster = ''
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (self.tmdb_poster, poster)
            if poster == '0':
                try: poster = client.parseDOM(item2, 'poster')[0]
                except: poster = '0'
                if not poster == '0': poster = self.tvdb_image + poster
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            if poster == '0' or poster == None:
                poster = self.getTVShowPosterFromGoogle(self.list[i]['title'], 3)
            if not poster == '0': self.list[i].update({'poster': poster})


            try: banner = client.parseDOM(item2, 'banner')[0]
            except: banner = ''
            if not banner == '': banner = self.tvdb_image + banner
            else: banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')
            if not banner == '0': self.list[i].update({'banner': banner})


            try: fanart = item['backdrop_path']
            except: fanart = ''
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
            if fanart == '0':
                try: fanart = client.parseDOM(item2, 'fanart')[0]
                except: fanart = '0'
                if not fanart == '0': fanart = self.tvdb_image + fanart
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0': self.list[i].update({'fanart': fanart})


            try: premiered = item['first_air_date']
            except: premiered = ''
            try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except: premiered = ''
            if premiered == '' or premiered == None:
                try: premiered = client.parseDOM(item2, 'FirstAired')[0]
                except: premiered = '0'
            if premiered == '': premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})


            try: studio = item['networks'][0]['name']
            except: studio = ''
            if studio == '' or studio == None:
                try: studio = client.parseDOM(item2, 'Network')[0]
                except: studio = ''
            if studio == '': studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})


            try: genre = item['genres']
            except: genre = []
            try: genre = [x['name'] for x in genre]
            except: genre = []
            if genre == '' or genre == None or genre == []:
                try: genre = client.parseDOM(item2, 'Genre')[0]
                except: genre = ''
                genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})


            try: duration = str(item['episode_run_time'][0])
            except: duration = ''
            if duration == '' or duration == None:
                try: duration = client.parseDOM(item2, 'Runtime')[0]
                except: duration = ''
            if duration == '': duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})


            try: rating = str(item['vote_average'])
            except: rating = ''
            if rating == '' or rating == None:
                try: rating = client.parseDOM(item2, 'Rating')[0]
                except: rating = ''
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})


            try: votes = str(item['vote_count'])
            except: votes = ''
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None:
                try: votes = client.parseDOM(item2, 'RatingCount')[0]
                except: votes = '0'
            if votes == '': votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})


            try: mpaa = item['content_ratings']['results'][-1]['rating']
            except: mpaa = ''
            if mpaa == '' or mpaa == None:
                try: mpaa = client.parseDOM(item2, 'ContentRating')[0]
                except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})


            try: cast = item['credits']['cast']
            except: cast = []
            try: cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except: cast = []
            if cast == []:
                try: cast = client.parseDOM(item2, 'Actors')[0]
                except: cast = ''
                cast = [x for x in cast.split('|') if not x == '']
                try: cast = [(x.encode('utf-8'), '') for x in cast]
                except: cast = []
            if len(cast) > 0: self.list[i].update({'cast': cast})


            try: plot = item['overview']
            except: plot = ''
            if plot == '' or plot == None:
                try: plot = client.parseDOM(item2, 'Overview')[0]
                except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})


            self.meta.append({'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': self.info_lang, 'item': {'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'tvrage': tvrage, 'poster': poster, 'banner': banner, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}})
        except:
            pass

    def tvshowDirectory(self, items):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('host_select') == '1' else False

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        sysaddon = sys.argv[0]

        for i in items:
            try:
                label = i['name']
                systitle = sysname = urllib.quote_plus(i['title'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tmdb, tvdb, tvrage, year = i['imdb'], i['tmdb'], i['tvdb'], i['tvrage'], i['year']
                try :sysurl, sysprovider = urllib.quote_plus(i['url']), i['provider']
                except:pass

                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster




                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                sysmeta = urllib.quote_plus(json.dumps(meta))

                action = 'episodes'
                #if not (tvdb == '0' or tvdb == 'None'):
                #    action = 'seasons'
                url = '%s?action=%s&provider=%s&url=%s&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s' % (sysaddon, action, sysprovider, sysurl, systitle, year, imdb, tmdb, tvdb, tvrage)

                cm = []

                if isFolder == False:
                    cm.append((control.lang(30232).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((control.lang(30233).encode('utf-8'), 'Action(Info)'))

                if not action == 'tvSearch':
                    cm.append((control.lang(30234).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, year, imdb, tvdb)))
                    cm.append((control.lang(30235).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, year, imdb, tvdb)))

                cm.append((control.lang(30240).encode('utf-8'), 'RunPlugin(%s?action=addView&content=tvshows)' % sysaddon))

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setInfo(type='Video', infoLabels = meta)
                item.setProperty('Video', 'true')
                item.addContextMenuItems(cm, replaceItems=True)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(int(sys.argv[1]), 'tvshows')
        views.setView('tvshows', {'skin.confluence': control.viewMode['mediainfo1']})
        control.directory(int(sys.argv[1]), cacheToDisc=True)

    def getTVShowPosterFromGoogle(self, showName, retry):
        if retry == 0:
            return ''
        #baseURL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={query}'

        keyBing = 'btcCcvQ4Sfo9P2Q7u62eOREA1NfLEQPezqCNb+2LVhY'        # get Bing key from: https://datamarket.azure.com/account/keys
        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds

        headers = {}
        headers['Authorization'] = credentialBing

        baseURL = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?Query=%27{query}%27&$format=json'

        query = showName.lower() + ' poster'
        url = baseURL.format(query=urllib.quote_plus(query))
        try:
            result = client.source(url, headers=headers)

            results = json.loads(result)['d']['results']

            for image_info in results:
                iconImage = image_info['MediaUrl']
                break
            if iconImage is not None:
                return iconImage
            else:
                return '0'
        except :
            return self.getTVShowPosterFromGoogle(showName, retry-1)
        return ''

    def addDirectory(self, items):
        if items == None or len(items) == 0: return

        sysaddon = sys.argv[0]
        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()

        for i in items:
            try:
                try: name = control.lang(i['name']).encode('utf-8')
                except: name = i['name']

                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                #try: cm.append((control.lang(30239).encode('utf-8'), 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                #except: pass

                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems(cm, replaceItems=False)
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass

        views.setView('tvshows', {'skin.confluence': control.viewMode['mediainfo1']})
        control.directory(int(sys.argv[1]), cacheToDisc=True)