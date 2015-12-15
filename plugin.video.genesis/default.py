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


import urlparse,sys
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))


try:
    action = params['action']
except:
    action = None
try:
    name = params['name']
except:
    name = None
try:
    title = params['title']
except:
    title = None
try:
    year = params['year']
except:
    year = None
try:
    imdb = params['imdb']
except:
    imdb = None
try:
    tvdb = params['tvdb']
except:
    tvdb = None
try:
    season = params['season']
except:
    season = None
try:
    episode = params['episode']
except:
    episode = None
try:
    show = params['show']
except:
    show = None
try:
    show_alt = params['show_alt']
except:
    show_alt = None
try:
    date = params['date']
except:
    date = None
try:
    genre = params['genre']
except:
    genre = None
try:
    url = params['url']
except:
    url = None
try:
    image = params['image']
except:
    image = None
try:
    meta = params['meta']
except:
    meta = None
try:
    query = params['query']
except:
    query = None
try:
    source = params['source']
except:
    source = None
try:
    content = params['content']
except:
    content = None
try:
    provider = params['provider']
except:
    provider = None




if action == None:
    from modules.indexers import genesis
    genesis.navigator().root()

elif action == 'root_movies':
    from modules.indexers import genesis
    genesis.navigator().movies()

elif action == 'root_shows':
    from modules.indexers import genesis
    genesis.navigator().tvshows()

elif action == 'root_genesis':
    from modules.indexers import genesis
    genesis.navigator().genesis()

elif action == 'root_calendar':
    from modules.indexers import genesis
    genesis.navigator().calendar()

elif action == 'root_tools':
    from modules.indexers import genesis
    genesis.navigator().tools()

elif action == 'root_library':
    from modules.indexers import genesis
    genesis.navigator().library()

elif action == 'root_search':
    from modules.indexers import genesis
    genesis.navigator().search()

elif action == 'clearCache':
    from modules.libraries import cache
    cache.clear()

elif action == 'refresh':
    from modules.libraries import control
    control.refresh()

elif action == 'queueItem':
    from modules.libraries import control
    control.queueItem()

elif action == 'openPlaylist':
    from modules.libraries import control
    control.openPlaylist()

elif action == 'openSettings':
    from modules.libraries import control
    control.openSettings()

elif action == 'generalSettings':
    from modules.libraries import control
    control.openSettings(c=0, f=0)

elif action == 'playbackSettings':
    from modules.libraries import control
    control.openSettings(c=1, f=0)

elif action == 'movieSettings':
    from modules.libraries import control
    control.openSettings(c=2, f=0)

elif action == 'tvSettings':
    from modules.libraries import control
    control.openSettings(c=3, f=0)

elif action == 'hdhostSettings':
    from modules.libraries import control
    control.openSettings(c=4, f=0)

elif action == 'sdhostSettings':
    from modules.libraries import control
    control.openSettings(c=5, f=0)

elif action == 'accountSettings':
    from modules.libraries import control
    control.openSettings(c=6, f=1)

elif action == 'librarySettings':
    from modules.libraries import control
    control.openSettings(c=7, f=0)

elif action == 'downloadSettings':
    from modules.libraries import control
    control.openSettings(c=8, f=0)

elif action == 'subtitleSettings':
    from modules.libraries import control
    control.openSettings(c=9, f=0)

elif action == 'addView':
    from modules.libraries import views
    views.addView(content)

elif action == 'downloader':
    from modules.libraries import downloader
    downloader.downloader()

elif action == 'addDownload':
    from modules.libraries import downloader
    downloader.addDownload(name,url,image,provider)

elif action == 'removeDownload':
    from modules.libraries import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from modules.libraries import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from modules.libraries import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from modules.libraries import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from modules.libraries import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from modules.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'clearSources':
    from modules.sources import sources
    sources().clearSources()

elif action == 'play':
    from modules.sources import sources
    sources().play(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url)

elif action == 'addPlayableItem':
    from modules.sources import sources
    sources().addPlayableItem(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, meta)

elif action == 'playItem':
    from modules.sources import sources
    sources().playItem(content, name, imdb, tvdb, url, source, provider)




elif action == 'favourite_movie_add':
    from modules.v4 import contextMenu
    contextMenu().favourite_add('Movie', imdb, name, year, image, refresh=True)

elif action == 'favourite_movie_from_search':
    from modules.v4 import contextMenu
    contextMenu().favourite_add('Movie', imdb, name, year, image)

elif action == 'favourite_tv_add':
    from modules.v4 import contextMenu
    contextMenu().favourite_add('TV Show', imdb, name, year, image, refresh=True)

elif action == 'favourite_tv_from_search':
    from modules.v4 import contextMenu
    contextMenu().favourite_add('TV Show', imdb, name, year, image)

elif action == 'favourite_delete':
    from modules.v4 import contextMenu
    contextMenu().favourite_delete(imdb)

elif action == 'trakt_manager':
    from modules.v4 import contextMenu
    contextMenu().trakt_manager('movie', name, imdb)

elif action == 'trakt_tv_manager':
    from modules.v4 import contextMenu
    contextMenu().trakt_manager('show', name, tvdb)

elif action == 'watched_movies':
    from modules.v4 import contextMenu
    contextMenu().playcount_movies(title, year, imdb, 7)

elif action == 'unwatched_movies':
    from modules.v4 import contextMenu
    contextMenu().playcount_movies(title, year, imdb, 6)

elif action == 'watched_episodes':
    from modules.v4 import contextMenu
    contextMenu().playcount_episodes(imdb, tvdb, season, episode, 7)

elif action == 'unwatched_episodes':
    from modules.v4 import contextMenu
    contextMenu().playcount_episodes(imdb, tvdb, season, episode, 6)

elif action == 'watched_shows':
    from modules.v4 import contextMenu
    contextMenu().playcount_shows(name, year, imdb, tvdb, '', 7)

elif action == 'unwatched_shows':
    from modules.v4 import contextMenu
    contextMenu().playcount_shows(name, year, imdb, tvdb, '', 6)

elif action == 'watched_seasons':
    from modules.v4 import contextMenu
    contextMenu().playcount_shows(name, year, imdb, tvdb, season, 7)

elif action == 'unwatched_seasons':
    from modules.v4 import contextMenu
    contextMenu().playcount_shows(name, year, imdb, tvdb, season, 6)

elif action == 'library_movie_add':
    from modules.v4 import contextMenu
    contextMenu().library_movie_add(name, title, year, imdb, url)

elif action == 'library_movie_list':
    from modules.v4 import contextMenu
    contextMenu().library_movie_list(url)

elif action == 'library_tv_add':
    from modules.v4 import contextMenu
    contextMenu().library_tv_add(name, year, imdb, tvdb)

elif action == 'library_tv_list':
    from modules.v4 import contextMenu
    contextMenu().library_tv_list(url)

elif action == 'library_update_tool':
    from modules.v4 import contextMenu
    contextMenu().library_update_tool()

elif action == 'library_update':
    from modules.v4 import contextMenu
    contextMenu().library_update('true')

elif action == 'library_trakt_collection':
    from modules.v4 import contextMenu
    contextMenu().library_movie_tool('trakt_collection')

elif action == 'library_trakt_watchlist':
    from modules.v4 import contextMenu
    contextMenu().library_movie_tool('trakt_watchlist')

elif action == 'library_imdb_watchlist':
    from modules.v4 import contextMenu
    contextMenu().library_movie_tool('imdb_watchlist')

elif action == 'library_tv_trakt_collection':
    from modules.v4 import contextMenu
    contextMenu().library_tv_tool('trakt_tv_collection')

elif action == 'library_tv_trakt_watchlist':
    from modules.v4 import contextMenu
    contextMenu().library_tv_tool('trakt_tv_watchlist')

elif action == 'library_tv_imdb_watchlist':
    from modules.v4 import contextMenu
    contextMenu().library_tv_tool('imdb_tv_watchlist')

elif action == 'toggle_movie_playback':
    from modules.v4 import contextMenu
    contextMenu().toggle_playback('movie', name, title, year, imdb, '', '', '', '', '', '', '')

elif action == 'toggle_episode_playback':
    from modules.v4 import contextMenu
    contextMenu().toggle_playback('episode', name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)

elif action == 'service':
    from modules.v4 import contextMenu
    contextMenu().service()

elif action == 'movies':
    from modules.v4 import movies
    movies().get(url)

elif action == 'movies_userlist':
    from modules.v4 import movies
    movies().get(url)

elif action == 'movies_popular':
    from modules.v4 import movies
    movies().popular()

elif action == 'movies_boxoffice':
    from modules.v4 import movies
    movies().boxoffice()

elif action == 'movies_views':
    from modules.v4 import movies
    movies().views()

elif action == 'movies_oscars':
    from modules.v4 import movies
    movies().oscars()

elif action == 'movies_added_hd':
    from modules.v4 import movies
    movies().added_hd()

elif action == 'movies_added':
    from modules.v4 import movies
    movies().added()

elif action == 'movies_theaters':
    from modules.v4 import movies
    movies().theaters()

elif action == 'movies_trending':
    from modules.v4 import movies
    movies().trending()

elif action == 'movies_featured':
    from modules.v4 import movies
    movies().featured()

elif action == 'movies_trakt_collection':
    from modules.v4 import movies
    movies().trakt_collection()

elif action == 'movies_trakt_watchlist':
    from modules.v4 import movies
    movies().trakt_watchlist()

elif action == 'movies_imdb_watchlist':
    from modules.v4 import movies
    movies().imdb_watchlist()

elif action == 'movies_search':
    from modules.v4 import movies
    movies().search(query)

elif action == 'movies_favourites':
    from modules.v4 import movies
    movies().favourites()

elif action == 'shows':
    from modules.v4 import shows
    shows().get(url)

elif action == 'shows_userlist':
    from modules.v4 import shows
    shows().get(url)

elif action == 'shows_popular':
    from modules.v4 import shows
    shows().popular()

elif action == 'shows_rating':
    from modules.v4 import shows
    shows().rating()

elif action == 'shows_views':
    from modules.v4 import shows
    shows().views()

elif action == 'shows_active':
    from modules.v4 import shows
    shows().active()

elif action == 'shows_trending':
    from modules.v4 import shows
    shows().trending()

elif action == 'shows_season_premieres':
    from modules.v4 import shows
    shows().season_premieres()

elif action == 'shows_premieres':
    from modules.v4 import shows
    shows().premieres()

elif action == 'shows_trakt_collection':
    from modules.v4 import shows
    shows().trakt_collection()

elif action == 'shows_trakt_watchlist':
    from modules.v4 import shows
    shows().trakt_watchlist()

elif action == 'shows_imdb_watchlist':
    from modules.v4 import shows
    shows().imdb_watchlist()

elif action == 'shows_search':
    from modules.v4 import shows
    shows().search(query)

elif action == 'shows_favourites':
    from modules.v4 import shows
    shows().favourites()

elif action == 'seasons':
    from modules.v4 import seasons
    seasons().get(show, year, imdb, tvdb)

elif action == 'episodes':
    from modules.v4 import episodes
    episodes().get(show, year, imdb, tvdb, season)

elif action == 'episodes2':
    from modules.v4 import episodes
    episodes().get2(show, year, imdb, tvdb, season, episode)

elif action == 'episodes_calendar_1':
    from modules.v4 import episodes
    episodes().calendar(1)

elif action == 'episodes_calendar_2':
    from modules.v4 import episodes
    episodes().calendar(2)

elif action == 'episodes_calendar_3':
    from modules.v4 import episodes
    episodes().calendar(3)

elif action == 'episodes_calendar_4':
    from modules.v4 import episodes
    episodes().calendar(4)

elif action == 'episodes_trakt_progress':
    from modules.v4 import episodes
    episodes().trakt_progress()

elif action == 'episodes_trakt':
    from modules.v4 import episodes
    episodes().trakt_added()

elif action == 'episodes_added':
    from modules.v4 import episodes
    episodes().added()

elif action == 'people_movies':
    from modules.v4 import people
    people().movies(query)

elif action == 'people_shows':
    from modules.v4 import people
    people().shows(query)

elif action == 'genres_movies':
    from modules.v4 import genres
    genres().movies()

elif action == 'genres_shows':
    from modules.v4 import genres
    genres().shows()

elif action == 'certificates_movies':
    from modules.v4 import certificates
    certificates().movies()

elif action == 'certificates_shows':
    from modules.v4 import certificates
    certificates().shows()

elif action == 'languages_movies':
    from modules.v4 import languages
    languages().movies()

elif action == 'years_movies':
    from modules.v4 import years
    years().movies()

elif action == 'channels_movies':
    from modules.v4 import channels
    channels().movies()

elif action == 'userlists_movies':
    from modules.v4 import userlists
    userlists().movies()

elif action == 'userlists_shows':
    from modules.v4 import userlists
    userlists().shows()

