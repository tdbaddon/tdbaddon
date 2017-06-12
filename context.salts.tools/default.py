"""
    SALTS Context Menu XBMC Addon
    Copyright (C) 2015 tknorris

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
"""
import json
import sys
import re
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import kodi
import log_utils

logger = log_utils.Logger.get_logger()
addon = xbmcaddon.Addon('plugin.video.salts')

def __enum(**enums):
    return type('Enum', (), enums)

MODES = __enum(GET_SOURCES='get_sources', SET_URL_MANUAL='set_url_manual', SET_URL_SEARCH='set_url_search', SELECT_SOURCE='select_source', DOWNLOAD_SOURCE='download_source',
               ADD_TO_LIST='add_to_list', SCRAPERS='scrapers', SEARCH='search', AUTOPLAY='autoplay')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
SECTIONS = __enum(TV='TV', MOVIES='Movies')

def toggle_auto_play():
    if __autoplay_enabled():
        addon.setSetting('auto-play', 'false')
        kodi.notify(msg='SALTS Auto-Play Turned Off')
    else:
        addon.setSetting('auto-play', 'true')
        kodi.notify(msg='SALTS Auto-Play Turned On')

def source_action(mode, li_path):
    try:
        lines = xbmcvfs.File(li_path).read()
        lines = lines.replace('mode=%s' % (MODES.GET_SOURCES), 'mode=%s' % (mode))
        if mode in [MODES.SELECT_SOURCE, MODES.AUTOPLAY]:
            builtin = 'PlayMedia'
        else:
            builtin = 'RunPlugin'
        runstring = '%s(%s)' % (builtin, lines)
        xbmc.executebuiltin(runstring)
    except Exception as e:
        logger.log('Failed to read item %s: %s' % (li_path, str(e)), xbmc.LOGERROR)

def set_related_url(mode, media_type, title, year):
    # pull title from infolabels if not provided (i.e. not a widget)
    if title is None:
        if media_type == VIDEO_TYPES.SEASON:
            title = xbmc.getInfoLabel('ListItem.TVShowtitle')
        else:
            title = xbmc.getInfoLabel('ListItem.Title')
        
    # year isn't provided (i.e not a widget)
    if year is None:
        if media_type == VIDEO_TYPES.SEASON:
            year = __get_show_year(title)
            
        if year is None:
            year = xbmc.getInfoLabel('ListItem.Year')
        
    title = re.sub('\s+\(\d{4}\)$', '', title)
    queries = {'mode': mode, 'video_type': media_type, 'title': title, 'year': year, 'trakt_id': 0}  # trakt_id set to 0, not used and don't have it
    if media_type == VIDEO_TYPES.SEASON:
        queries['season'] = xbmc.getInfoLabel('ListItem.Season')
    runstring = 'RunPlugin(plugin://plugin.video.salts%s)' % (kodi.get_plugin_url(queries))
    xbmc.executebuiltin(runstring)
    
def add_to_list():
    show_id = {'show_id': xbmc.getInfoLabel('ListItem.IMDBNumber')}
    if __get_media_type() == VIDEO_TYPES.TVSHOW:
        show_id['id_type'] = 'tvdb'
        section = SECTIONS.TV
    elif __get_media_type() == VIDEO_TYPES.MOVIE:
        show_id['id_type'] = 'tmdb'
        section = SECTIONS.MOVIES

    # override id_type if it looks like an imdb #
    if show_id['show_id'].startswith('tt'):
        show_id['id_type'] = 'imdb'
    
    if 'id_type' in show_id:
        queries = {'mode': MODES.ADD_TO_LIST, 'section': section}
        queries.update(show_id)
        runstring = 'RunPlugin(plugin://plugin.video.salts%s)' % (kodi.get_plugin_url(queries))
        xbmc.executebuiltin(runstring)

def scraper_sort_order():
    queries = {'mode': MODES.SCRAPERS}
    runstring = 'RunAddon(plugin.video.salts,%s)' % (kodi.get_plugin_url(queries))
    xbmc.executebuiltin(runstring)
    
def addon_settings():
    xbmc.executebuiltin('Addon.OpenSettings(plugin.video.salts)')

def search(section):
    queries = {'mode': MODES.SEARCH, 'section': section}
    runstring = 'RunPlugin(plugin://plugin.video.salts%s)' % (kodi.get_plugin_url(queries))
    xbmc.executebuiltin(runstring)
    
def __get_show_year(title):
    filter_params = {'field': 'title', 'operator': 'contains', 'value': title}
    properties = ['title', 'year']
    sort = {'order': 'ascending', 'method': 'label', 'ignorearticle': True}
    limits = {'start': 0, 'end': 25}
    params = {'filter': filter_params, 'properties': properties, 'sort': sort, 'limits': limits}
    cmd = {'jsonrpc': '2.0', 'method': 'VideoLibrary.GetTVShows', 'params': params, 'id': 'libTvShows'}
    meta = kodi.execute_jsonrpc(cmd)
    logger.log('Search Meta: %s' % (meta), log_utils.LOGDEBUG)
    try: return meta['result']['tvshows'][0]['year']
    except (KeyError, IndexError): return None

def __autoplay_enabled():
    return addon.getSetting('auto-play') == 'true'
    
def __get_media_type():
    if xbmc.getCondVisibility('Container.Content(tvshows)'):
        return VIDEO_TYPES.TVSHOW
    elif xbmc.getCondVisibility('Container.Content(seasons)'):
        return VIDEO_TYPES.SEASON
    elif xbmc.getCondVisibility('Container.Content(episodes)'):
        return VIDEO_TYPES.EPISODE
    elif xbmc.getCondVisibility('Container.Content(movies)'):
        return VIDEO_TYPES.MOVIE
    else:
        return None
    
def __is_salts_listitem(li_path):
    tvshow_folder = __get_folder('tvshow-folder')
    movie_folder = __get_folder('movie-folder')
    real_path = xbmc.translatePath(li_path)
    if not real_path.startswith(movie_folder) and not real_path.startswith(tvshow_folder):
        logger.log('Path Mismatch: |%s|%s|%s|' % (real_path, movie_folder, tvshow_folder))
        return False
    
    try:
        lines = xbmcvfs.File(li_path).read()
        if lines and not lines.startswith('plugin://plugin.video.salts'):
            logger.log('STRM Mistmatch: %s' % (lines))
            return False
    except Exception as e:
        logger.log('Failed to read item %s: %s' % (li_path, str(e)), xbmc.LOGERROR)
    
    return True

def __get_folder(setting):
    folder = xbmc.translatePath(addon.getSetting(setting))
    folder = re.sub('://[^/]+@', '://', folder)
    return folder
    
def __get_tools(path, media_type, title, year):
    if __autoplay_enabled():
        action = MODES.SELECT_SOURCE
        label = 'Select Source'
    else:
        action = MODES.AUTOPLAY
        label = 'Auto-Play'
        
    tools = [
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE), 'Toggle Auto-Play', toggle_auto_play, []),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE), label, source_action, [action, path]),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE), 'Download Source', source_action, [MODES.DOWNLOAD_SOURCE, path]),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW), 'Add to List', add_to_list, []),
        ((VIDEO_TYPES.MOVIE), 'Movie Search', search, [SECTIONS.MOVIES]),
        ((VIDEO_TYPES.TVSHOW), 'TV Show Search', search, [SECTIONS.TV]),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE), 'Scraper Sort Order', scraper_sort_order, []),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE), 'Addon Settings', addon_settings, []),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON), 'Set Related Url (Search)', set_related_url, [MODES.SET_URL_SEARCH, media_type, title, year]),
        ((VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.SEASON), 'Set Related Url (Manual)', set_related_url, [MODES.SET_URL_MANUAL, media_type, title, year])
    ]
    
    new_tools = [(tool[1:]) for tool in tools if media_type in tool[0]]
    return new_tools

def __get_widget_details(filename, title, year):
    if not isinstance(title, unicode): title = title.decode('utf-8')
    path = ''
    media_type = None

    try: _filename, extra = filename.split('?')
    except: _filename, extra = filename.split('?')[0], ''
    tokens = _filename.split('/')
    queries = kodi.parse_query(extra)
    for value in queries.itervalues():
        try: js_data = json.loads(value)
        except: js_data = {}
        js_type = js_data.get('type')
        if js_type == 'tvshows':
            media_type = VIDEO_TYPES.TVSHOW
            break
        elif js_type == 'episodes':
            media_type = VIDEO_TYPES.EPISODE
            break
        elif js_type == 'movies':
            media_type = VIDEO_TYPES.MOVIE
            break
    else:
        for token in tokens:
            if 'movie' in token:
                media_type = VIDEO_TYPES.MOVIE
                break
            elif 'tvshow' in token:
                media_type = VIDEO_TYPES.TVSHOW
                break
            elif 'episode' in token:
                media_type = VIDEO_TYPES.EPISODE
                break
    
    if media_type == VIDEO_TYPES.MOVIE:
        lib_id = 'libMovies'
        method = 'VideoLibrary.GetMovieDetails'
        id_type = 'movieid'
        details = 'moviedetails'
        properties = ['file', 'title', 'year']
    elif media_type == VIDEO_TYPES.TVSHOW:
        lib_id = 'libTvShows'
        method = 'VideoLibrary.GetTVShowDetails'
        id_type = 'tvshowid'
        details = 'tvshowdetails'
        properties = ['file', 'title', 'year']
    elif media_type == VIDEO_TYPES.EPISODE:
        lib_id = 'libTvShows'
        method = 'VideoLibrary.GetEpisodeDetails'
        id_type = 'episodeid'
        details = 'episodedetails'
        properties = ['file', 'title']
    
    if media_type is not None:
        for token in tokens:
            if token.isdigit():
                cmd = {'jsonrpc': '2.0', 'method': method, 'params': {id_type: int(token), 'properties': properties}, 'id': lib_id}
                response = kodi.execute_jsonrpc(cmd)
                logger.log('Details Result: %s' % (response), log_utils.LOGDEBUG)
                if 'result' in response and details in response['result']:
                    details = response['result'][details]
                    if details['title'] == title and ('year' not in details or details['year'] == year):
                        path = details['file']
    
    logger.log('Widget ID: |%s| -> (%s): |%s|' % (filename, media_type, path))
    return media_type, path
        
def main(argv=None):
    if sys.argv: argv = sys.argv
    logger.log('Version: |%s|' % (kodi.get_version()))
    logger.log('Args: |%s|' % (argv))
    title = None
    year = None
    media_type = __get_media_type()
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    if not path:
        path = xbmc.getInfoLabel('ListItem.Path')

    # assume this is a widget if we couldn't get a path infolabel
    if not path:
        filename = sys.listitem.getfilename()  # @UndefinedVariable
        title = sys.listitem.getVideoInfoTag().getTitle()  # @UndefinedVariable
        year = sys.listitem.getVideoInfoTag().getYear()  # @UndefinedVariable
        if filename.startswith('videodb://'):
            media_type, path = __get_widget_details(filename, title, year)
        
    if __is_salts_listitem(path):
        dialog = xbmcgui.Dialog()
        tools = __get_tools(path, media_type, title, year)
        try: ret = dialog.contextmenu([i[0] for i in tools])
        except: ret = dialog.select('SALTS Tools', [i[0] for i in tools])
        if ret > -1:
            tools[ret][1](*tools[ret][2])
    else:
        kodi.notify(msg='Not a SALTS Library Item')

if __name__ == '__main__':
    sys.exit(main())
