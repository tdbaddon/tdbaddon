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


import json
import base64
import urlparse
from modules.libraries import cache
from modules.libraries import control
from modules.libraries import client


def getTrakt(url, post=None):
    try:
        trakt_base = 'http://api-v2launch.trakt.tv'
        headers = {'Content-Type': 'application/json', 'trakt-api-key': base64.urlsafe_b64decode('ZWI0MWU5NTI0M2Q4Yzk1MTUyZWQ3MmExZmMwMzk0YzkzY2I3ODVjYjMzYWVkNjA5ZmRkZTFhMDc0NTQ1ODRiNA=='), 'trakt-api-version': '2'}
        user, password = getTraktCredentials()
        token = cache.get(authTrakt, 24, urlparse.urljoin(trakt_base, '/auth/login'), json.dumps({'login': user, 'password': password}), headers, table='rel_trakt')
        headers.update({'trakt-user-login': user, 'trakt-user-token': token})
    except:
        pass
    try:
        if not post == None: post = json.dumps(post)
        result = client.request(urlparse.urljoin(trakt_base, url), post=post, headers=headers)
        return result
    except:
        pass


def authTrakt(url, post, headers):
    try:
        result = client.request(url, post=post, headers=headers)
        return json.loads(result)['token']
    except:
        pass


def getTraktCredentials():
    user = control.setting('trakt_user') 
    password = control.setting('trakt_password')
    if (user == '' or password == ''): return False
    return (user, password)


def getTraktAddonMovieInfo():
    try: scrobble = control.addon('script.trakt').getSetting('scrobble_movie')
    except: scrobble = ''
    try: ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
    except: ExcludeHTTP = ''
    try: authorization = control.addon('script.trakt').getSetting('authorization')
    except: authorization = ''
    if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '': return True
    else: return False


def getTraktAddonEpisodeInfo():
    try: scrobble = control.addon('script.trakt').getSetting('scrobble_episode')
    except: scrobble = ''
    try: ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
    except: ExcludeHTTP = ''
    try: authorization = control.addon('script.trakt').getSetting('authorization')
    except: authorization = ''
    if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '': return True
    else: return False


def syncMovies(timeout=0):
    try:
        user, password = getTraktCredentials()
        return cache.get(getTrakt, timeout, '/users/%s/watched/movies' % user, table='rel_trakt')
    except:
        pass


def syncTVShows(timeout=0):
    try:
        user, password = getTraktCredentials()
        return cache.get(getTrakt, timeout, '/users/%s/watched/shows?extended=full' % user, table='rel_trakt')
    except:
        pass


def markMovieAsWatched(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt('/sync/history', {"movies": [{"ids": {"imdb": imdb}}]})


def markMovieAsNotWatched(imdb):
    if not imdb.startswith('tt'): imdb = 'tt' + imdb
    return getTrakt('/sync/history/remove', {"movies": [{"ids": {"imdb": imdb}}]})


def markTVShowAsWatched(tvdb):
    return getTrakt('/sync/history', {"shows": [{"ids": {"tvdb": tvdb}}]})


def markTVShowAsNotWatched(tvdb):
    return getTrakt('/sync/history/remove', {"shows": [{"ids": {"tvdb": tvdb}}]})


def markEpisodeAsWatched(tvdb, season, episode):
    season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
    return getTrakt('/sync/history', {"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": tvdb}}]})


def markEpisodeAsNotWatched(tvdb, season, episode):
    season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
    return getTrakt('/sync/history/remove', {"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": tvdb}}]})


def getMovieSummary(id):
    return getTrakt('/movies/%s' % id)


def getTVShowSummary(id):
    return getTrakt('/shows/%s' % id)

