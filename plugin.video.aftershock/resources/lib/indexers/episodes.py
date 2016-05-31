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


import os,sys,re,json,zipfile,StringIO,urllib,urllib2,base64,datetime

from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import views
from resources.lib.libraries import logger

class seasons:
    def __init__(self):
        self.list = []

        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=')
        self.tvdb_key = base64.urlsafe_b64decode('OUZDQkM2MjlEQzgyRjA4Qw==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.info_lang = control.setting('infoLang') or 'en'

        self.tmdb_info_link = 'http://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=credits,content_ratings,external_ids' % ('%s', self.tmdb_key, '%s')
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/all/%s.zip' % (self.tvdb_key, '%s', '%s')
        self.tmdb_by_imdb = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ('%s', self.tmdb_key)
        self.tmdb_by_tvdb = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=tvdb_id' % ('%s', self.tmdb_key)
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_poster = 'http://thetvdb.com/banners/_cache/'


    def get(self, tvshowtitle, year, imdb, tmdb, tvdb, tvrage, idx=True):
        if idx == True:
            self.list = cache.get(self.tvdb_list, 24, tvshowtitle, year, imdb, tmdb, tvdb, tvrage, self.info_lang)
            self.seasonDirectory(self.list)
            return self.list
        else:
            self.list = self.tvdb_list(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, self.info_lang)
            return self.list


    def tvdb_list(self, tvshowtitle, year, imdb, tmdb, tvdb, tvrage, lang, limit=''):
        try:
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
                tvdb = tvdb.encode('utf-8')


            if tmdb == '0' and not imdb == '0':
                url = self.tmdb_by_imdb % imdb
                result = client.request(url, timeout='10')
                result = json.loads(result)

                tmdb = result['tv_results'][0]['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                if not tmdb == '0':
                    url = self.tmdb_info_link % (tmdb, lang)

                    item = client.request(url, timeout='10')
                    item = json.loads(item)

                    tvdb = item['external_ids']['tvdb_id']
                    if tvdb == '' or tvdb == None: tvdb = '0'
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                    tvdb = tvdb.encode('utf-8')
        except:
            pass


        try:
            try: item = item
            except: item = ''
            if limit == '-2' or not item == '': raise Exception()

            if tmdb == '0' and not imdb == '0':
                url = self.tmdb_by_imdb % imdb
                result = client.request(url, timeout='10')
                result = json.loads(result)

                tmdb = result['tv_results'][0]['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')


            if tmdb == '0' and not tvdb == '0':
                url = self.tmdb_by_tvdb % tvdb
                result = client.request(url, timeout='10')
                result = json.loads(result)

                tmdb = result['tv_results'][0]['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')



            if tmdb == '0': raise Exception()

            url = self.tmdb_info_link % (tmdb, lang)

            item = client.request(url, timeout='10')
            item = json.loads(item)
        except:
            pass


        try:
            if tvdb == '0': raise Exception()

            tvdb_lang = re.sub('bg', 'en', lang)

            url = self.tvdb_info_link % (tvdb, tvdb_lang)
            data = urllib2.urlopen(url, timeout=30).read()

            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read('%s.xml' % tvdb_lang)
            artwork = zip.read('banners.xml')
            zip.close()

            dupe = client.parseDOM(result, 'SeriesName')[0]
            dupe = re.compile('[***]Duplicate (\d*)[***]').findall(dupe)
            if len(dupe) > 0:
                tvdb = str(dupe[0]).encode('utf-8')
                url = self.tvdb_info_link % (tvdb, tvdb_lang)
                data = urllib2.urlopen(url, timeout=30).read()
                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('%s.xml' % tvdb_lang)
                artwork = zip.read('banners.xml')
                zip.close()


            artwork = artwork.split('<Banner>')
            artwork = [i for i in artwork if '<Language>en</Language>' in i and '<BannerType>season</BannerType>' in i]
            artwork = [i for i in artwork if not 'seasonswide' in re.compile('<BannerPath>(.+?)</BannerPath>').findall(i)[0]]

            result = result.split('<Episode>')

            item2 = result[0]
            episodes = [i for i in result if '<EpisodeNumber>' in i]
            episodes = [i for i in episodes if not '<SeasonNumber>0</SeasonNumber>' in i]
            episodes = [i for i in episodes if not '<EpisodeNumber>0</EpisodeNumber>' in i]
            seasons = [i for i in episodes if '<EpisodeNumber>1</EpisodeNumber>' in i]

            result = ''

            if limit == '':
                episodes = []
            elif limit == '-1' or  limit == '-2':
                seasons = []
            else:
                episodes = [i for i in episodes if '<SeasonNumber>%01d</SeasonNumber>' % int(limit) in i]
                seasons = []


            try: poster = item['poster_path']
            except: poster = ''
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = self.tmdb_poster + poster
            if poster == '0':
                try: poster = client.parseDOM(item2, 'poster')[0]
                except: poster = ''
                if not poster == '': poster = self.tvdb_image + poster
                else: poster = '0'
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = client.parseDOM(item2, 'banner')[0]
            except: banner = ''
            if not banner == '': banner = self.tvdb_image + banner
            else: banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = item['backdrop_path']
            except: fanart = ''
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = self.tmdb_image + fanart
            if fanart == '0':
                try: fanart = client.parseDOM(item2, 'fanart')[0]
                except: fanart = ''
                if not fanart == '': fanart = self.tvdb_image + fanart
                else: fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            if not poster == '0': pass
            elif not fanart == '0': poster = fanart
            elif not banner == '0': poster = banner

            if not banner == '0': pass
            elif not fanart == '0': banner = fanart
            elif not poster == '0': banner = poster

            try: tvrage2 = item['external_ids']['tvrage_id']
            except: tvrage2 = '0'
            if tvrage == '0' or tvrage == None: tvrage = tvrage2
            if tvrage == '' or tvrage == None: tvrage = '0'
            tvrage = re.sub('[^0-9]', '', str(tvrage))
            tvrage = tvrage.encode('utf-8')

            try: status = client.parseDOM(item2, 'Status')[0]
            except: status = ''
            if status == '': status = 'Ended'
            status = client.replaceHTMLCodes(status)
            status = status.encode('utf-8')

            try: alter = client.parseDOM(item2, 'Genre')[0]
            except: alter = '0'
            if any(x in alter for x in ['Documentary', 'Reality', 'Game Show', 'Talk Show']): alter = '1'
            else: alter = '0'
            alter = alter.encode('utf-8')

            try: studio = item['networks'][0]['name']
            except: studio = ''
            if studio == '' or studio == None:
                try: studio = client.parseDOM(item2, 'Network')[0]
                except: studio = ''
            if studio == '': studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

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

            try: duration = str(item['episode_run_time'][0])
            except: duration = ''
            if duration == '' or duration == None:
                try: duration = client.parseDOM(item2, 'Runtime')[0]
                except: duration = ''
            if duration == '': duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            try: rating = str(item['vote_average'])
            except: rating = ''
            if rating == '' or rating == None:
                try: rating = client.parseDOM(item2, 'Rating')[0]
                except: rating = ''
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

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

            try: mpaa = item['content_ratings']['results'][-1]['rating']
            except: mpaa = ''
            if mpaa == '' or mpaa == None:
                try: mpaa = client.parseDOM(item2, 'ContentRating')[0]
                except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

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

            try: plot = item['overview']
            except: plot = ''
            if plot == '' or plot == None:
                try: plot = client.parseDOM(item2, 'Overview')[0]
                except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
        except:
            return


        for item in seasons:
            try:
                premiered = client.parseDOM(item, 'FirstAired')[0]
                if premiered == '' or '-00' in premiered: premiered = '0'
                premiered = client.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                if status == 'Ended': pass
                elif premiered == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))): raise Exception()

                season = client.parseDOM(item, 'SeasonNumber')[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                thumb = [i for i in artwork if client.parseDOM(i, 'Season')[0] == season]
                try: thumb = client.parseDOM(thumb[0], 'BannerPath')[0]
                except: thumb = ''
                if not thumb == '': thumb = self.tvdb_image + thumb
                else: thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if thumb == '0': thumb = poster

                self.list.append({'season': season, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'tvrage': tvrage, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb})
            except:
                pass


        for item in episodes:
            try:
                premiered = client.parseDOM(item, 'FirstAired')[0]
                if premiered == '' or '-00' in premiered: premiered = '0'
                premiered = client.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                if status == 'Ended': pass
                elif premiered == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))): raise Exception()

                season = client.parseDOM(item, 'SeasonNumber')[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                episode = client.parseDOM(item, 'EpisodeNumber')[0]
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                episode = episode.encode('utf-8')

                title = client.parseDOM(item, 'EpisodeName')[0]
                if title == '': title = '0'
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                name = '%s S%02dE%02d' % (tvshowtitle, int(season), int(episode))
                try: name = name.encode('utf-8')
                except: pass

                try: thumb = client.parseDOM(item, 'filename')[0]
                except: thumb = ''
                if not thumb == '': thumb = self.tvdb_image + thumb
                else: thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not thumb == '0': pass
                elif not fanart == '0': thumb = fanart.replace(self.tmdb_image, self.tmdb_poster).replace(self.tvdb_image, self.tvdb_poster)
                elif not poster == '0': thumb = poster

                try: rating = client.parseDOM(item, 'Rating')[0]
                except: rating = ''
                if rating == '': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: director = client.parseDOM(item, 'Director')[0]
                except: director = ''
                director = [x for x in director.split('|') if not x == '']
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: writer = client.parseDOM(item, 'Writer')[0]
                except: writer = ''
                writer = [x for x in writer.split('|') if not x == '']
                writer = ' / '.join(writer)
                if writer == '': writer = '0'
                writer = client.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')

                try: episodeplot = client.parseDOM(item, 'Overview')[0]
                except: episodeplot = ''
                if episodeplot == '': episodeplot = '0'
                if episodeplot == '0': episodeplot = plot
                episodeplot = client.replaceHTMLCodes(episodeplot)
                try: episodeplot = episodeplot.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'alter': alter, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': episodeplot, 'name': name, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'tvrage': tvrage, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb})
            except:
                pass

        return self.list


    def seasonDirectory(self, items):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('autoplay') == 'false' and control.setting('host_select') == '1' else False
        isFolder = False if control.window.getProperty('PseudoTVRunning') == 'True' else isFolder

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        sysaddon = sys.argv[0]

        for i in items:
            try:
                label = '%s %s' % ('Season', i['season'])
                systitle = sysname = urllib.quote_plus(i['tvshowtitle'])
                imdb, tmdb, tvdb, tvrage, year, season = i['imdb'], i['tmdb'], i['tvdb'], i['tvrage'], i['year'], i['season']

                poster, banner, fanart, thumb = i['poster'], i['banner'], i['fanart'], i['thumb']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster
                if thumb == '0' and poster == '0': thumb = addonPoster
                elif thumb == '0': thumb = poster

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                sysmeta = urllib.quote_plus(json.dumps(meta))


                url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s' % (sysaddon, systitle, year, imdb, tmdb, tvdb, tvrage, season)


                cm = []

                if isFolder == False:
                    cm.append((control.lang(30261).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((control.lang(30262).encode('utf-8'), 'Action(Info)'))

                cm.append((control.lang(30263).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s&query=7)' % (sysaddon, systitle, year, imdb, tvdb, season)))
                cm.append((control.lang(30264).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s&query=6)' % (sysaddon, systitle, year, imdb, tvdb, season)))

                #cm.append((control.lang(30267).encode('utf-8'), 'RunPlugin(%s?action=deleteFavourite&meta=%s&content=tvshows)' % (sysaddon, sysmeta)))

                #cm.append((control.lang(30268).encode('utf-8'), 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s)' % (sysaddon, systitle, year, imdb, tmdb, tvdb, tvrage)))

                cm.append((control.lang(30269).encode('utf-8'), 'RunPlugin(%s?action=addView&content=seasons)' % sysaddon))


                item = control.item(label=label, iconImage=thumb, thumbnailImage=thumb)

                try: item.setArt({'poster': thumb, 'tvshow.poster': poster, 'season.poster': thumb, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
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


        try: control.property(int(sys.argv[1]), 'showplot', items[0]['plot'])
        except: pass

        control.content(int(sys.argv[1]), 'seasons')
        control.directory(int(sys.argv[1]), cacheToDisc=True)
        views.setView('seasons', {'skin.confluence': 500})


class episodes:
    def __init__(self):
        self.list = []

        self.trakt_link = 'http://api-v2launch.trakt.tv'
        self.tvdb_key = base64.urlsafe_b64decode('OUZDQkM2MjlEQzgyRjA4Qw==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt_user')
        self.info_lang = control.setting('infoLang') or 'en'

        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/all/%s.zip' % (self.tvdb_key, '%s', '%s')
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_poster = 'http://thetvdb.com/banners/_cache/'

        self.mycalendar_link = 'http://api-v2launch.trakt.tv/calendars/my/shows/%s/31/' % (self.datetime - datetime.timedelta(days = 32)).strftime('%Y-%m-%d')
        self.progress_link = 'http://api-v2launch.trakt.tv/users/%s/watched/shows' % self.trakt_user
        self.calendar_link = 'http://api-v2launch.trakt.tv/calendars/all/shows/%s/%s'

        self.scn_link = 'http://m2v.ru'
        self.added_link = 'http://m2v.ru/?Part=11&func=part&page=1'

    def get(self, tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season=None, episode=None, idx=True, provider=None, url=None):
        try:
            if idx == True:
                #if not (tvdb == None or tvdb == '0') :
                    #self.list = cache.get(seasons().tvdb_list, 1, tvshowtitle, year, imdb, tmdb, tvdb, tvrage, self.info_lang, season)
                #else :
                if not provider == None:
                    call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
                    self.list = call.get_episodes(tvshowtitle, url)
                    if self.list == [] : raise Exception(control.lang(30516).encode('utf-8'))
                    self.list = self.super_info(self.list)

                self.episodeDirectory(self.list, provider)
                return self.list
        except Exception as e:
            logger.error(e)
            control.infoDialog(control.lang(30516).encode('utf-8'))
            pass

    def super_info(self, items):
        try :
            for i in range(0, len(items)):
                self.list[i].update({'season':'0', 'episode':'0','imdb':'0', 'tmdb':'0', 'tvdb':'0', 'tvrage':'0', 'year':'0', 'alter':'0','poster':'0', 'banner':'0', 'fanart':'0', 'thumb':'0', 'premiered':'0', 'duration':'30'})
            return self.list
        except:
            pass

    def episodeDirectory(self, items, provider=None):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('autoplay') == 'false' and control.setting('host_select') == '1' else False
        isFolder = False if control.window.getProperty('PseudoTVRunning') == 'True' else isFolder

        playbackMenu = control.lang(30271).encode('utf-8') if control.setting('autoplay') == 'true' else control.lang(30270).encode('utf-8')

        cacheToDisc = False

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        sysaddon = sys.argv[0]

        try: multi = [i['tvshowtitle'] for i in items]
        except: multi = []
        multi = len([x for y,x in enumerate(multi) if x not in multi[:y]])
        multi = True if multi > 1 else False

        try: sysaction = items[0]['action']
        except: sysaction = ''

        for i in items:
            try:
                try :
                    if i['title'] == '0':
                        label = '%sx%02d . %s %s' % (i['season'], int(i['episode']), 'Episode', i['episode'])
                    else:
                        label = '%sx%02d . %s' % (i['season'], int(i['episode']), i['title'])
                except:
                    label = i['title']
                if multi == True:
                    label = '%s - %s' % (i['tvshowtitle'], label)

                systitle = sysname = urllib.quote_plus(i['tvshowtitle'])
                episodetitle, episodename = urllib.quote_plus(i['title']), urllib.quote_plus(i['name'])
                syspremiered = urllib.quote_plus(i['premiered'])
                imdb, tmdb, tvdb, tvrage, year, season, episode, alter = i['imdb'], i['tmdb'], i['tvdb'], i['tvrage'], i['year'], i['season'], i['episode'], i['alter']

                poster, banner, fanart, thumb = i['poster'], i['banner'], i['fanart'], i['thumb']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster
                if thumb == '0' and fanart == '0': thumb = addonFanart
                elif thumb == '0': thumb = fanart

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&tvshowtitle=%s&alter=%s&date=%s&meta=%s&t=%s' % (sysaddon, episodename, episodetitle, year, imdb, tmdb, tvdb, tvrage, season, episode, systitle, alter, syspremiered, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                if isFolder == True:
                    url = '%s?action=sources&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&tvshowtitle=%s&alter=%s&date=%s&meta=%s&provider=%s' % (sysaddon, episodename, episodetitle, year, imdb, tmdb, tvdb, tvrage, season, episode, systitle, alter, syspremiered, sysmeta, provider)

                if sysaction == 'episodes':
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s' % (sysaddon, systitle, year, imdb, tmdb, tvdb, tvrage, season, episode)
                    isFolder = True ; cacheToDisc = True

                cm = []

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isFolder == False:
                    cm.append((control.lang(30261).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((control.lang(30272).encode('utf-8'), 'Action(Info)'))

                if multi == True:
                    cm.append((control.lang(30274).encode('utf-8'), 'ActivateWindow(Videos,%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s,return)' % (sysaddon, systitle, year, imdb, tmdb, tvdb, tvrage)))

                cm.append((control.lang(30263).encode('utf-8'), 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=7)' % (sysaddon, imdb, tvdb, season, episode)))
                cm.append((control.lang(30264).encode('utf-8'), 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=6)' % (sysaddon, imdb, tvdb, season, episode)))

                #cm.append((control.lang(30268).encode('utf-8'), 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s)' % (sysaddon, systitle, year, imdb, tmdb, tvdb, tvrage)))

                cm.append((control.lang(30273).encode('utf-8'), 'RunPlugin(%s?action=addView&content=episodes)' % sysaddon))

                item = control.item(label=label, iconImage=thumb, thumbnailImage=thumb)

                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setInfo(type='Video', infoLabels = meta)
                item.setProperty('Video', 'true')
                #item.setProperty('IsPlayable', 'true')
                item.setProperty('resumetime',str(0))
                item.setProperty('totaltime',str(1))
                item.addContextMenuItems(cm, replaceItems=True)

                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()
            url = '%s?action=episodes&tvshowtitle=%s&url=%s&provider=%s' % (sysaddon, systitle, urllib.quote_plus(url), provider)
            addonNext = control.addonNext()
            item = control.item(label=control.lang(30213).encode('utf-8'), iconImage=addonNext, thumbnailImage=addonNext)
            item.addContextMenuItems([], replaceItems=False)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(int(sys.argv[1]), 'episodes')
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        views.setView('episodes', {'skin.confluence': 504})

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

                if not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems([], replaceItems=False)
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass

        control.directory(int(sys.argv[1]), cacheToDisc=True)