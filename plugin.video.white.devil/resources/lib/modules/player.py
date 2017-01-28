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


import re,sys,json,time,xbmc

from resources.lib.modules import control
from resources.lib.modules import bookmarks
from resources.lib.modules import playcount
from resources.lib.modules import subtitles


class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)


    def run(self, title, year, season, episode, imdb, tvdb, meta, url):
        try:
            self.loadingTime = time.time()
            self.totalTime = 0 ; self.currentTime = 0

            self.content = 'movie' if season == None or episode == None else 'episode'

            self.title = title ; self.year = year
            self.name = '%s (%s)' % (title, year) if self.content == 'movie' else '%s S%02dE%02d' % (title, int(season), int(episode))
            self.season = '%01d' % int(season) if self.content == 'episode' else None
            self.episode = '%01d' % int(episode) if self.content == 'episode' else None

            self.imdb = imdb if not imdb == None else '0'
            self.tvdb = tvdb if not tvdb == None else '0'
            self.ids = {'imdb': self.imdb, 'tvdb': self.tvdb}
            self.ids = dict((k,v) for k, v in self.ids.iteritems() if not v == '0')

            control.window.setProperty('script.trakt.ids', json.dumps(self.ids))

            self.getBookmark()

            poster, thumb, meta = self.getMeta(meta)
            item = control.item(path=url, iconImage='DefaultVideo.png', thumbnailImage=thumb)
            item.setInfo(type='Video', infoLabels = meta)
            try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
            except: pass
            item.setProperty('Video', 'true')
            item.setProperty('IsPlayable', 'true')
            control.player.play(url, item)
            control.resolve(int(sys.argv[1]), True, item)

            self.keepPlaybackAlive()

            control.window.clearProperty('script.trakt.ids')
        except:
            return


    def getMeta(self, meta):
        try:
            meta = json.loads(meta)

            poster = meta['poster'] if 'poster' in meta else '0'
            thumb = meta['thumb'] if 'thumb' in meta else poster

            if poster == '0': poster = control.addonPoster()

            return (poster, thumb, meta)
        except:
            poster, thumb, meta = '', '', {'title': self.name}
            return (poster, thumb, meta)


    def getBookmark(self):
        try:
            if not control.setting('bookmarks') == 'true': raise Exception()

            self.offset = bookmarks.getBookmark(self.name, self.year)
            if self.offset == '0': raise Exception()

            minutes, seconds = divmod(float(self.offset), 60) ; hours, minutes = divmod(minutes, 60)
            yes = control.yesnoDialog('%s %02d:%02d:%02d' % (control.lang(30461).encode('utf-8'), hours, minutes, seconds), '', '', self.name, control.lang(30463).encode('utf-8'), control.lang(30462).encode('utf-8'))

            if yes: self.offset = '0'
        except:
            pass


    def resetBookmark(self):
        try:
            bookmarks.deleteBookmark(self.name, self.year)
            ok = int(self.currentTime) > 180 and (self.currentTime / self.totalTime) <= .92
            if ok: bookmarks.addBookmark(self.currentTime, self.name, self.year)
        except:
            pass


    def setBookmark(self):
        try:
            if self.offset == '0': raise Exception()
            self.seekTime(float(self.offset))
        except:
            pass


    def keepPlaybackAlive(self):
        pname = '%s.player.overlay' % control.addonInfo('id')
        control.window.clearProperty(pname)


        if self.content == 'movie':
            overlay = playcount.getMovieOverlay(playcount.getMovieIndicators(), self.imdb)

        elif self.content == 'episode':
            overlay = playcount.getEpisodeOverlay(playcount.getTVShowIndicators(), self.imdb, self.tvdb, self.season, self.episode)

        else:
            overlay = '6'


        for i in range(0, 240):
            if self.isPlayingVideo(): break
            xbmc.sleep(1000)


        if overlay == '7':

            while self.isPlayingVideo():
                try:
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()
                except:
                    pass
                xbmc.sleep(2000)


        elif self.content == 'movie':

            while self.isPlayingVideo():
                try:
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()

                    watcher = (self.currentTime / self.totalTime >= .9)
                    property = control.window.getProperty(pname)

                    if watcher == True and not property == '7':
                        control.window.setProperty(pname, '7')
                        playcount.markMovieDuringPlayback(self.imdb, '7')

                    elif watcher == False and not property == '6':
                        control.window.setProperty(pname, '6')
                        playcount.markMovieDuringPlayback(self.imdb, '6')
                except:
                    pass
                xbmc.sleep(2000)


        elif self.content == 'episode':

            while self.isPlayingVideo():
                try:
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()

                    watcher = (self.currentTime / self.totalTime >= .9)
                    property = control.window.getProperty(pname)

                    if watcher == True and not property == '7':
                        control.window.setProperty(pname, '7')
                        playcount.markEpisodeDuringPlayback(self.imdb, self.tvdb, self.season, self.episode, '7')

                    elif watcher == False and not property == '6':
                        control.window.setProperty(pname, '6')
                        playcount.markEpisodeDuringPlayback(self.imdb, self.tvdb, self.season, self.episode, '6')
                except:
                    pass
                xbmc.sleep(2000)


        control.window.clearProperty(pname)


    def idleForPlayback(self):
        for i in range(0, 200):
            if control.condVisibility('Window.IsActive(busydialog)') == 1: control.idle()
            else: break
            control.sleep(100)


    def showPlaybackInfo(self):
        try:
            if not control.setting('player.info') == 'true': raise Exception()
            elapsedTime = '%s %s %s' % (control.lang(30464).encode('utf-8'), int((time.time() - self.loadingTime)), control.lang(30465).encode('utf-8'))
            control.infoDialog(elapsedTime, heading=self.name)
        except:
            pass


    def searchForSubtitles(self):
        try:
            if not control.setting('subtitles') == 'true': raise Exception()
            if self.content == 'episode': subtitles.get(self.name, self.imdb, self.season, self.episode)
            elif self.content == 'movie': subtitles.get(self.name, self.imdb, '', '')
        except:
            pass


    def onPlayBackStarted(self):
        self.idleForPlayback()
        self.showPlaybackInfo()
        self.setBookmark()
        self.searchForSubtitles()


    def onPlayBackStopped(self):
        self.resetBookmark()


    def onPlayBackEnded(self):
        self.onPlayBackStopped()


