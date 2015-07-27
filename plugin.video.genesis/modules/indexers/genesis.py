# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import os
import sys
import urlparse
from modules.libraries import control


sysAddon = sys.argv[0]

artPath = control.artPath()

addonFanart = control.addonFanart()

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

if (control.setting('trakt_user') == '' or control.setting('trakt_password') == ''): traktMode = False
else: traktMode = True

if control.setting('imdb_user') == '': imdbMode = False
else: imdbMode = True


class navigator:

    def root(self):
        self.addDirectoryItem(30501, 'root_movies', 'root_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30502, 'root_shows', 'root_shows.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30503, 'channels_movies', 'channels_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30504, 'root_genesis', 'root_genesis.jpg', 'DefaultVideoPlaylists.png')

        root_movies = control.setting('root_movies')
        if root_movies == '1':
            self.addDirectoryItem(30505, 'movies_featured', 'movies_added.jpg', 'DefaultRecentlyAddedMovies.png')
        elif root_movies == '2':
            self.addDirectoryItem(30505, 'movies_added_hd', 'movies_added.jpg', 'DefaultRecentlyAddedMovies.png')
        elif root_movies == '3':
            self.addDirectoryItem(30505, 'movies_added', 'movies_added.jpg', 'DefaultRecentlyAddedMovies.png')

        if traktMode == True:
            root_episodes = control.setting('root_episodes_trakt')
        else:
            root_episodes = control.setting('root_episodes')

        if root_episodes == '1':
            self.addDirectoryItem(30506, 'episodes_added', 'episodes_added.jpg', 'DefaultRecentlyAddedEpisodes.png')
        elif root_episodes == '2':
            self.addDirectoryItem(30506, 'episodes_trakt_progress', 'episodes_added.jpg', 'DefaultRecentlyAddedEpisodes.png')
        elif root_episodes == '3':
            self.addDirectoryItem(30506, 'episodes_trakt', 'episodes_added.jpg', 'DefaultRecentlyAddedEpisodes.png')

        '''
        if not control.setting('root_movies') == '0':
            self.addDirectoryItem(30505, 'root_movies_added', 'movies_added.jpg', 'DefaultRecentlyAddedMovies.png')

        if (traktMode == True and not control.setting('root_episodes_trakt') == '0') or (traktMode == False and not control.setting('root_episodes') == '0'):
            self.addDirectoryItem(30506, 'root_episodes_added', 'episodes_added.jpg', 'DefaultRecentlyAddedEpisodes.png')

        if not control.setting('root_calendar') == '0':
            self.addDirectoryItem(30507, 'root_calendar', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        '''

        self.addDirectoryItem(30508, 'root_tools', 'root_tools.jpg', 'DefaultAddonProgram.png')

        if not control.setting('downloadPath') == '':
            self.addDirectoryItem(30140, 'downloader', 'downloader.jpg', 'DefaultFolder.png')

        self.addDirectoryItem(30509, 'root_search', 'root_search.jpg', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self):
        self.addDirectoryItem(30521, 'genres_movies', 'genres_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30522, 'languages_movies', 'languages_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30523, 'certificates_movies', 'certificates_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30524, 'movies_boxoffice', 'movies_boxoffice.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30525, 'years_movies', 'years_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30526, 'movies_trending', 'movies_trending.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30527, 'movies_popular', 'movies_popular.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30528, 'movies_views', 'movies_views.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30529, 'movies_oscars', 'movies_oscars.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30530, 'movies_theaters', 'movies_theaters.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30531, 'movies_added_hd', 'movies_added_hd.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30532, 'movies_added', 'movies_added.jpg', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(30533, 'movies_favourites', 'movies_favourites.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30534, 'people_movies', 'people_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30535, 'movies_search', 'movies_search.jpg', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self):
        self.addDirectoryItem(30541, 'genres_shows', 'genres_shows.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30542, 'certificates_shows', 'certificates_shows.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30543, 'shows_popular', 'shows_popular.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30544, 'shows_active', 'shows_active.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30545, 'shows_trending', 'shows_trending.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30546, 'shows_rating', 'shows_rating.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30547, 'shows_views', 'shows_views.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30548, 'episodes_added', 'episodes_added.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30549, 'root_calendar', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30550, 'shows_favourites', 'shows_favourites.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30551, 'people_shows', 'people_shows.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30552, 'shows_search', 'shows_search.jpg', 'DefaultTVShows.png')

        self.endDirectory()


    def genesis(self):
        if traktMode == True:
            self.addDirectoryItem(30581, 'movies_trakt_collection', 'movies_trakt_collection.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30582, 'shows_trakt_collection', 'shows_trakt_collection.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30583, 'movies_trakt_watchlist', 'movies_trakt_watchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30584, 'shows_trakt_watchlist', 'shows_trakt_watchlist.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30585, 'episodes_trakt_progress', 'episodes_trakt_progress.jpg', 'DefaultRecentlyAddedEpisodes.png')
            self.addDirectoryItem(30586, 'episodes_trakt', 'episodes_trakt.jpg', 'DefaultRecentlyAddedEpisodes.png')

        if imdbMode == True:
            self.addDirectoryItem(30587, 'movies_imdb_watchlist', 'movies_imdb_watchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30588, 'shows_imdb_watchlist', 'shows_imdb_watchlist.jpg', 'DefaultTVShows.png')

        if traktMode == True or imdbMode == True:
            self.addDirectoryItem(30589, 'userlists_movies', 'userlists_movies.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30590, 'userlists_shows', 'userlists_shows.jpg', 'DefaultTVShows.png')

        self.addDirectoryItem(30591, 'movies_favourites', 'movies_favourites.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30592, 'shows_favourites', 'shows_favourites.jpg', 'DefaultTVShows.png')

        self.endDirectory()


    def calendar(self):
        self.addDirectoryItem(30561, 'episodes_calendar_1', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30562, 'episodes_calendar_2', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30563, 'episodes_calendar_3', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30564, 'episodes_calendar_4', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30565, 'shows_season_premieres', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(30566, 'shows_premieres', 'root_calendar.jpg', 'DefaultRecentlyAddedEpisodes.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(30621, 'generalSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30622, 'accountSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30623, 'playbackSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30624, 'subtitleSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30625, 'movieSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30626, 'tvSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30627, 'hdhostSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30628, 'sdhostSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30629, 'clearSources', 'cache_clear.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30630, 'clearCache', 'cache_clear.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30631, 'downloadSettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30632, 'root_library', 'root_library.jpg', 'DefaultAddonProgram.png')

        self.endDirectory()


    def library(self):
        self.addDirectoryItem(30640, 'librarySettings', 'settings.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30641, 'library_update_tool', 'library_update.jpg', 'DefaultAddonProgram.png')
        self.addDirectoryItem(30642, control.setting('movie_library'), 'library_movies.jpg', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(30643, control.setting('tv_library'), 'library_shows.jpg', 'DefaultTVShows.png', isAction=False)

        if traktMode == True:
            self.addDirectoryItem(30644, 'library_trakt_collection', 'movies_trakt_collection.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30645, 'library_tv_trakt_collection', 'shows_trakt_collection.jpg', 'DefaultTVShows.png')
            self.addDirectoryItem(30646, 'library_trakt_watchlist', 'movies_trakt_watchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30647, 'library_tv_trakt_watchlist', 'shows_trakt_watchlist.jpg', 'DefaultTVShows.png')

        if imdbMode == True:
            self.addDirectoryItem(30648, 'library_imdb_watchlist', 'movies_imdb_watchlist.jpg', 'DefaultMovies.png')
            self.addDirectoryItem(30649, 'library_tv_imdb_watchlist', 'shows_imdb_watchlist.jpg', 'DefaultTVShows.png')

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(30601, 'movies_search', 'movies_search.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30602, 'shows_search', 'shows_search.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30603, 'people_movies', 'people_movies.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30604, 'people_shows', 'people_shows.jpg', 'DefaultTVShows.png')

        self.endDirectory()


    def addDirectoryItem(self, name, query, thumb, icon, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysAddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        item = control.item(name, iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems([], replaceItems=False)
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=int(sys.argv[1]),url=url,listitem=item,isFolder=isFolder)


    def endDirectory(self, cacheToDisc=True):
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)

