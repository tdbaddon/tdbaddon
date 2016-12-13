# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 Innovate

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


import urlparse,sys, xbmc
from resources.lib.libraries import logger
from resources.lib.libraries import analytics

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
    tmdb = params['tmdb']
except:
    tmdb = '0'
try:
    tvdb = params['tvdb']
except:
    tvdb = '0'
try:
    tvrage = params['tvrage']
except:
    tvrage = '0'
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
    alter = params['alter']
except:
    alter = '0'
try:
    alter = params['genre']
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
    from resources.lib.indexers import livetv
    analytics.sendAnalytics('%s-LIVE' % action)
    livetv.channels().get()

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'liveEPGNavigator':
    from resources.lib.libraries import control
    analytics.sendAnalytics('%s-EPG' % action)
    try :
        tmpAddon = control.addon('script.aftershocknow.guide')
        xbmc.executebuiltin("RunAddon(script.aftershocknow.guide)")
    except:
        import traceback
        traceback.print_exc()
        control.dialog.ok(control.addonInfo('name'), "Please make a $5 donation to aftershockpy@gmail.com via PayPal to get access !!")

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    analytics.sendAnalytics('%s-%s' % (action,name))
    tvshows.tvshows().get(url, provider=provider, network=name)

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    analytics.sendAnalytics('%s-%s' % (action,tvshowtitle))
    episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode, provider=provider, url=url)

elif action == 'addItem':
    from resources.lib.sources import sources
    sources().addItem(title, content)

elif action == 'download':
    import json
    from resources.lib.sources import sources
    from resources.lib.libraries import downloader
    try: downloader.download(name, image, sources().sourcesResolve(json.loads(source)[0]))
    except: pass

elif action == 'play':
    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url, select)

elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(content, title, source)

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'addView':
    from resources.lib.libraries import views
    views.addView(content)

elif action == 'refresh':
    from resources.lib.libraries import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.libraries import control
    control.queueItem()

elif action == 'moviePlaycount':
    from resources.lib.libraries import playcount
    playcount.movies(title, year, imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.libraries import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.libraries import playcount
    playcount.tvshows(name, year, imdb, tvdb, season, query)

elif action == 'rdAuthorize':
    from resources.lib.libraries import debrid
    debrid.rdAuthorize()

elif action == 'alterSources':
    from resources.lib.sources import sources
    sources().alterSources(url, meta)

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'openSettings':
    from resources.lib.libraries import control
    control.openSettings(query)

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache(url)