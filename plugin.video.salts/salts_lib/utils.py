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
import time
import _strptime
import datetime
import xbmc
import xbmcgui
import log_utils
import kodi
import utils2
from constants import *
from trakt_api import Trakt_API
from db_utils import DB_Connection
import threading
from scrapers import *  # import all scrapers into this namespace

_db_connection = None
last_check = datetime.datetime.fromtimestamp(0)
TOKEN = kodi.get_setting('trakt_oauth_token')
use_https = kodi.get_setting('use_https') == 'true'
trakt_timeout = int(kodi.get_setting('trakt_timeout'))
list_size = int(kodi.get_setting('list_size'))
trakt_api = Trakt_API(TOKEN, use_https, list_size, trakt_timeout)

# delay db_connection until needed to force db errors during recovery try: block
def _get_db_connection():
    global _db_connection
    if _db_connection is None:
        _db_connection = DB_Connection()
    return _db_connection
    
def choose_list(username=None):
    lists = trakt_api.get_lists(username)
    if username is None: lists.insert(0, {'name': 'watchlist', 'ids': {'slug': WATCHLIST_SLUG}})
    if lists:
        dialog = xbmcgui.Dialog()
        index = dialog.select(utils2.i18n('pick_a_list'), [list_data['name'] for list_data in lists])
        if index > -1:
            return lists[index]['ids']['slug']
    else:
        kodi.notify(msg=utils2.i18n('no_lists_for_user') % (username), duration=5000)

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
    if 'trailer' in item and item['trailer']: info['trailer'] = utils2.make_trailer(item['trailer'])
    if 'first_aired' in item: info['aired'] = info['premiered'] = utils2.make_air_date(item['first_aired'])
    info.update(utils2.make_ids(item))

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
    if 'trailer' in show and show['trailer']: info['trailer'] = utils2.make_trailer(show['trailer'])
    info.update(utils2.make_ids(show))
    info.update(utils2.make_people(people))
    return info

def update_url(video_type, title, year, source, old_url, new_url, season, episode):
    log_utils.log('Setting Url: |%s|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title.decode('utf-8').encode('ascii', 'xmlcharrefreplace'), year, source, old_url, new_url, season, episode), log_utils.LOGDEBUG)
    db_connection = _get_db_connection()
    if new_url:
        db_connection.set_related_url(video_type, title, year, source, new_url, season, episode)
    else:
        db_connection.clear_related_url(video_type, title, year, source, season, episode)

    # clear all episode local urls if tvshow url changes
    if video_type == VIDEO_TYPES.TVSHOW and new_url != old_url:
        db_connection.clear_related_url(VIDEO_TYPES.EPISODE, title, year, source)

def make_source_sort_key():
    sso = kodi.get_setting('source_sort_order')
    # migrate sso to kodi setting
    if not sso:
        db_connection = _get_db_connection()
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

def parallel_get_progress(q, trakt_id, cached, cache_limit):
    worker = threading.current_thread()
    log_utils.log('Worker: %s (%s) for %s progress' % (worker.name, worker, trakt_id), log_utils.LOGDEBUG)
    progress = trakt_api.get_show_progress(trakt_id, full=True, cached=cached, cache_limit=cache_limit)
    progress['trakt'] = trakt_id  # add in a hacked show_id to be used to match progress up to the show its for
    log_utils.log('Got progress for %s from %s' % (trakt_id, worker), log_utils.LOGDEBUG)
    q.put(progress)

# Run a task on startup. Settings and mode values must match task name
def do_startup_task(task):
    run_on_startup = kodi.get_setting('auto-%s' % task) == 'true' and kodi.get_setting('%s-during-startup' % task) == 'true'
    if run_on_startup and not xbmc.abortRequested:
        log_utils.log('Service: Running startup task [%s]' % (task))
        now = datetime.datetime.now()
        xbmc.executebuiltin('RunPlugin(plugin://%s/?mode=%s)' % (kodi.get_id(), task))
        _get_db_connection().set_setting('%s-last_run' % (task), now.strftime("%Y-%m-%d %H:%M:%S.%f"))

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
                    _get_db_connection().set_setting('%s-last_run' % task, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                else:
                    log_utils.log('Service: Playing... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)
            else:
                log_utils.log('Service: Scanning... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)

def get_next_run(task):
    # strptime mysteriously fails sometimes with TypeError; this is a hacky workaround
    # note, they aren't 100% equal as time.strptime loses fractional seconds but they are close enough
    try:
        last_run_string = _get_db_connection().get_setting(task + '-last_run')
        if not last_run_string: last_run_string = LONG_AGO
        last_run = datetime.datetime.strptime(last_run_string, "%Y-%m-%d %H:%M:%S.%f")
    except (TypeError, ImportError):
        last_run = datetime.datetime(*(time.strptime(last_run_string, '%Y-%m-%d %H:%M:%S.%f')[0:6]))
    interval = datetime.timedelta(hours=float(kodi.get_setting(task + '-interval')))
    return (last_run + interval)

def keep_search(section, search_text):
    head = int(kodi.get_setting('%s_search_head' % (section)))
    new_head = (head + 1) % SEARCH_HISTORY
    log_utils.log('Setting %s to %s' % (new_head, search_text), log_utils.LOGDEBUG)
    _get_db_connection().set_setting('%s_search_%s' % (section, new_head), search_text)
    kodi.set_setting('%s_search_head' % (section), str(new_head))

def bookmark_exists(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
        return bookmark is not None
    else:
        return _get_db_connection().bookmark_exists(trakt_id, season, episode)

# returns true if user chooses to resume, else false
def get_resume_choice(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        resume_point = '%s%%' % (trakt_api.get_bookmark(trakt_id, season, episode))
        header = utils2.i18n('trakt_bookmark_exists')
    else:
        resume_point = utils2.format_time(_get_db_connection().get_bookmark(trakt_id, season, episode))
        header = utils2.i18n('local_bookmark_exists')
    question = utils2.i18n('resume_from') % (resume_point)
    return xbmcgui.Dialog().yesno(header, question, '', '', utils2.i18n('start_from_beginning'), utils2.i18n('resume')) == 1

def get_bookmark(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
    else:
        bookmark = _get_db_connection().get_bookmark(trakt_id, season, episode)
    return bookmark

def relevant_scrapers(video_type=None, include_disabled=False, order_matters=False):
    classes = scraper.Scraper.__class__.__subclasses__(scraper.Scraper)
    classes += proxy.Proxy.__class__.__subclasses__(proxy.Proxy)
    relevant = []
    for cls in classes:
        if cls.get_name() and not cls.has_proxy() and (video_type is None or video_type in cls.provides()):
            if include_disabled or utils2.scraper_enabled(cls.get_name()):
                    relevant.append(cls)

    if order_matters:
        relevant.sort(key=get_source_sort_key)
    return relevant

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
                kodi.notify(msg='[COLOR blue]%s[/COLOR] %s' % (cls.get_name(), utils2.i18n('scraper_disabled')), duration=5000)
                kodi.set_setting(setting, '0')
            elif auto_disable == DISABLE_SETTINGS.PROMPT:
                dialog = xbmcgui.Dialog()
                line1 = utils2.i18n('disable_line1') % (cls.get_name(), fails)
                line2 = utils2.i18n('disable_line2')
                line3 = utils2.i18n('disable_line3')
                ret = dialog.yesno('SALTS', line1, line2, line3, utils2.i18n('keep_enabled'), utils2.i18n('disable_it'))
                if ret:
                    kodi.set_setting('%s-enable' % (cls.get_name()), 'false')
                    kodi.set_setting(setting, '0')
                else:
                    kodi.set_setting(setting, '-1')
