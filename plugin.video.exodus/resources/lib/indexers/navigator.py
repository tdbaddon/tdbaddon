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


import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt


artPath = control.artPath()

addonFanart = control.addonFanart()

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

isPlayable = False if control.setting('autoplay') == 'false' and control.setting('hosts.mode') == '1' else True

classicMenu = True if control.setting('menu.classic') == 'true' else False

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

sysaddon = sys.argv[0]


class navigator:
    def root(self):
        self.addDirectoryItem(30001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(30002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30003, 'channels', 'channels.png', 'DefaultMovies.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(30004, 'myNavigator', 'userlists.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(30005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png', queue=True)

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(30006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        if not control.setting('calendar.widget') == '0':
            self.addDirectoryItem(30007, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem(30008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(30010, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(30009, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        self.endDirectory()

        from resources.lib.modules import cache
        from resources.lib.modules import changelog
        cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')


    def movies(self):
        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30036, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30037, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True)

        if classicMenu == False and imdbCredentials == True:
            self.addDirectoryItem(30037, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(30021, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(30022, 'movieYears', 'years.png', 'DefaultMovies.png')
        self.addDirectoryItem(30023, 'moviePersons', 'people.png', 'DefaultMovies.png')
        self.addDirectoryItem(30024, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')

        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30025, 'movies&url=traktfeatured', 'featured.png', 'DefaultRecentlyAddedMovies.png')
        else:
            self.addDirectoryItem(30025, 'movies&url=featured', 'featured.png', 'DefaultRecentlyAddedMovies.png')

        self.addDirectoryItem(30026, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30027, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem(30028, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(30029, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem(30030, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.addDirectoryItem(30031, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30032, 'movies&url=featured', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if classicMenu == False and (traktCredentials == True or imdbCredentials == True):
            self.addDirectoryItem(30038, 'movieUserlists', 'userlists.png', 'DefaultVideoPlaylists.png')
        elif not control.setting('lists.widget') == '0':
            self.addDirectoryItem(30033, 'myNavigator', 'userlists.png', 'DefaultVideoPlaylists.png')

        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30039, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(30034, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(30035, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self):
        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30067, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(30068, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        if classicMenu == False and traktIndicators == True:
            self.addDirectoryItem(30069, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        if classicMenu == False and imdbCredentials == True:
            self.addDirectoryItem(30068, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        self.addDirectoryItem(30051, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30024, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30053, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')

        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30070, 'tvshows&url=traktfeatured', 'featured.png', 'DefaultTVShows.png')

        self.addDirectoryItem(30054, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30055, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30056, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30057, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30058, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30059, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30060, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30061, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if classicMenu == False and traktIndicators == True:
            self.addDirectoryItem(30062, 'calendar&url=mycalendar', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        else:
            self.addDirectoryItem(30062, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        if classicMenu == False and (traktCredentials == True or imdbCredentials == True):
            self.addDirectoryItem(30071, 'tvUserlists', 'userlists.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(30072, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')
        elif not control.setting('lists.widget') == '0':
            self.addDirectoryItem(30063, 'myNavigator', 'userlists.png', 'DefaultVideoPlaylists.png')

        if classicMenu == False and traktCredentials == True:
            self.addDirectoryItem(30073, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)

        self.addDirectoryItem(30065, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30066, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def lists(self):
        if traktCredentials == False and imdbCredentials == False:
            return control.dialog.ok('Exodus', control.lang(30081).encode('utf-8'), control.lang(30082).encode('utf-8'), control.lang(30083).encode('utf-8'))

        if traktCredentials == True:
            self.addDirectoryItem(30084, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30085, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(30086, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30087, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        if imdbCredentials == True:
            self.addDirectoryItem(30088, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30089, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(30090, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30091, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        if traktIndicators == True:
            self.addDirectoryItem(30092, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(30093, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(30094, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(30095, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        if traktCredentials == True or imdbCredentials == True:
            self.addDirectoryItem(30096, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')
            self.addDirectoryItem(30097, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')
            self.addDirectoryItem(30098, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(30111, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30112, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30113, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30114, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30115, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30122, 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30119, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30120, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(30141, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(30142, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(30151, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(30152, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(30153, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(30154, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def addDirectoryItem(self, name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True and isPlayable == True: cm.append((control.lang(30155).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))
        item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems(cm, replaceItems=False)
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self, cacheToDisc=True):
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)


