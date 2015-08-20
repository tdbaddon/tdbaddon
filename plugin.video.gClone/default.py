# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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
    from modules.v4 import root
    root().get()

elif action == 'root_movies':
    from modules.v4 import root
    root().movies()

elif action == 'root_shows':
    from modules.v4 import root
    root().shows()

elif action == 'root_calendar':
    from modules.v4 import root
    root().calendar()

elif action == 'root_genesis':
    from modules.v4 import root
    root().gClone()

elif action == 'root_tools':
    from modules.v4 import root
    root().tools()

elif action == 'root_search':
    from modules.v4 import root
    root().search()

elif action == 'root_library':
    from modules.v4 import root
    root().library()

elif action == 'cache_clear_list':
    from modules.v4 import index
    index().cache_clear_list()

elif action == 'cache_clear_src':
    from modules.v4 import index
    index().cache_clear_src()

elif action == 'container_refresh':
    from modules.v4 import index
    index().container_refresh()

elif action == 'item_queue':
    from modules.v4 import contextMenu
    contextMenu().item_queue()

elif action == 'view_movies':
    from modules.v4 import contextMenu
    contextMenu().view('movies')

elif action == 'view_tvshows':
    from modules.v4 import contextMenu
    contextMenu().view('tvshows')

elif action == 'view_seasons':
    from modules.v4 import contextMenu
    contextMenu().view('seasons')

elif action == 'view_episodes':
    from modules.v4 import contextMenu
    contextMenu().view('episodes')

elif action == 'playlist_open':
    from modules.v4 import contextMenu
    contextMenu().playlist_open()

elif action == 'settings_open':
    from modules.v4 import contextMenu
    contextMenu().settings_open()

elif action == 'settings_general':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=0.0)

elif action == 'settings_playback':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=1.0)

elif action == 'settings_movies':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=2.0)

elif action == 'settings_tv':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=3.0)

elif action == 'settings_hostshd':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=4.0)

elif action == 'settings_hostssd':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=5.0)

elif action == 'settings_accounts':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=6.1)

elif action == 'settings_library':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=7.0)

elif action == 'settings_downloads':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=8.0)

elif action == 'settings_subtitles':
    from modules.v4 import contextMenu
    contextMenu().settings_open(cat=9.0)

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

elif action == 'download':
    from modules.v4 import contextMenu
    contextMenu().download(name, url, provider)

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

elif action == 'trailer':
    from modules.libraries.trailer import trailer
    trailer().play(name, url)

elif action == 'play':
    from modules.sources import sources
    sources().play(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url)

elif action == 'addPlayableItem':
    from modules.sources import sources
    sources().addPlayableItem(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, meta)

elif action == 'playItem':
    from modules.sources import sources
    sources().playItem(content, name, imdb, tvdb, url, source, provider)

