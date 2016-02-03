"""
    SALTS XBMC Addon
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
import os
import time
import _strptime
import re
import datetime
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import log_utils
import sys
import urlparse
import urllib
import urllib2
import traceback
import random
import xml.etree.ElementTree as ET
import kodi
from constants import *
from trans_utils import i18n
from scrapers import *  # import all scrapers into this namespace
from trakt_api import Trakt_API
from db_utils import DB_Connection
import threading

ICON_PATH = os.path.join(kodi.get_path(), 'icon.png')
SORT_FIELDS = [
    (SORT_LIST[int(kodi.get_setting('sort1_field'))], SORT_SIGNS[kodi.get_setting('sort1_order')]),
    (SORT_LIST[int(kodi.get_setting('sort2_field'))], SORT_SIGNS[kodi.get_setting('sort2_order')]),
    (SORT_LIST[int(kodi.get_setting('sort3_field'))], SORT_SIGNS[kodi.get_setting('sort3_order')]),
    (SORT_LIST[int(kodi.get_setting('sort4_field'))], SORT_SIGNS[kodi.get_setting('sort4_order')]),
    (SORT_LIST[int(kodi.get_setting('sort5_field'))], SORT_SIGNS[kodi.get_setting('sort5_order')]),
    (SORT_LIST[int(kodi.get_setting('sort6_field'))], SORT_SIGNS[kodi.get_setting('sort6_order')])]

last_check = datetime.datetime.fromtimestamp(0)

TOKEN = kodi.get_setting('trakt_oauth_token')
use_https = kodi.get_setting('use_https') == 'true'
trakt_timeout = int(kodi.get_setting('trakt_timeout'))
list_size = int(kodi.get_setting('list_size'))
trakt_api = Trakt_API(TOKEN, use_https, list_size, trakt_timeout)
db_connection = DB_Connection()

THEME_LIST = ['Shine', 'Luna_Blue', 'Iconic', 'Simple', 'SALTy', 'SALTy (Blended)', 'SALTy (Blue)', 'SALTy (Frog)', 'SALTy (Green)',
              'SALTy (Macaw)', 'SALTier (Green)', 'SALTier (Orange)', 'SALTier (Red)', 'IGDB', 'Simply Elegant', 'IGDB Redux']
THEME = THEME_LIST[int(kodi.get_setting('theme'))]
if xbmc.getCondVisibility('System.HasAddon(script.salts.themepak)'):
    themepak_path = xbmcaddon.Addon('script.salts.themepak').getAddonInfo('path')
else:
    themepak_path = kodi.get_path()
THEME_PATH = os.path.join(themepak_path, 'art', 'themes', THEME)
PLACE_POSTER = os.path.join(kodi.get_path(), 'resources', 'place_poster.png')

def art(name):
    path = os.path.join(THEME_PATH, name)
    if not xbmcvfs.exists(path):
        if name == 'fanart.jpg':
            path = os.path.join(kodi.get_path(), name)
        else:
            path.replace('.png', '.jpg')
    return path

def choose_list(username=None):
    lists = trakt_api.get_lists(username)
    if username is None: lists.insert(0, {'name': 'watchlist', 'ids': {'slug': WATCHLIST_SLUG}})
    if lists:
        dialog = xbmcgui.Dialog()
        index = dialog.select(i18n('pick_a_list'), [list_data['name'] for list_data in lists])
        if index > -1:
            return lists[index]['ids']['slug']
    else:
        kodi.notify(msg=i18n('no_lists_for_user') % (username), duration=5000)

def show_id(show):
    queries = {}
    ids = show['ids']
    if 'trakt' in ids and ids['trakt']:
        queries['id_type'] = 'trakt'
        queries['show_id'] = ids['trakt']
    elif 'imdb' in ids and ids['imdb']:
        queries['id_type'] = 'imdb'
        queries['show_id'] = ids['imdb']
    elif 'tvdb' in ids and ids['tvdb']:
        queries['id_type'] = 'tvdb'
        queries['show_id'] = ids['tvdb']
    elif 'tmdb' in ids and ids['tmdb']:
        queries['id_type'] = 'tmdb'
        queries['show_id'] = ids['tmdb']
    elif 'tvrage' in ids and ids['tvrage']:
        queries['id_type'] = 'tvrage'
        queries['show_id'] = ids['tvrage']
    elif 'slug' in ids and ids['slug']:
        queries['id_type'] = 'slug'
        queries['show_id'] = ids['slug']
    return queries

def update_url(video_type, title, year, source, old_url, new_url, season, episode):
    log_utils.log('Setting Url: |%s|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title.decode('utf-8').encode('ascii', 'xmlcharrefreplace'), year, source, old_url, new_url, season, episode), log_utils.LOGDEBUG)
    if new_url:
        db_connection.set_related_url(video_type, title, year, source, new_url, season, episode)
    else:
        db_connection.clear_related_url(video_type, title, year, source, season, episode)

    # clear all episode local urls if tvshow url changes
    if video_type == VIDEO_TYPES.TVSHOW and new_url != old_url:
        db_connection.clear_related_url(VIDEO_TYPES.EPISODE, title, year, source)

def make_seasons_info(progress):
    season_info = {}
    if progress:
        for season in progress['seasons']:
            info = {}
            if 'aired' in season: info['episode'] = info['TotalEpisodes'] = season['aired']
            if 'completed' in season: info['WatchedEpisodes'] = season['completed']
            if 'aired' in season and 'completed' in season:
                info['UnWatchedEpisodes'] = season['aired'] - season['completed']
                info['playcount'] = season['aired'] if season['completed'] == season['aired'] else 0

            if 'number' in season: info['season'] = season['number']
            season_info[str(season['number'])] = info
    return season_info

def make_episodes_watched(episodes, progress):
    watched = {}
    for season in progress['seasons']:
        watched[str(season['number'])] = {}
        for ep_status in season['episodes']:
            watched[str(season['number'])][str(ep_status['number'])] = ep_status['completed']

    for episode in episodes:
        season_str = str(episode['season'])
        episode_str = str(episode['number'])
        if season_str in watched and episode_str in watched[season_str]:
            episode['watched'] = watched[season_str][episode_str]
        else:
            episode['watched'] = False

    return episodes

def make_list_item(label, meta):
    art = make_art(meta)
    listitem = xbmcgui.ListItem(label, iconImage=art['thumb'], thumbnailImage=art['thumb'])
    listitem.setProperty('fanart_image', art['fanart'])
    try: listitem.setArt(art)
    except: pass
    if 'ids' in meta and 'imdb' in meta['ids']: listitem.setProperty('imdb_id', str(meta['ids']['imdb']))
    if 'ids' in meta and 'tvdb' in meta['ids']: listitem.setProperty('tvdb_id', str(meta['ids']['tvdb']))
    return listitem

def make_art(show):
    min_size = int(kodi.get_setting('image_size'))
    art_dict = {'banner': '', 'fanart': art('fanart.jpg'), 'thumb': '', 'poster': PLACE_POSTER}
    if 'images' in show:
        images = show['images']
        for i in range(0, min_size + 1):
            if 'banner' in images and IMG_SIZES[i] in images['banner'] and images['banner'][IMG_SIZES[i]]: art_dict['banner'] = images['banner'][IMG_SIZES[i]]
            if 'fanart' in images and IMG_SIZES[i] in images['fanart'] and images['fanart'][IMG_SIZES[i]]: art_dict['fanart'] = images['fanart'][IMG_SIZES[i]]
            if 'poster' in images and IMG_SIZES[i] in images['poster'] and images['poster'][IMG_SIZES[i]]: art_dict['thumb'] = art_dict['poster'] = images['poster'][IMG_SIZES[i]]
            if 'thumb' in images and IMG_SIZES[i] in images['thumb'] and images['thumb'][IMG_SIZES[i]]: art_dict['thumb'] = images['thumb'][IMG_SIZES[i]]
            if 'screen' in images and IMG_SIZES[i] in images['screen'] and images['screen'][IMG_SIZES[i]]: art_dict['thumb'] = images['screen'][IMG_SIZES[i]]
            if 'screenshot' in images and IMG_SIZES[i] in images['screenshot'] and images['screenshot'][IMG_SIZES[i]]: art_dict['thumb'] = images['screenshot'][IMG_SIZES[i]]
            if 'logo' in images and IMG_SIZES[i] in images['logo'] and images['logo'][IMG_SIZES[i]]: art_dict['clearlogo'] = images['logo'][IMG_SIZES[i]]
            if 'clearart' in images and IMG_SIZES[i] in images['clearart'] and images['clearart'][IMG_SIZES[i]]: art_dict['clearart'] = images['clearart'][IMG_SIZES[i]]
    return art_dict

def make_info(item, show=None, people=None):
    if people is None: people = {}
    if show is None: show = {}
    # log_utils.log('Making Info: Show: %s' % (show), xbmc.LOGDEBUG)
    # log_utils.log('Making Info: Item: %s' % (item), xbmc.LOGDEBUG)
    info = {}
    info['title'] = item['title']
    if 'overview' in item: info['plot'] = info['plotoutline'] = item['overview']
    if 'runtime' in item and item['runtime'] is not None: info['duration'] = item['runtime'] * 60
    if 'certification' in item: info['mpaa'] = item['certification']
    if 'year' in item: info['year'] = item['year']
    if 'season' in item: info['season'] = item['season']  # needs check
    if 'episode' in item: info['episode'] = item['episode']  # needs check
    if 'number' in item: info['episode'] = item['number']  # needs check
    if 'genres' in item:
        genres = dict((genre['slug'], genre['name']) for genre in trakt_api.get_genres(SECTIONS.TV))
        genres.update(dict((genre['slug'], genre['name']) for genre in trakt_api.get_genres(SECTIONS.MOVIES)))
        item_genres = [genres[genre] for genre in item['genres'] if genre in genres]
        info['genre'] = ', '.join(item_genres)
    if 'network' in item: info['studio'] = item['network']
    if 'status' in item: info['status'] = item['status']
    if 'tagline' in item: info['tagline'] = item['tagline']
    if 'watched' in item and item['watched']: info['playcount'] = 1
    if 'plays' in item and item['plays']: info['playcount'] = item['plays']
    if 'rating' in item: info['rating'] = item['rating']
    if 'votes' in item: info['votes'] = item['votes']
    if 'released' in item: info['premiered'] = item['released']
    if 'trailer' in item and item['trailer']: info['trailer'] = make_trailer(item['trailer'])
    if 'first_aired' in item: info['aired'] = info['premiered'] = make_air_date(item['first_aired'])
    info.update(make_ids(item))

    if 'aired_episodes' in item:
        info['episode'] = info['TotalEpisodes'] = item['aired_episodes']
        info['WatchedEpisodes'] = item['watched_count'] if 'watched_count' in item else 0
        info['UnWatchedEpisodes'] = info['TotalEpisodes'] - info['WatchedEpisodes']

    # override item params with show info if it exists
    if 'certification' in show: info['mpaa'] = show['certification']
    if 'year' in show: info['year'] = show['year']
    if 'runtime' in show and show['runtime'] is not None: info['duration'] = show['runtime'] * 60
    if 'title' in show: info['tvshowtitle'] = show['title']
    if 'network' in show: info['studio'] = show['network']
    if 'status' in show: info['status'] = show['status']
    if 'trailer' in show and show['trailer']: info['trailer'] = make_trailer(show['trailer'])
    info.update(make_ids(show))
    info.update(make_people(people))
    return info

def make_trailer(trailer_url):
    match = re.search('\?v=(.*)', trailer_url)
    if match:
        return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1))

def make_ids(item):
    info = {}
    if 'ids' in item:
        ids = item['ids']
        if 'imdb' in ids: info['code'] = info['imdbnumber'] = info['imdb_id'] = ids['imdb']
        if 'tmdb' in ids: info['tmdb_id'] = ids['tmdb']
        if 'tvdb' in ids: info['tvdb_id'] = ids['tvdb']
        if 'trakt' in ids: info['trakt_id'] = ids['trakt']
        if 'slug' in ids: info['slug'] = ids['slug']
    return info

def make_people(item):
    people = {}
    if 'cast' in item: people['castandrole'] = people['cast'] = [(person['person']['name'], person['character']) for person in item['cast']]
    if 'crew' in item and 'directing' in item['crew']:
        directors = [director['person']['name'] for director in item['crew']['directing'] if director['job'].lower() == 'director']
        people['director'] = ', '.join(directors)
    if 'crew' in item and 'writing' in item['crew']:
        writers = [writer['person']['name'] for writer in item['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']]
        people['writer'] = ', '.join(writers)

    return people

def make_air_date(first_aired):
    utc_air_time = iso_2_utc(first_aired)
    try: air_date = time.strftime('%Y-%m-%d', time.localtime(utc_air_time))
    except ValueError:  # windows throws a ValueError on negative values to localtime
        d = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=utc_air_time)
        air_date = d.strftime('%Y-%m-%d')
    return air_date

def get_section_params(section):
    section_params = {}
    section_params['section'] = section
    if section == SECTIONS.TV:
        section_params['next_mode'] = MODES.SEASONS
        section_params['folder'] = True
        section_params['video_type'] = VIDEO_TYPES.TVSHOW
        section_params['content_type'] = CONTENT_TYPES.TVSHOWS
        section_params['search_img'] = 'television_search.png'
        section_params['label_plural'] = i18n('tv_shows')
        section_params['label_single'] = i18n('tv_show')
    else:
        section_params['next_mode'] = MODES.GET_SOURCES
        section_params['folder'] = kodi.get_setting('source-win') == 'Directory' and kodi.get_setting('auto-play') == 'false'
        section_params['video_type'] = VIDEO_TYPES.MOVIE
        section_params['content_type'] = CONTENT_TYPES.MOVIES
        section_params['search_img'] = 'movies_search.png'
        section_params['label_plural'] = i18n('movies')
        section_params['label_single'] = i18n('movie')

    return section_params

def filename_from_title(title, video_type, year=None):
    if video_type == VIDEO_TYPES.TVSHOW:
        filename = '%s S%sE%s.strm'
        filename = filename % (title, '%s', '%s')
    else:
        if year: title = '%s (%s)' % (title, year)
        filename = '%s.strm' % title

    filename = re.sub(r'(?!%s)[^\w\-_\.]', '.', filename)
    filename = re.sub('\.+', '.', filename)
    xbmc.makeLegalFilename(filename)
    return filename

def filter_unknown_hosters(hosters):
    filtered_hosters = []
    for host in hosters:
        for key, _ in SORT_FIELDS:
            if key in host and host[key] is None:
                break
        else:
            filtered_hosters.append(host)
    return filtered_hosters

def filter_exclusions(hosters):
    exclusions = kodi.get_setting('excl_list')
    exclusions = exclusions.replace(' ', '')
    exclusions = exclusions.lower()
    if not exclusions: return hosters
    filtered_hosters = []
    for hoster in hosters:
        if hoster['host'].lower() in exclusions:
            log_utils.log('Excluding %s (%s) from %s' % (hoster['url'], hoster['host'], hoster['class'].get_name()), log_utils.LOGDEBUG)
            continue
        filtered_hosters.append(hoster)
    return filtered_hosters

def filter_quality(video_type, hosters):
    qual_filter = 5 - int(kodi.get_setting('%s_quality' % video_type))  # subtract to match Q_ORDER
    if qual_filter == 5:
        return hosters
    else:
        return [hoster for hoster in hosters if Q_ORDER[hoster['quality']] <= qual_filter]

def get_sort_key(item):
    item_sort_key = []
    for field, sign in SORT_FIELDS:
        if field == 'none':
            break
        elif field in SORT_KEYS:
            if field == 'source':
                value = item['class'].get_name()
            else:
                value = item[field]

            if value in SORT_KEYS[field]:
                item_sort_key.append(sign * int(SORT_KEYS[field][value]))
            else:  # assume all unlisted values sort as worst
                item_sort_key.append(sign * -1)
        elif field == 'debrid':
            if field in item:
                item_sort_key.append(sign * bool(item[field]))
            else:
                item_sort_key.append(sign * -1)
        else:
            if item[field] is None:
                item_sort_key.append(sign * -1)
            else:
                item_sort_key.append(sign * int(item[field]))
    # print 'item: %s sort_key: %s' % (item, item_sort_key)
    return tuple(item_sort_key)

def make_source_sort_key():
    sso = kodi.get_setting('source_sort_order')
    # migrate sso to kodi setting
    if not sso:
        sso = db_connection.get_setting('source_sort_order')
        sso = kodi.set_setting('source_sort_order', sso)
        db_connection.set_setting('source_sort_order', '')
        
    sort_key = {}
    i = 0
    scrapers = relevant_scrapers(include_disabled=True)
    scraper_names = [scraper.get_name() for scraper in scrapers]
    if sso:
        sources = sso.split('|')
        sort_key = {}
        for i, source in enumerate(sources):
            if source in scraper_names:
                sort_key[source] = -i

    for j, scraper in enumerate(scrapers):
        if scraper.get_name() not in sort_key:
            sort_key[scraper.get_name()] = -(i + j)

    return sort_key

def get_source_sort_key(item):
    sort_key = make_source_sort_key()
    return -sort_key[item.get_name()]

def make_source_sort_string(sort_key):
    sorted_key = sorted(sort_key.items(), key=lambda x: -x[1])
    sort_string = '|'.join([element[0] for element in sorted_key])
    return sort_string

def start_worker(q, func, args):
    worker = threading.Thread(target=func, args=([q] + args))
    worker.daemon = True
    worker.start()
    return worker

def reap_workers(workers, timeout=0):
    """
    Reap thread/process workers; don't block by default; return un-reaped workers
    """
    log_utils.log('In Reap: %s' % (workers), log_utils.LOGDEBUG)
    living_workers = []
    for worker in workers:
        if worker:
            log_utils.log('Reaping: %s' % (worker.name), log_utils.LOGDEBUG)
            worker.join(timeout)
            if worker.is_alive():
                log_utils.log('Worker %s still running' % (worker.name), log_utils.LOGDEBUG)
                living_workers.append(worker)
    return living_workers

def parallel_get_sources(q, scraper, video):
    worker = threading.current_thread()
    log_utils.log('Worker: %s (%s) for %s sources' % (worker.name, worker, scraper.get_name()), log_utils.LOGDEBUG)
    hosters = scraper.get_sources(video)
    if hosters is None: hosters = []
    if kodi.get_setting('filter_direct') == 'true':
        hosters = [hoster for hoster in hosters if not hoster['direct'] or test_stream(hoster)]
    for hoster in hosters:
        if not hoster['direct']:
            hoster['host'] = hoster['host'].lower().strip()
    log_utils.log('%s returned %s sources from %s' % (scraper.get_name(), len(hosters), worker), log_utils.LOGDEBUG)
    result = {'name': scraper.get_name(), 'hosters': hosters}
    q.put(result)

def parallel_get_url(q, scraper, video):
    worker = threading.current_thread()
    log_utils.log('Worker: %s (%s) for %s url' % (worker.name, worker, scraper.get_name()), log_utils.LOGDEBUG)
    url = scraper.get_url(video)
    log_utils.log('%s returned url %s from %s' % (scraper.get_name(), url, worker), log_utils.LOGDEBUG)
    if not url: url = ''
    if url == FORCE_NO_MATCH:
        label = '[%s] [COLOR green]%s[/COLOR]' % (scraper.get_name(), i18n('force_no_match'))
    else:
        label = '[%s] %s' % (scraper.get_name(), url)
    related = {'class': scraper, 'url': url, 'name': scraper.get_name(), 'label': label}
    q.put(related)

def parallel_get_progress(q, trakt_id, cached):
    worker = threading.current_thread()
    log_utils.log('Worker: %s (%s) for %s progress' % (worker.name, worker, trakt_id), log_utils.LOGDEBUG)
    progress = trakt_api.get_show_progress(trakt_id, full=True, cached=cached)
    progress['trakt'] = trakt_id  # add in a hacked show_id to be used to match progress up to the show its for
    log_utils.log('Got progress for %s from %s' % (trakt_id, worker), log_utils.LOGDEBUG)
    q.put(progress)

def test_stream(hoster):
    # parse_qsl doesn't work because it splits elements by ';' which can be in a non-quoted UA
    try:
        headers = dict([item.split('=') for item in (hoster['url'].split('|')[1]).split('&')])
        for key in headers: headers[key] = urllib.unquote(headers[key])
    except:
        headers = {}
    log_utils.log('Testing Stream: %s from %s using Headers: %s' % (hoster['url'], hoster['class'].get_name(), headers), xbmc.LOGDEBUG)
    request = urllib2.Request(hoster['url'].split('|')[0], headers=headers)

    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    urllib2.install_opener(opener)
    #  set urlopen timeout to 1 seconds
    try: http_code = urllib2.urlopen(request, timeout=1).getcode()
    except urllib2.URLError as e:
        # treat an unhandled url type as success
        if hasattr(e, 'reason') and 'unknown url type' in str(e.reason).lower():
            return True
        else:
            if isinstance(e, urllib2.HTTPError):
                http_code = e.code
            else:
                http_code = 600
    except Exception as e:
        if 'unknown url type' in str(e).lower():
            return True
        else:
            log_utils.log('Exception during test_stream: (%s) %s' % (type(e).__name__, e), xbmc.LOGDEBUG)
            http_code = 601

    if int(http_code) >= 400:
        log_utils.log('Test Stream Failed: Url: %s HTTP Code: %s' % (hoster['url'], http_code), xbmc.LOGDEBUG)

    return int(http_code) < 400

# Run a task on startup. Settings and mode values must match task name
def do_startup_task(task):
    run_on_startup = kodi.get_setting('auto-%s' % task) == 'true' and kodi.get_setting('%s-during-startup' % task) == 'true'
    if run_on_startup and not xbmc.abortRequested:
        log_utils.log('Service: Running startup task [%s]' % (task))
        now = datetime.datetime.now()
        xbmc.executebuiltin('RunPlugin(plugin://%s/?mode=%s)' % (kodi.get_id(), task))
        db_connection.set_setting('%s-last_run' % (task), now.strftime("%Y-%m-%d %H:%M:%S.%f"))

# Run a recurring scheduled task. Settings and mode values must match task name
def do_scheduled_task(task, isPlaying):
    global last_check
    now = datetime.datetime.now()
    if kodi.get_setting('auto-%s' % task) == 'true':
        if last_check < now - datetime.timedelta(minutes=1):
            # log_utils.log('Check Triggered: Last: %s Now: %s' % (last_check, now), log_utils.LOGDEBUG)
            next_run = get_next_run(task)
            last_check = now
        else:
            # hack next_run to be in the future
            next_run = now + datetime.timedelta(seconds=1)

        # log_utils.log("Update Status on [%s]: Currently: %s Will Run: %s Last Check: %s" % (task, now, next_run, last_check), xbmc.LOGDEBUG)
        if now >= next_run:
            is_scanning = xbmc.getCondVisibility('Library.IsScanningVideo')
            if not is_scanning:
                during_playback = kodi.get_setting('%s-during-playback' % (task)) == 'true'
                if during_playback or not isPlaying:
                    log_utils.log('Service: Running Scheduled Task: [%s]' % (task))
                    builtin = 'RunPlugin(plugin://%s/?mode=%s)' % (kodi.get_id(), task)
                    xbmc.executebuiltin(builtin)
                    db_connection.set_setting('%s-last_run' % task, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                else:
                    log_utils.log('Service: Playing... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)
            else:
                log_utils.log('Service: Scanning... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)

def get_next_run(task):
    # strptime mysteriously fails sometimes with TypeError; this is a hacky workaround
    # note, they aren't 100% equal as time.strptime loses fractional seconds but they are close enough
    try:
        last_run_string = db_connection.get_setting(task + '-last_run')
        if not last_run_string: last_run_string = LONG_AGO
        last_run = datetime.datetime.strptime(last_run_string, "%Y-%m-%d %H:%M:%S.%f")
    except (TypeError, ImportError):
        last_run = datetime.datetime(*(time.strptime(last_run_string, '%Y-%m-%d %H:%M:%S.%f')[0:6]))
    interval = datetime.timedelta(hours=float(kodi.get_setting(task + '-interval')))
    return (last_run + interval)

def url_exists(video):
    """
    check each source for a url for this video; return True as soon as one is found. If none are found, return False
    """
    max_timeout = int(kodi.get_setting('source_timeout'))
    log_utils.log('Checking for Url Existence: |%s|' % (video), log_utils.LOGDEBUG)
    for cls in relevant_scrapers(video.video_type):
        if kodi.get_setting('%s-sub_check' % (cls.get_name())) == 'true':
            scraper_instance = cls(max_timeout)
            url = scraper_instance.get_url(video)
            if url:
                log_utils.log('Found url for |%s| @ %s: %s' % (video, cls.get_name(), url), log_utils.LOGDEBUG)
                return True

    log_utils.log('No url found for: |%s|' % (video))
    return False

def relevant_scrapers(video_type=None, include_disabled=False, order_matters=False):
    classes = scraper.Scraper.__class__.__subclasses__(scraper.Scraper)
    relevant = []
    for cls in classes:
        if video_type is None or video_type in cls.provides():
            if include_disabled or scraper_enabled(cls.get_name()):
                relevant.append(cls)

    if order_matters:
        relevant.sort(key=get_source_sort_key)
    return relevant

def scraper_enabled(name):
    # return true if setting exists and set to true, or setting doesn't exist (i.e. '')
    return kodi.get_setting('%s-enable' % (name)) in ['true', '']

def set_view(content, set_sort):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    view = kodi.get_setting('%s_view' % (content))
    if view != '0':
        log_utils.log('Setting View to %s (%s)' % (view, content), log_utils.LOGDEBUG)
        xbmc.executebuiltin('Container.SetViewMode(%s)' % (view))

    # set sort methods - probably we don't need all of them
    if set_sort:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_GENRE)

def make_day(date):
    try: date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except TypeError: date = datetime.datetime(*(time.strptime(date, '%Y-%m-%d')[0:6])).date()
    today = datetime.date.today()
    day_diff = (date - today).days
    if day_diff == -1:
        date = 'YDA'
    elif day_diff == 0:
        date = 'TDA'
    elif day_diff == 1:
        date = 'TOM'
    elif day_diff > 1 and day_diff < 7:
        date = date.strftime('%a')

    return date

def make_time(utc_ts):
    local_time = time.localtime(utc_ts)
    if kodi.get_setting('calendar_time') == '1':
        time_format = '%H:%M'
        time_str = time.strftime(time_format, local_time)
    else:
        time_format = '%I%p' if local_time.tm_min == 0 else '%I:%M%p'
        time_str = time.strftime(time_format, local_time)
        if time_str[0] == '0': time_str = time_str[1:]
    return time_str

def iso_2_utc(iso_ts):
    if not iso_ts or iso_ts is None: return 0
    delim = -1
    if not iso_ts.endswith('Z'):
        delim = iso_ts.rfind('+')
        if delim == -1: delim = iso_ts.rfind('-')

    if delim > -1:
        ts = iso_ts[:delim]
        sign = iso_ts[delim]
        tz = iso_ts[delim + 1:]
    else:
        ts = iso_ts
        tz = None

    if ts.find('.') > -1:
        ts = ts[:ts.find('.')]

    try: d = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
    except TypeError: d = datetime.datetime(*(time.strptime(ts, '%Y-%m-%dT%H:%M:%S')[0:6]))

    dif = datetime.timedelta()
    if tz:
        hours, minutes = tz.split(':')
        hours = int(hours)
        minutes = int(minutes)
        if sign == '-':
            hours = -hours
            minutes = -minutes
        dif = datetime.timedelta(minutes=minutes, hours=hours)
    utc_dt = d - dif
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = utc_dt - epoch
    try: seconds = delta.total_seconds()  # works only on 2.7
    except: seconds = delta.seconds + delta.days * 24 * 3600  # close enough
    return seconds

def format_sub_label(sub):
    label = '%s - [%s] - (' % (sub['language'], sub['version'])
    if sub['completed']:
        color = 'green'
    else:
        label += '%s%% Complete, ' % (sub['percent'])
        color = 'yellow'
    if sub['hi']: label += 'HI, '
    if sub['corrected']: label += 'Corrected, '
    if sub['hd']: label += 'HD, '
    if not label.endswith('('):
        label = label[:-2] + ')'
    else:
        label = label[:-4]
    label = '[COLOR %s]%s[/COLOR]' % (color, label)
    return label

def format_source_label(item):
    label = item['class'].format_source_label(item)
    label = '[%s] %s' % (item['class'].get_name(), label)
    if kodi.get_setting('show_debrid') == 'true' and 'debrid' in item and item['debrid']:
        label = '[COLOR green]%s[/COLOR]' % (label)
    if 'debrid' in item and item['debrid']:
        label += ' (%s)' % (', '.join(item['debrid']))
    item['label'] = label
    return label
    
def srt_indicators_enabled():
    return (kodi.get_setting('enable-subtitles') == 'true' and (kodi.get_setting('subtitle-indicator') == 'true'))

def srt_download_enabled():
    return (kodi.get_setting('enable-subtitles') == 'true' and (kodi.get_setting('subtitle-download') == 'true'))

def srt_show_enabled():
    return (kodi.get_setting('enable-subtitles') == 'true' and (kodi.get_setting('subtitle-show') == 'true'))

def format_episode_label(label, season, episode, srts):
    req_hi = kodi.get_setting('subtitle-hi') == 'true'
    req_hd = kodi.get_setting('subtitle-hd') == 'true'
    color = 'red'
    percent = 0
    hi = None
    hd = None
    corrected = None

    for srt in srts:
        if str(season) == srt['season'] and str(episode) == srt['episode']:
            if not req_hi or srt['hi']:
                if not req_hd or srt['hd']:
                    if srt['completed']:
                        color = 'green'
                        if not hi: hi = srt['hi']
                        if not hd: hd = srt['hd']
                        if not corrected: corrected = srt['corrected']
                    elif color != 'green':
                        color = 'yellow'
                        if float(srt['percent']) > percent:
                            if not hi: hi = srt['hi']
                            if not hd: hd = srt['hd']
                            if not corrected: corrected = srt['corrected']
                            percent = srt['percent']

    if color != 'red':
        label += ' [COLOR %s](SRT: ' % (color)
        if color == 'yellow':
            label += ' %s%%, ' % (percent)
        if hi: label += 'HI, '
        if hd: label += 'HD, '
        if corrected: label += 'Corrected, '
        label = label[:-2]
        label += ')[/COLOR]'
    return label

def get_force_title_list():
    filter_str = kodi.get_setting('force_title_match')
    filter_list = filter_str.split('|') if filter_str else []
    return filter_list

def get_progress_skip_list():
    filter_str = kodi.get_setting('progress_skip_cache')
    filter_list = filter_str.split('|') if filter_str else []
    return filter_list

def get_force_progress_list():
    filter_str = kodi.get_setting('force_include_progress')
    filter_list = filter_str.split('|') if filter_str else []
    return filter_list

def record_failures(fails, counts=None):
    if counts is None: counts = {}

    for name in fails:
        setting = '%s_last_results' % (name)
        # remove timeouts from counts so they aren't double counted
        if name in counts: del counts[name]
        if int(kodi.get_setting(setting)) > -1:
            accumulate_setting(setting, 5)
    
    for name in counts:
        setting = '%s_last_results' % (name)
        if counts[name]:
            kodi.set_setting(setting, '0')
        elif int(kodi.get_setting(setting)) > -1:
            accumulate_setting(setting)

def do_disable_check():
    auto_disable = kodi.get_setting('auto-disable')
    disable_limit = int(kodi.get_setting('disable-limit'))
    for cls in relevant_scrapers():
        setting = '%s_last_results' % (cls.get_name())
        fails = kodi.get_setting(setting)
        fails = int(fails) if fails else 0
        if fails >= disable_limit:
            if auto_disable == DISABLE_SETTINGS.ON:
                kodi.set_setting('%s-enable' % (cls.get_name()), 'false')
                kodi.notify(msg='[COLOR blue]%s[/COLOR] %s' % (cls.get_name(), i18n('scraper_disabled')), duration=5000)
                kodi.set_setting(setting, '0')
            elif auto_disable == DISABLE_SETTINGS.PROMPT:
                dialog = xbmcgui.Dialog()
                line1 = i18n('disable_line1') % (cls.get_name(), fails)
                line2 = i18n('disable_line2')
                line3 = i18n('disable_line3')
                ret = dialog.yesno('SALTS', line1, line2, line3, i18n('keep_enabled'), i18n('disable_it'))
                if ret:
                    kodi.set_setting('%s-enable' % (cls.get_name()), 'false')
                    kodi.set_setting(setting, '0')
                else:
                    kodi.set_setting(setting, '-1')

def menu_on(menu):
    return kodi.get_setting('show_%s' % (menu)) == 'true'

def accumulate_setting(setting, addend=1):
    cur_value = kodi.get_setting(setting)
    cur_value = int(cur_value) if cur_value else 0
    kodi.set_setting(setting, cur_value + addend)

def show_requires_source(trakt_id):
    show_str = kodi.get_setting('exists_list')
    show_list = show_str.split('|')
    return str(trakt_id) in show_list

def keep_search(section, search_text):
    head = int(kodi.get_setting('%s_search_head' % (section)))
    new_head = (head + 1) % SEARCH_HISTORY
    log_utils.log('Setting %s to %s' % (new_head, search_text), log_utils.LOGDEBUG)
    db_connection.set_setting('%s_search_%s' % (section, new_head), search_text)
    kodi.set_setting('%s_search_head' % (section), str(new_head))

def bookmark_exists(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
        return bookmark is not None
    else:
        return db_connection.bookmark_exists(trakt_id, season, episode)

# returns true if user chooses to resume, else false
def get_resume_choice(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        resume_point = '%s%%' % (trakt_api.get_bookmark(trakt_id, season, episode))
        header = i18n('trakt_bookmark_exists')
    else:
        resume_point = format_time(db_connection.get_bookmark(trakt_id, season, episode))
        header = i18n('local_bookmark_exists')
    question = i18n('resume_from') % (resume_point)
    return xbmcgui.Dialog().yesno(header, question, '', '', i18n('start_from_beginning'), i18n('resume')) == 1

def get_bookmark(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
    else:
        bookmark = db_connection.get_bookmark(trakt_id, season, episode)
    return bookmark

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)

def download_media(url, path, file_name):
    try:
        progress = int(kodi.get_setting('down_progress'))
        request = urllib2.Request(url)
        request.add_header('User-Agent', USER_AGENT)
        request.add_unredirected_header('Host', request.get_host())
        response = urllib2.urlopen(request)

        content_length = 0
        if 'Content-Length' in response.info():
            content_length = int(response.info()['Content-Length'])

        file_name = file_name.replace('.strm', get_extension(url, response))
        full_path = os.path.join(path, file_name)
        log_utils.log('Downloading: %s -> %s' % (url, full_path), log_utils.LOGDEBUG)

        path = xbmc.makeLegalFilename(path)
        if not xbmcvfs.exists(path):
            try:
                try: xbmcvfs.mkdirs(path)
                except: os.mkdir(path)
            except Exception as e:
                raise Exception(i18n('failed_create_dir'))

        file_desc = xbmcvfs.File(full_path, 'w')
        total_len = 0
        if progress:
            if progress == PROGRESS.WINDOW:
                dialog = xbmcgui.DialogProgress()
            else:
                dialog = xbmcgui.DialogProgressBG()

            dialog.create('Stream All The Sources', i18n('downloading') % (file_name))
            dialog.update(0)
        while True:
            data = response.read(CHUNK_SIZE)
            if not data:
                break

            if progress == PROGRESS.WINDOW and dialog.iscanceled():
                break

            total_len += len(data)
            if not file_desc.write(data):
                raise Exception('failed_write_file')

            percent_progress = (total_len) * 100 / content_length if content_length > 0 else 0
            log_utils.log('Position : %s / %s = %s%%' % (total_len, content_length, percent_progress), log_utils.LOGDEBUG)
            if progress == PROGRESS.WINDOW:
                dialog.update(percent_progress)
            elif progress == PROGRESS.BACKGROUND:
                dialog.update(percent_progress, 'Stream All The Sources')
        else:
            kodi.notify(msg=i18n('download_complete') % (file_name), duration=5000)
            log_utils.log('Download Complete: %s -> %s' % (url, full_path), log_utils.LOGDEBUG)

        file_desc.close()
        if progress:
            dialog.close()

    except Exception as e:
        log_utils.log('Error (%s) during download: %s -> %s' % (str(e), url, file_name), log_utils.LOGERROR)
        kodi.notify(msg=i18n('download_error') % (str(e), file_name), duration=5000)

def get_extension(url, response):
    filename = url2name(url)
    if 'Content-Disposition' in response.info():
        cd_list = response.info()['Content-Disposition'].split('filename=')
        if len(cd_list) > 1:
            filename = cd_list[-1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
    elif response.url != url:
        filename = url2name(response.url)
    ext = os.path.splitext(filename)[1]
    if not ext: ext = DEFAULT_EXT
    return ext

def url2name(url):
    return os.path.basename(urllib.unquote(urlparse.urlsplit(url)[2]))

def sort_progress(episodes, sort_order):
    if sort_order == TRAKT_SORT.TITLE:
        return sorted(episodes, key=lambda x: title_key(x['show']['title']))
    elif sort_order == TRAKT_SORT.ACTIVITY:
        return sorted(episodes, key=lambda x: iso_2_utc(x['last_watched_at']), reverse=True)
    elif sort_order == TRAKT_SORT.LEAST_COMPLETED:
        return sorted(episodes, key=lambda x: (x['percent_completed'], x['completed']))
    elif sort_order == TRAKT_SORT.MOST_COMPLETED:
        return sorted(episodes, key=lambda x: (x['percent_completed'], x['completed']), reverse=True)
    elif sort_order == TRAKT_SORT.PREVIOUSLY_AIRED:
        return sorted(episodes, key=lambda x: iso_2_utc(x['episode']['first_aired']))
    elif sort_order == TRAKT_SORT.RECENTLY_AIRED:
        return sorted(episodes, key=lambda x: iso_2_utc(x['episode']['first_aired']), reverse=True)
    else:  # default sort set to activity
        return sorted(episodes, key=lambda x: x['last_watched_at'], reverse=True)

def title_key(title):
    temp = title.upper()
    if temp.startswith('THE '):
        offset = 4
    elif temp.startswith('A '):
        offset = 2
    elif temp.startswith('AN '):
        offset = 3
    else:
        offset = 0
    return title[offset:]
    
def make_progress_msg(video_type, title, year, season, episode):
    progress_msg = '%s: %s' % (video_type, title)
    if year: progress_msg += ' (%s)' % (year)
    if video_type == VIDEO_TYPES.EPISODE:
        progress_msg += ' - S%02dE%02d' % (int(season), int(episode))
    return progress_msg

def from_playlist():
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    if pl.size() > 0:
        li = pl[pl.getposition()]
        plugin_url = 'plugin://%s/' % (kodi.get_id())
        if li.getfilename().lower().startswith(plugin_url):
            log_utils.log('Playing SALTS item from playlist |%s|%s|%s|' % (pl.getposition(), li.getfilename(), plugin_url), log_utils.LOGDEBUG)
            return True
    
    return False

def reset_base_url():
    xml_path = os.path.join(kodi.get_path(), 'resources', 'settings.xml')
    tree = ET.parse(xml_path)
    for category in tree.getroot().findall('category'):
        if category.get('label').startswith('Scrapers '):
            for setting in category.findall('setting'):
                if setting.get('id').endswith('-base_url'):
                    log_utils.log('Resetting: %s -> %s' % (setting.get('id'), setting.get('default')), xbmc.LOGDEBUG)
                    kodi.set_setting(setting.get('id'), setting.get('default'))
