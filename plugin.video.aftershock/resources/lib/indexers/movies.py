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


import os, sys, re, json, urllib, urlparse, base64, datetime

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import metacache
from resources.lib.libraries import workers
from resources.lib.libraries import views
from resources.lib.libraries import logger

class movies:
    def __init__(self):
        self.list = []

        self.tmdb_link = 'http://api.themoviedb.org'
        self.imdb_link = 'http://www.imdb.com'
        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.imdb_user = control.setting('imdb_user').replace('ur', '')
        self.info_lang = control.setting('infoLang') or 'en'

        self.tmdb_info_link = 'http://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases' % ('%s', self.tmdb_key, self.info_lang)
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'

        self.search_link = 'http://api.themoviedb.org/3/search/movie?api_key=%s&query=%s'

    def get(self, url, idx=True, provider=None, lang=None):
        try:
            if not provider == None:
                call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
                self.list = cache.get(call.scn_full_list, 24, url, lang, provider)
                self.worker()

            if idx == True: self.movieDirectory(self.list, provider, lang)
            return self.list
        except:
            pass

    def tmdb_list(self, url):
        try:
            result = client.request(url % self.tmdb_key)
            result = json.loads(result)
            items = result['results']
        except:
            return

        try:
            next = str(result['page'])
            total = str(result['total_pages'])
            if next == total: raise Exception()
            if not 'page=' in url: raise Exception()
            next = '%s&page=%s' % (url.split('&page=', 1)[0], str(int(next)+1))
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')

                except: pass

                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                poster = item['poster_path']
                if poster == '' or poster == None: raise Exception()
                else: poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')

                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')

                premiered = item['release_date']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')

                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')

                votes = str(item['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')

                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'name': name, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'tvrage': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass

        return self.list

    def search(self, query=None, lang=None):
        try:
            if query == None:
                t = control.lang(30201).encode('utf-8')
                k = control.keyboard('', t) ; k.doModal()
                self.query = k.getText() if k.isConfirmed() else None
            else:
                self.query = query

            if (self.query == None or self.query == ''): return

            url = self.search_link % ('%s', urllib.quote_plus(self.query))
            self.list = cache.get(self.tmdb_list, 0, url)

            self.worker()
            self.movieDirectory(self.list)
            return self.list
        except:
            return

    def genres(self, lang=None):
        try:
            self.list = []
            provider = '%s_mv' % control.setting('idx_provider')
            call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
            genres = call.genres
            url = call.genre_url
            keys = genres.keys()
            for i in keys:
                self.list.append({'name':i, 'image':i[:3].lower()+'.png', 'action':'movies&provider=%s&lang=%s' % (provider, lang), 'url':url % (lang, genres[i])})
            self.list.sort()
            self.addDirectory(self.list)
            return self.list
        except:
            return

    def years(self, lang=None):
        year = (self.datetime.strftime('%Y'))
        provider = '%s_mv' % control.setting('idx_provider')
        call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
        year_url = call.years_url
        for i in range(int(year)-0, int(year)-50, -1): self.list.append({'name': str(i), 'url': year_url % (lang, str(i)), 'image': str(i)+'.png', 'action': 'movies&provider=%s&lang=%s' % (provider, lang)})
        self.addDirectory(self.list)
        return self.list

    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetchImdb(self.list)
        self.list = metacache.fetch(self.list, self.info_lang)

        itemsPerPage = 25
        for r in range(0, total, itemsPerPage):
            threads = []
            for i in range(r, r+itemsPerPage):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        metacache.insertImdb(self.list)
        #self.list = [i for i in self.list if not (i['imdb'] == '0' and i['tmdb'] == '0')]

        if len(self.meta) > 0: metacache.insert(self.meta)

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            try: imdb = self.list[i]['imdb']
            except: imdb = '0'
            try: tmdb = self.list[i]['tmdb']
            except: tmdb = '0'

            if not tmdb == '0': url = self.tmdb_info_link % tmdb
            elif not imdb == '0': url = self.tmdb_info_link % imdb
            else:
                try :
                    year = self.list[i]['year']
                    years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
                    year = " ".join(years)
                    url = self.imdb_by_query % (urllib.quote_plus(self.list[i]['title']), urllib.quote_plus(year))
                    item = client.request(url, timeout='10')
                    item = json.loads(item)
                    imdb = item['imdbID']
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                    try : poster = item['Poster']
                    except:poster=self.list[i]['poster']
                    self.list[i].update({"tmdb":'0', "imdb":imdb, "poster":poster})
                    url = self.tmdb_info_link % imdb
                except:
                    self.list[i].update({"tmdb":'0', "imdb":'0'})
                    raise Exception()

            item = client.request(url, timeout='10', error=True, debug=True)
            item = json.loads(item)

            tmdb = item['id']
            if tmdb == '' or tmdb == None: tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0': self.list[i].update({'tmdb': tmdb})

            imdb = item['imdb_id']
            if imdb == '' or imdb == None: imdb = '0'
            if not imdb == '0': imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            if not imdb == '0': self.list[i].update({'imdb': imdb, 'code': imdb})

            poster = item['poster_path']
            if poster == '' or poster == 'N/A' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            fanart = item['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0': self.list[i].update({'fanart': fanart})

            premiered = item['release_date']
            try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except: premiered = '0'
            if premiered == '' or premiered == None: premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            studio = item['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            genre = item['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: duration = str(item['runtime'])
            except: duration = '0'
            if duration == '' or duration == None: duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(item['vote_average'])
            if rating == '' or rating == None: rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = str(item['vote_count'])
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None: votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            mpaa = item['releases']['countries']
            try: mpaa = [x for x in mpaa if not x['certification'] == '']
            except: mpaa = '0'
            try: mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except: mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            director = item['credits']['crew']
            try: director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except: director = '0'
            if director == '' or director == None or director == []: director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0': self.list[i].update({'director': director})

            writer = item['credits']['crew']
            try: writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except: writer = '0'
            try: writer = [x for n,x in enumerate(writer) if x not in writer[:n]]
            except: writer = '0'
            if writer == '' or writer == None or writer == []: writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0': self.list[i].update({'writer': writer})

            cast = item['credits']['cast']
            try: cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except: cast = []
            if len(cast) > 0: self.list[i].update({'cast': cast})

            plot = item['overview']
            if plot == '' or plot == None: plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = item['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            try: tagline = tagline.encode('utf-8')
            except: pass
            if not tagline == '0': self.list[i].update({'tagline': tagline})

            self.meta.append({'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'tvrage': '0', 'lang': self.info_lang, 'item': {'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
        except:
            pass

    def movieDirectory(self, items, provider=None, lang=None):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('autoplay') == 'false' and control.setting('host_select') == '1' else False
        isFolder = False if control.window.getProperty('PseudoTVRunning') == 'True' else isFolder

        playbackMenu = control.lang(30204).encode('utf-8') if control.setting('autoplay') == 'true' else control.lang(30203).encode('utf-8')

        cacheToDisc = False if not action == 'movieSearch' else True

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        sysaddon = sys.argv[0]

        try:
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(tmdb_api_key=self.tmdb_key, preparezip=False)
        except:
            pass

        for i in items:
            try:
                label = i['name']
                sysname = urllib.quote_plus(label)
                systitle = urllib.quote_plus(i['title'])
                imdb, tmdb, year = i['imdb'], i['tmdb'], i['year']


                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster


                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '120'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                sysmeta = urllib.quote_plus(json.dumps(meta))


                url = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&meta=%s&t=%s' % (sysaddon, sysname, systitle, year, imdb, tmdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                if isFolder == True:
                    url = '%s?action=sources&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&meta=%s' % (sysaddon, sysname, systitle, year, imdb, tmdb, sysmeta)


                try:
                    playcount = metaget._get_watched('movie', imdb, '', '')
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                cm = []

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                cm.append((control.lang(30214).encode('utf-8'), 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, sysname)))
                cm.append((control.lang(30205).encode('utf-8'), 'Action(Info)'))

                if not action == 'movieSearch':
                    cm.append((control.lang(30206).encode('utf-8'), 'RunPlugin(%s?action=moviePlaycount&title=%s&year=%s&imdb=%s&query=7)' % (sysaddon, systitle, year, imdb)))
                    cm.append((control.lang(30207).encode('utf-8'), 'RunPlugin(%s?action=moviePlaycount&title=%s&year=%s&imdb=%s&query=6)' % (sysaddon, systitle, year, imdb)))#

                cm.append((control.lang(30212).encode('utf-8'), 'RunPlugin(%s?action=addView&content=movies)' % sysaddon))


                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'banner': banner})
                except: pass

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setInfo(type='Video', infoLabels = meta)
                item.setProperty('Video', 'true')
                #item.setProperty('IsPlayable', 'true')
                item.addContextMenuItems(cm, replaceItems=True)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()
            url = '%s?action=movies&url=%s&provider=%s&lang=%s' % (sysaddon, urllib.quote_plus(url), provider, lang)
            addonNext = control.addonNext()
            item = control.item(label=control.lang(30213).encode('utf-8'), iconImage=addonNext, thumbnailImage=addonNext)
            item.addContextMenuItems([], replaceItems=False)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
        except:
            pass


        control.content(int(sys.argv[1]), 'movies')
        views.setView('movies', {'skin.confluence': control.viewMode['thumbnails']})
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)

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

                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems(cm, replaceItems=False)
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass
        views.setView('movies', {'skin.confluence': control.viewMode['thumbnails']})
        control.directory(int(sys.argv[1]), cacheToDisc=True)