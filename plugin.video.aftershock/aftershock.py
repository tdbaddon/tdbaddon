# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import sys
import urlparse

import xbmc
from ashock.modules import analytics
from ashock.modules import logger

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

logger.debug(params, __name__)

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
    imdb = '0'
try:
    tvdb = params['tvdb']
except:
    tvdb = '0'
try:
    season = params['season']
except:
    season = None
try:
    episode = params['episode']
except:
    episode = None
try:
    tvshowtitle = params['tvshowtitle']
except:
    tvshowtitle = None
try:
    tvshowtitle = params['show']
except:
    pass
try:
    date = params['date']
except:
    date = None
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
try:
    genre = params['genre']
except:
    genre = None
try:
    lang = params['lang']
except:
    lang = None
try:
    select = params.get('select')
except:
    select=1

if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'movieLangNavigator':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieLangHome':
    from resources.lib.indexers import movies
    movies.movies().home(lang=lang)

elif action == 'movieLangGenre':
    from resources.lib.indexers import movies
    movies.movies().genres(lang=lang)

elif action == 'movieLangYears':
    from resources.lib.indexers import movies
    movies.movies().years(lang=lang)

elif action == 'movies':
    from resources.lib.indexers import movies
    analytics.sendAnalytics('%s-%s' % (action, lang))
    movies.movies().get(url, lang=lang)

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search(query, lang)

elif action == 'desiTVNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().desiTV()

elif action == 'desiLiveNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().desiLiveTV(url)
    analytics.sendAnalytics('%s-LIVE' % action)

elif action == 'artwork':
    from ashock.modules import control
    control.artwork()

elif action == 'liveEPGNavigator':
    from ashock.modules import control
    analytics.sendAnalytics('%s-EPG' % action)
    xbmc.executebuiltin("RunAddon(script.aftershocknow.guide)")

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    analytics.sendAnalytics('%s-%s' % (action, name))
    tvshows.tvshows().get(url, provider=provider, network=name)

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    analytics.sendAnalytics('%s-%s' % (action, tvshowtitle))
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode, provider=provider, url=url)

elif action == 'addItem':
    from resources.lib.sources import sources
    sources().addItem(title, content)

elif action == 'download':
    import json
    from resources.lib.sources import sources
    from ashock.modules import downloader
    try: downloader.download(name, image, sources().sourcesResolve(json.loads(source)[0]))
    except: pass

elif action == 'play':
    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tvdb, season, episode, tvshowtitle, date, meta, url, select)

elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(content, title, source)

elif action == 'trailer':
    from ashock.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'addView':
    from ashock.modules import views
    views.addView(content)

elif action == 'refresh':
    from ashock.modules import control
    control.refresh()

elif action == 'queueItem':
    from ashock.modules import control
    control.queueItem()

elif action == 'moviePlaycount':
    from ashock.modules import playcount
    playcount.movies(title, year, imdb, query)

elif action == 'episodePlaycount':
    from ashock.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from ashock.modules import playcount
    playcount.tvshows(name, year, imdb, tvdb, season, query)

elif action == 'rdAuthorize':
    from ashock.modules import debrid
    debrid.rdAuthorize()

elif action == 'alterSources':
    from resources.lib.sources import sources
    sources().alterSources(url, meta)

elif action == 'trailer':
    from ashock.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'openSettings':
    from ashock.modules import control
    control.openSettings(query)

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache(url)

elif action == 'changelog':
    from ashock.modules import changelog
    changelog.get('1')

elif action == 'startLiveProxy':
    try :
        import os
        from ashock.modules import control

        libPath = os.path.join(control.addonInfo('path'), 'resources', 'lib', 'modules')
        serverPath = os.path.join(libPath, 'localproxy.py')
        try:
            import requests
            requests.get('http://127.0.0.1:29000/version')
            proxyIsRunning = True
        except:
            proxyIsRunning = False
        if not proxyIsRunning:
            xbmc.executebuiltin('RunScript(' + serverPath + ')')
    except:
        import traceback
        traceback.print_exc()