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


from resources.lib.modules import trakt
from resources.lib.modules import cleantitle
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views

import os,sys,re,json,zipfile,StringIO,urllib,urllib2,urlparse,base64,datetime

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

control.moderator()


class seasons:
    def __init__(self):
        self.list = []

        self.lang = control.apiLanguage()['tvdb']
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')

        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/all/%s.zip' % (self.tvdb_key, '%s', '%s')
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_poster = 'http://thetvdb.com/banners/_cache/'


    def get(self, tvshowtitle, year, imdb, tvdb, idx=True):
        if idx == True:
            if control.setting('flatten.tvshows') == 'true' or control.window.getProperty('PseudoTVRunning') == 'True':
                self.list = cache.get(self.tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang, '-1')
                episodes().episodeDirectory(self.list)
                return self.list
            else:
                self.list = cache.get(self.tvdb_list, 24, tvshowtitle, year, imdb, tvdb, self.lang)
                self.seasonDirectory(self.list)
                return self.list
        else:
            self.list = self.tvdb_list(tvshowtitle, year, imdb, tvdb, 'en')
            return self.list


    def tvdb_list(self, tvshowtitle, year, imdb, tvdb, lang, limit=''):
        try:
            if imdb == '0':
                url = self.imdb_by_query % (urllib.quote_plus(tvshowtitle), year)

                imdb = client.request(url, timeout='10')
                try: imdb = json.loads(imdb)['imdbID']
                except: imdb = '0'

                if imdb == None or imdb == '' or imdb == 'N/A': imdb = '0'


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


            if tvdb == '0':
                url = self.tvdb_by_query % (urllib.quote_plus(tvshowtitle))

                years = [str(year), str(int(year)+1), str(int(year)-1)]

                tvdb = client.request(url, timeout='10')
                tvdb = re.sub(r'[^\x00-\x7F]+', '', tvdb)
                tvdb = client.replaceHTMLCodes(tvdb)
                tvdb = client.parseDOM(tvdb, 'Series')
                tvdb = [(x, client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired')) for x in tvdb]
                tvdb = [(x, x[1][0], x[2][0]) for x in tvdb if len(x[1]) > 0 and len(x[2]) > 0]
                tvdb = [x for x in tvdb if cleantitle.get(tvshowtitle) == cleantitle.get(x[1])]
                tvdb = [x[0][0] for x in tvdb if any(y in x[2] for y in years)][0]
                tvdb = client.parseDOM(tvdb, 'seriesid')[0]

                if tvdb == '': tvdb = '0'
        except:
            return


        try:
            if tvdb == '0': return

            url = self.tvdb_info_link % (tvdb, 'en')
            data = urllib2.urlopen(url, timeout=30).read()

            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read('%s.xml' % 'en')
            artwork = zip.read('banners.xml')
            zip.close()

            dupe = client.parseDOM(result, 'SeriesName')[0]
            dupe = re.compile('[***]Duplicate (\d*)[***]').findall(dupe)

            if len(dupe) > 0:
                tvdb = str(dupe[0]).encode('utf-8')

                url = self.tvdb_info_link % (tvdb, 'en')
                data = urllib2.urlopen(url, timeout=30).read()

                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('%s.xml' % 'en')
                artwork = zip.read('banners.xml')
                zip.close()

            if not lang == 'en':
                url = self.tvdb_info_link % (tvdb, lang)
                data = urllib2.urlopen(url, timeout=30).read()

                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result2 = zip.read('%s.xml' % lang)
                zip.close()
            else:
                result2 = result


            artwork = artwork.split('<Banner>')
            artwork = [i for i in artwork if '<Language>en</Language>' in i and '<BannerType>season</BannerType>' in i]
            artwork = [i for i in artwork if not 'seasonswide' in re.findall('<BannerPath>(.+?)</BannerPath>', i)[0]]


            result = result.split('<Episode>')
            result2 = result2.split('<Episode>')

            item = result[0] ; item2 = result2[0]

            episodes = [i for i in result if '<EpisodeNumber>' in i]
            episodes = [i for i in episodes if not '<SeasonNumber>0</SeasonNumber>' in i]
            episodes = [i for i in episodes if not '<EpisodeNumber>0</EpisodeNumber>' in i]

            seasons = [i for i in episodes if '<EpisodeNumber>1</EpisodeNumber>' in i]

            locals = [i for i in result2 if '<EpisodeNumber>' in i]

            result = '' ; result2 = ''

            if limit == '':
                episodes = []
            elif limit == '-1':
                seasons = []
            else:
                episodes = [i for i in episodes if '<SeasonNumber>%01d</SeasonNumber>' % int(limit) in i]
                seasons = []


            try: poster = client.parseDOM(item, 'poster')[0]
            except: poster = ''
            if not poster == '': poster = self.tvdb_image + poster
            else: poster = '0'
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = client.parseDOM(item, 'banner')[0]
            except: banner = ''
            if not banner == '': banner = self.tvdb_image + banner
            else: banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = client.parseDOM(item, 'fanart')[0]
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

            try: status = client.parseDOM(item, 'Status')[0]
            except: status = ''
            if status == '': status = 'Ended'
            status = client.replaceHTMLCodes(status)
            status = status.encode('utf-8')

            try: studio = client.parseDOM(item, 'Network')[0]
            except: studio = ''
            if studio == '': studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

            try: genre = client.parseDOM(item, 'Genre')[0]
            except: genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try: duration = client.parseDOM(item, 'Runtime')[0]
            except: duration = ''
            if duration == '': duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            try: rating = client.parseDOM(item, 'Rating')[0]
            except: rating = ''
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            try: votes = client.parseDOM(item, 'RatingCount')[0]
            except: votes = '0'
            if votes == '': votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')

            try: mpaa = client.parseDOM(item, 'ContentRating')[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            try: cast = client.parseDOM(item, 'Actors')[0]
            except: cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []

            try: label = client.parseDOM(item2, 'SeriesName')[0]
            except: label = '0'
            label = client.replaceHTMLCodes(label)
            label = label.encode('utf-8')

            try: plot = client.parseDOM(item2, 'Overview')[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
        except:
            pass


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

                self.list.append({'season': season, 'tvshowtitle': tvshowtitle, 'label': label, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb})
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

                try: thumb = client.parseDOM(item, 'filename')[0]
                except: thumb = ''
                if not thumb == '': thumb = self.tvdb_image + thumb
                else: thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not thumb == '0': pass
                elif not fanart == '0': thumb = fanart.replace(self.tvdb_image, self.tvdb_poster)
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

                try:
                    local = client.parseDOM(item, 'id')[0]
                    local = [x for x in locals if '<id>%s</id>' % str(local) in x][0]
                except:
                    local = item

                label = client.parseDOM(local, 'EpisodeName')[0]
                if label == '': label = '0'
                label = client.replaceHTMLCodes(label)
                label = label.encode('utf-8')

                try: episodeplot = client.parseDOM(local, 'Overview')[0]
                except: episodeplot = ''
                if episodeplot == '': episodeplot = '0'
                if episodeplot == '0': episodeplot = plot
                episodeplot = client.replaceHTMLCodes(episodeplot)
                try: episodeplot = episodeplot.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'label': label, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': episodeplot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb})
            except:
                pass

        return self.list


    def seasonDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try: isOld = False ; control.item().getArt('type')
        except: isOld = True

        isEstuary = True if 'estuary' in control.skin else False

        try: indicators = playcount.getSeasonIndicators(items[0]['imdb'])
        except: pass

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        labelMenu = control.lang(32055).encode('utf-8')


        for i in items:
            try:
                label = '%s %s' % (labelMenu, i['season'])
                systitle = sysname = urllib.quote_plus(i['tvshowtitle'])
                sysimage = urllib.quote_plus(i['thumb'])

                imdb, tvdb, year, season = i['imdb'], i['tvdb'], i['year'], i['season']


                poster, banner, fanart, thumb = i['poster'], i['banner'], i['fanart'], i['thumb']
                if banner == '0' and not fanart == '0': banner = fanart
                elif banner == '0' and not poster == '0': banner = poster
                if thumb == '0' and not poster == '0': thumb = poster
                elif thumb == '0' and not fanart == '0': thumb = fanart
                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if thumb == '0': thumb = addonPoster


                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                try: meta.update({'tvshowtitle': i['label']})
                except: pass
                if isEstuary == True:
                    try: del meta['cast']
                    except: pass

                try:
                    if season in indicators: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass


                url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s&season=%s' % (sysaddon, systitle, year, imdb, tvdb, season)


                cm = []

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&season=%s&query=7)' % (sysaddon, systitle, imdb, tvdb, season)))

                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&season=%s&query=6)' % (sysaddon, systitle, imdb, tvdb, season)))

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, sysname, tvdb)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))


                item = control.item(label=label)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                item.setArt({'icon': poster, 'thumb': poster, 'poster': thumb, 'tvshow.poster': poster, 'season.poster': thumb, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass


        try: control.property(syshandle, 'showplot', items[0]['plot'])
        except: pass

        control.content(syshandle, 'seasons')
        #control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)
        views.setView('seasons', {'skin.confluence': 500})


class episodes:
    def __init__(self):
        self.list = []

        self.trakt_link = 'http://api-v2launch.trakt.tv'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.lang = control.apiLanguage()['tvdb']

        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/all/%s.zip' % (self.tvdb_key, '%s', '%s')
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_poster = 'http://thetvdb.com/banners/_cache/'

        self.added_link = 'http://api-v2launch.trakt.tv/calendars/all/shows/date[6]/7/'
        self.mycalendar_link = 'http://api-v2launch.trakt.tv/calendars/my/shows/date[29]/60/'
        self.trakthistory_link = 'http://api-v2launch.trakt.tv/users/me/history/shows?limit=300'
        self.progress_link = 'http://api-v2launch.trakt.tv/users/me/watched/shows'
        self.calendar_link = 'http://api-v2launch.trakt.tv/calendars/all/shows/%s/%s'
        self.traktlists_link = 'http://api-v2launch.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api-v2launch.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'http://api-v2launch.trakt.tv/users/%s/lists/%s/items'


    def get(self, tvshowtitle, year, imdb, tvdb, season=None, episode=None, idx=True):
        try:
            if idx == True:
                if episode == None:
                    self.list = cache.get(seasons().tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang, season)
                else:
                    self.list = cache.get(seasons().tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang, '-1')
                    num = [x for x,y in enumerate(self.list) if y['season'] == str(season) and  y['episode'] == str(episode)][-1]
                    self.list = [y for x,y in enumerate(self.list) if x >= num]

                self.episodeDirectory(self.list)
                return self.list
            else:
                self.list = seasons().tvdb_list(tvshowtitle, year, imdb, tvdb, 'en', '-1')
                return self.list
        except:
            pass


    def calendar(self, url):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            if url in self.progress_link:
                self.blist = cache.get(self.trakt_progress_list, 720, url, self.trakt_user, self.lang)
                self.list = []
                self.list = cache.get(self.trakt_progress_list, 0, url, self.trakt_user, self.lang)
            elif '/users/' in url:
                self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                self.list = self.list[::-1]
            else:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)

            self.episodeDirectory(self.list)
            return self.list
        except:
            pass


    def widget(self):
        if trakt.getTraktIndicatorsInfo() == True:
            setting = control.setting('tv.widget.alt')
        else:
            setting = control.setting('tv.widget')

        if setting == '2':
            self.calendar(self.progress_link)
        elif setting == '3':
            self.calendar(self.mycalendar_link)
        else:
            self.calendar(self.added_link)


    def calendars(self):
        m = control.lang(32060).encode('utf-8').split('|')
        try: months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'), (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'), (m[10], 'November'), (m[11], 'December')]
        except: months = []

        d = control.lang(32061).encode('utf-8').split('|')
        try: days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'), (d[5], 'Saturday'), (d[6], 'Sunday')]
        except: days = []

        for i in range(0, 30):
            try:
                name = (self.datetime - datetime.timedelta(days = i))
                name = (control.lang(32062) % (name.strftime('%A'), name.strftime('%d %B'))).encode('utf-8')
                for m in months: name = name.replace(m[1], m[0])
                for d in days: name = name.replace(d[1], d[0])
                try: name = name.encode('utf-8')
                except: pass

                url = self.calendar_link % ((self.datetime - datetime.timedelta(days = i)).strftime('%Y-%m-%d'), '1')

                self.list.append({'name': name, 'url': url, 'image': 'calendar.png', 'action': 'calendar'})
            except:
                pass
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'calendar'})
        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full,images'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTrakt(u)

            itemlist = []
            items = json.loads(result)
        except:
            return

        for item in items:
            try:
                title = item['episode']['title']
                if title == None or title == '': raise Exception()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                season = item['episode']['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0': raise Exception()
                season = season.encode('utf-8')

                episode = item['episode']['number']
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                if episode == '0': raise Exception()
                episode = episode.encode('utf-8')

                tvshowtitle = item['show']['title']
                if tvshowtitle == None or tvshowtitle == '': raise Exception()
                tvshowtitle = client.replaceHTMLCodes(tvshowtitle)
                tvshowtitle = tvshowtitle.encode('utf-8')

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'
                else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = item['show']['ids']['tvdb']
                if tvdb == None or tvdb == '': raise Exception()
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                poster = '0'
                try: poster = item['show']['images']['poster']['medium']
                except: pass
                if poster == None or not '/posters/' in poster: poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = poster.encode('utf-8')

                banner = poster
                try: banner = item['show']['images']['banner']['full']
                except: pass
                if banner == None or not '/banners/' in banner: banner = poster
                banner = banner.rsplit('?', 1)[0]
                banner = banner.encode('utf-8')

                fanart = '0'
                try: fanart = item['show']['images']['fanart']['full']
                except: pass
                if fanart == None or not '/fanarts/' in fanart: fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = fanart.encode('utf-8')

                thumb1 = item['episode']['images']['screenshot']['thumb']
                thumb2 = item['show']['images']['thumb']['full']
                if '/screenshots/' in thumb1: thumb = thumb1
                elif '/thumbs/' in thumb2: thumb = thumb2
                else: thumb = fanart
                thumb = thumb.rsplit('?', 1)[0]
                try: thumb = thumb.encode('utf-8')
                except: pass

                premiered = item['episode']['first_aired']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')

                studio = item['show']['network']
                if studio == None: studio = '0'
                studio = studio.encode('utf-8')

                genre = item['show']['genres']
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                try: duration = str(item['show']['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'
                duration = duration.encode('utf-8')

                try: rating = str(item['episode']['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = rating.encode('utf-8')

                try: votes = str(item['show']['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'
                votes = votes.encode('utf-8')

                mpaa = item['show']['certification']
                if mpaa == None: mpaa = '0'
                mpaa = mpaa.encode('utf-8')

                plot = item['episode']['overview']
                if plot == None or plot == '': plot = item['show']['overview']
                if plot == None or plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                itemlist.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': 'Continuing', 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb})
            except:
                pass

        itemlist = itemlist[::-1]

        return itemlist


    def trakt_progress_list(self, url, user, lang):
        try:
            url += '?extended=full'
            result = trakt.getTrakt(url)
            result = json.loads(result)
            items = []
        except:
            return

        for item in result:
            try:
                num_1 = 0
                for i in range(0, len(item['seasons'])): num_1 += len(item['seasons'][i]['episodes'])
                num_2 = int(item['show']['aired_episodes'])
                if num_1 >= num_2: raise Exception()

                season = str(item['seasons'][-1]['number'])
                season = season.encode('utf-8')

                episode = str(item['seasons'][-1]['episodes'][-1]['number'])
                episode = episode.encode('utf-8')

                tvshowtitle = item['show']['title']
                if tvshowtitle == None or tvshowtitle == '': raise Exception()
                tvshowtitle = client.replaceHTMLCodes(tvshowtitle)
                tvshowtitle = tvshowtitle.encode('utf-8')

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(self.datetime.strftime('%Y')): raise Exception()

                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '': raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = item['show']['ids']['tvdb']
                if tvdb == None or tvdb == '': raise Exception()
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                items.append({'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'snum': season, 'enum': episode})
            except:
                pass


        def items_list(i):
            try:
                item = [x for x in self.blist if x['tvdb'] == i['tvdb'] and x['snum'] == i['snum'] and x['enum'] == i['enum']][0]
                item['action'] = 'episodes'
                self.list.append(item)
                return
            except:
                pass

            try:
                url = self.tvdb_info_link % (i['tvdb'], lang)
                data = urllib2.urlopen(url, timeout=10).read()

                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('%s.xml' % lang)
                artwork = zip.read('banners.xml')
                zip.close()

                result = result.split('<Episode>')
                item = [x for x in result if '<EpisodeNumber>' in x]
                item2 = result[0]

                num = [x for x,y in enumerate(item) if re.compile('<SeasonNumber>(.+?)</SeasonNumber>').findall(y)[0] == str(i['snum']) and re.compile('<EpisodeNumber>(.+?)</EpisodeNumber>').findall(y)[0] == str(i['enum'])][-1]
                item = [y for x,y in enumerate(item) if x > num][0]


                premiered = client.parseDOM(item, 'FirstAired')[0]
                if premiered == '' or '-00' in premiered: premiered = '0'
                premiered = client.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                try: status = client.parseDOM(item2, 'Status')[0]
                except: status = ''
                if status == '': status = 'Ended'
                status = client.replaceHTMLCodes(status)
                status = status.encode('utf-8')

                if status == 'Ended': pass
                elif premiered == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))): raise Exception()

                title = client.parseDOM(item, 'EpisodeName')[0]
                if title == '': title = '0'
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                season = client.parseDOM(item, 'SeasonNumber')[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                episode = client.parseDOM(item, 'EpisodeNumber')[0]
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                episode = episode.encode('utf-8')

                tvshowtitle = i['tvshowtitle']
                imdb, tvdb = i['imdb'], i['tvdb']

                year = i['year']
                try: year = year.encode('utf-8')
                except: pass

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

                try: fanart = client.parseDOM(item2, 'fanart')[0]
                except: fanart = ''
                if not fanart == '': fanart = self.tvdb_image + fanart
                else: fanart = '0'
                fanart = client.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try: thumb = client.parseDOM(item, 'filename')[0]
                except: thumb = ''
                if not thumb == '': thumb = self.tvdb_image + thumb
                else: thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not poster == '0': pass
                elif not fanart == '0': poster = fanart
                elif not banner == '0': poster = banner

                if not banner == '0': pass
                elif not fanart == '0': banner = fanart
                elif not poster == '0': banner = poster

                if not thumb == '0': pass
                elif not fanart == '0': thumb = fanart.replace(self.tvdb_image, self.tvdb_poster)
                elif not poster == '0': thumb = poster

                try: studio = client.parseDOM(item2, 'Network')[0]
                except: studio = ''
                if studio == '': studio = '0'
                studio = client.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                try: genre = client.parseDOM(item2, 'Genre')[0]
                except: genre = ''
                genre = [x for x in genre.split('|') if not x == '']
                genre = ' / '.join(genre)
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = client.parseDOM(item2, 'Runtime')[0]
                except: duration = ''
                if duration == '': duration = '0'
                duration = client.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = client.parseDOM(item, 'Rating')[0]
                except: rating = ''
                if rating == '': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = client.parseDOM(item2, 'RatingCount')[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = client.parseDOM(item2, 'ContentRating')[0]
                except: mpaa = ''
                if mpaa == '': mpaa = '0'
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

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

                try: cast = client.parseDOM(item2, 'Actors')[0]
                except: cast = ''
                cast = [x for x in cast.split('|') if not x == '']
                try: cast = [(x.encode('utf-8'), '') for x in cast]
                except: cast = []

                try: plot = client.parseDOM(item, 'Overview')[0]
                except: plot = ''
                if plot == '':
                    try: plot = client.parseDOM(item2, 'Overview')[0]
                    except: plot = ''
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb, 'snum': i['snum'], 'enum': i['enum'], 'action': 'episodes'})
            except:
                pass


        items = items[:100]

        threads = []
        for i in items: threads.append(workers.Thread(items_list, i))
        [i.start() for i in threads]
        [i.join() for i in threads]


        try: self.list = sorted(self.list, key=lambda k: k['premiered'], reverse=True)
        except: pass

        return self.list


    def trakt_user_list(self, url, user):
        try:
            result = trakt.getTrakt(url)
            items = json.loads(result)
        except:
            pass

        for item in items:
            try:
                try: name = item['list']['name']
                except: name = item['name']
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                try: url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except: url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['name'].lower()))
        return self.list


    def episodeDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try: isOld = False ; control.item().getArt('type')
        except: isOld = True

        isEstuary = True if 'estuary' in control.skin else False

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getTVShowIndicators(refresh=True)

        try: multi = [i['tvshowtitle'] for i in items]
        except: multi = []
        multi = len([x for y,x in enumerate(multi) if x not in multi[:y]])
        multi = True if multi > 1 else False

        try: sysaction = items[0]['action']
        except: sysaction = ''

        isFolder = False if not sysaction == 'episodes' else True

        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        tvshowBrowserMenu = control.lang(32071).encode('utf-8')


        for i in items:
            try:
                if not 'label' in i: i['label'] = i['title']

                if i['label'] == '0':
                    label = '%sx%02d . %s %s' % (i['season'], int(i['episode']), 'Episode', i['episode'])
                else:
                    label = '%sx%02d . %s' % (i['season'], int(i['episode']), i['label'])
                if multi == True:
                    label = '%s - %s' % (i['tvshowtitle'], label)

                imdb, tvdb, year, season, episode = i['imdb'], i['tvdb'], i['year'], i['season'], i['episode']

                systitle = urllib.quote_plus(i['title'])
                systvshowtitle = urllib.quote_plus(i['tvshowtitle'])
                syspremiered = urllib.quote_plus(i['premiered'])


                poster, banner, fanart, thumb = i['poster'], i['banner'], i['fanart'], i['thumb']
                if banner == '0' and not fanart == '0': banner = fanart
                elif banner == '0' and not poster == '0': banner = poster
                if thumb == '0' and not fanart == '0': thumb = fanart
                elif thumb == '0' and not poster == '0': thumb = poster
                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if thumb == '0': thumb = addonFanart


                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'mediatype': 'episode'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, systvshowtitle)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                try: meta.update({'title': i['label']})
                except: pass
                if isEstuary == True:
                    try: del meta['cast']
                    except: pass

                sysmeta = urllib.quote_plus(json.dumps(meta))


                url = '%s?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, tvdb, season, episode, systvshowtitle, syspremiered, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                path = '%s?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s' % (sysaddon, systitle, year, imdb, tvdb, season, episode, systvshowtitle, syspremiered)

                if isFolder == True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s' % (sysaddon, systvshowtitle, year, imdb, tvdb, season, episode)


                cm = []

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                if multi == True:
                    cm.append((tvshowBrowserMenu, 'Container.Update(%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s,return)' % (sysaddon, systvshowtitle, year, imdb, tvdb)))

                try:
                    overlay = int(playcount.getEpisodeOverlay(indicators, imdb, tvdb, season, episode))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=6)' % (sysaddon, imdb, tvdb, season, episode)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=7)' % (sysaddon, imdb, tvdb, season, episode)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, systvshowtitle, tvdb)))

                if isFolder == False:
                    cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))


                item = control.item(label=label)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = meta)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except:
                pass


        control.content(syshandle, 'episodes')
        #control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)
        views.setView('episodes', {'skin.confluence': 504})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        #control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)


