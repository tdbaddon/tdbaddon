# -*- coding: utf-8 -*-

'''
    zen Add-on
    Copyright (C) 2016 zen

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
import xbmc,os,zipfile,ntpath,xbmcgui
dialog = xbmcgui.Dialog()
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')


if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'ShowChangelog':
    from resources.lib.modules import changelog
    changelog.get()
	
elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)
	
elif action == 'similar_movies':
    from resources.lib.indexers import movies
    movies.movies().similar_movies(imdb)
	
elif action == 'get_similar_movies':
    from resources.lib.indexers import movies
    movies.movies().get_similar_movies(imdb)	
	



elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search(query)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person(query)

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons()

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)
	
elif action == 'similar_shows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().similar_shows(imdb)
	
elif action == 'get_similar_shows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get_similar_shows(imdb)	

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'rdAuthorize':
    from resources.lib.modules import debrid
    debrid.rdAuthorize()

elif action == 'download':
    import json
    from resources.lib.sources import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play':
    from resources.lib.modules import control
    select = control.setting('hosts.mode')
    if select == '3' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.sources import sources
		sources().play_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    elif select == '4' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.sources import sources
		sources().play_dialog_list(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    else:
		from resources.lib.sources import sources
		sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
		
elif action == 'play_alter':
		from resources.lib.sources import sources
		sources().play_alter(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta)

elif action == 'play_library':
    from resources.lib.sources import sources
    sources().play_library(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.sources import sources
    sources().addItem(title)
	
elif action == 'movieFavourites':
    from resources.lib.indexers import movies
    movies.movies().favourites()
	
elif action == 'movieProgress':
    from resources.lib.indexers import movies
    movies.movies().in_progress()
	
elif action == 'showsProgress':
    from resources.lib.indexers import episodes
    episodes.episodes().in_progress()
	
elif action == 'deleteProgress':
    from resources.lib.modules import favourites
    favourites.deleteProgress(meta, content)
	
elif action == 'tvFavourites':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().favourites()
	
elif action == 'addFavourite':
    from resources.lib.modules import favourites
    favourites.addFavourite(meta, content)

elif action == 'deleteFavourite':
    from resources.lib.modules import favourites
    favourites.deleteFavourite(meta, content)
elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.sources import sources
    sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.sources import sources
    sources().clearSources()
	
elif action == 'clearProgress':
    from resources.lib.modules import control
    import os,xbmc,xbmcaddon,xbmcgui
    dialog = xbmcgui.Dialog()
    addonInfo = xbmcaddon.Addon().getAddonInfo
    dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
    favouritesFile = os.path.join(dataPath, 'favourites.db')
    progressFile = os.path.join(dataPath, 'progress.db')
    yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
    if yes:
		try: 
			os.remove(progressFile)
			dialog.ok('Clear Progress','Clear Progress Complete','','')
		except:
			dialog.ok('Clear Progress','There was an error Deleting the Database','','')		
		
	
elif action == 'urlresolversettings':
    import urlresolver
    urlresolver.display_settings()	
	
elif action == 'movieToLibrary':
    from resources.lib.sources import sources
    sources().movieToLibrary(title,year,imdb,meta)

elif action == 'backupwatchlist':
    import xbmc,os,zipfile,ntpath,xbmcgui
    from resources.lib.modules import control
    dialog = xbmcgui.Dialog()
    USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.zen',''))
    if os.path.exists(os.path.join(USERDATA,'favourites.db')):
		backupdir = control.setting('remote_path')
		if not backupdir == '':
		   to_backup = xbmc.translatePath(os.path.join('special://','home/userdata/addon_data/'))	
		   rootlen = len(USERDATA)
		   backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'zen_watchlist.zip'))
		   zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
		   fn = os.path.join(USERDATA, 'favourites.db')
		   zipobj.write(fn, fn[rootlen:])
		   dialog.ok('Backup Watchlist','Backup complete','','')
		else:
		   dialog.ok('Backup Watchlist','No backup location found: Please setup your Backup location in the addon settings','','')
		   xbmc.executebuiltin('RunPlugin(%s?action=openSettings&query=5.0)' % sys.argv[0])
       
elif action == 'restorewatchlist':
    import xbmc,os,zipfile,ntpath,xbmcgui
    from resources.lib.modules import control
    dialog = xbmcgui.Dialog()
    USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.zen',''))
    if os.path.exists(USERDATA):
		zipdir=control.setting('remote_restore_path')
		if not zipdir == '':
		   with zipfile.ZipFile(zipdir, "r") as z:
				z.extractall(USERDATA)
				dialog.ok('Restore Watchlist','Restore complete','','')
		else:
				dialog.ok('Restore Watchlist','No item found: Please select your zipfile location in the addon settings','','')
				xbmc.executebuiltin('RunPlugin(%s?action=openSettings&query=5.0)' % sys.argv[0])
				
elif action == 'movielist':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()	

elif action == 'tvlist':
    from resources.lib.indexers import navigator
    navigator.navigator().mytv()		
				
elif action == 'lists_navigator':
    from resources.lib.indexers import navigator
    navigator.navigator().lists_navigator()				
				
				
				