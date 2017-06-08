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
import xbmc
import base64

from . import control

def getMovieIndicators(refresh=False):
    try:
        from metahandler import metahandlers
        indicators = metahandlers.MetaData(preparezip=False)
        return indicators
    except:
        pass

def getTVShowIndicators(refresh=False):
    try:
        from metahandler import metahandlers
        indicators = metahandlers.MetaData(preparezip=False)
        return indicators
    except:
        pass

def getMovieOverlay(indicators, imdb):
    try:
        try:
            playcount = indicators._get_watched('movie', imdb, '', '')
            return str(playcount)
        except:
            playcount = [i for i in indicators if i == imdb]
            playcount = 7 if len(playcount) > 0 else 6
            return str(playcount)
    except:
        return '6'

def getEpisodeOverlay(indicators, tvshowtitle, episode, season=''):
    try:
        try:
            playcount = indicators._get_watched_episode({'title':tvshowtitle, 'season' : season, 'episode': episode, 'premiered' : ''})
            return str(playcount)
        except:
            return '6'
            #playcount = [i[2] for i in indicators if i[0] == tvdb]
            #playcount = playcount[0] if len(playcount) > 0 else []
            #playcount = [i for i in playcount if int(season) == int(i[0]) and int(episode) == int(i[1])]
            #playcount = 7 if len(playcount) > 0 else 6
            #return str(playcount)
    except:
        return '6'

def movies(title, year, imdb, watched):
    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('movie', name='', imdb_id=imdb)
        metaget.change_watched('movie', name='', imdb_id=imdb, watched=int(watched))
    except :
        pass

    control.refresh()

def episodes(tvshowtitle, episode, watched, season=''):

    watched = int(watched)

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('tvshow', tvshowtitle)
        metaget.get_episode_meta(tvshowtitle, imdb=None, season=None, episode=episode)
        metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)
    except:
        pass

    control.refresh()

def tvshows(imdb, tvdb, season, episode, watched):

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('tvshow', name='', imdb_id=imdb)
        metaget.get_episode_meta('', imdb_id=imdb, season=season, episode=episode)
        metaget.change_watched('episode', '', imdb_id=imdb, season=season, episode=episode, watched=int(watched))
    except:
        import traceback
        traceback.print_exc()
        pass

    control.refresh()