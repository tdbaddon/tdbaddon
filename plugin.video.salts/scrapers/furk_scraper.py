"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import re
import urllib
import urlparse
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.kodi import i18n
import scraper
import xml.etree.ElementTree as ET
import xbmcgui

BASE_URL = 'http://www.furk.net'
SEARCH_URL = '/api/plugins/metasearch'
LOGIN_URL = '/api/login/login'
MIN_DURATION = 10 * 60 * 1000  # 10 minutes in milliseconds

class Furk_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))
        self.max_results = int(kodi.get_setting('%s-result_limit' % (self.get_name())))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Furk.net'

    def resolve_link(self, link):
        playlist = super(self.__class__, self)._http_get(link, cache_limit=.5)
        try:
            ns = '{http://xspf.org/ns/0/}'
            root = ET.fromstring(playlist)
            tracks = root.findall('.//%strack' % (ns))
            locations = []
            for track in tracks:
                duration = track.find('%sduration' % (ns)).text
                try: duration = int(duration)
                except: duration = 0
                if duration >= MIN_DURATION:
                    location = track.find('%slocation' % (ns)).text
                    locations.append({'duration': duration / 1000, 'url': location})

            if len(locations) > 1:
                result = xbmcgui.Dialog().select(i18n('choose_stream'), [self.__format_time(location['duration']) for location in locations])
                if result > -1:
                    return locations[result]['url']
            elif locations:
                return locations[0]['url']
        except Exception as e:
            log_utils.log('Failure during furk playlist parse: %s' % (e), log_utils.LOGWARNING)

    def __format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        if minutes > 60:
            hours, minutes = divmod(minutes, 60)
            return "%02dh:%02dm:%02ds" % (hours, minutes, seconds)
        else:
            return "00h:%02dm:%02ds" % (minutes, seconds)
        
    def format_source_label(self, item):
            label = '[%s] %s' % (item['quality'], item['host'])
            if 'size' in item:
                label += ' (%s)' % (item['size'])
            if 'extra' in item:
                label += ' [%s]' % (item['extra'])
            return label

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            params = urlparse.parse_qs(urlparse.urlparse(source_url).query)
            if 'title' in params:
                search_title = re.sub("[^A-Za-z0-9. ]", "", urllib.unquote_plus(params['title'][0]))
                query = search_title
                if video.video_type == VIDEO_TYPES.MOVIE:
                    if 'year' in params: query += ' %s' % (params['year'][0])
                else:
                    sxe = ''
                    if 'season' in params:
                        sxe = 'S%02d' % (int(params['season'][0]))
                    if 'episode' in params:
                        sxe += 'E%02d' % (int(params['episode'][0]))
                    if sxe: query = '%s %s' % (query, sxe)
                query_url = '/search?query=%s' % (query)
                hosters = self.__get_links(query_url, video)
                if not hosters and video.video_type == VIDEO_TYPES.EPISODE and params['air_date'][0]:
                    query = urllib.quote_plus('%s %s' % (search_title, params['air_date'][0].replace('-', '.')))
                    query_url = '/search?query=%s' % (query)
                    hosters = self.__get_links(query_url, video)

        return hosters
    
    def __get_links(self, url, video):
        hosters = []
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        query = self.__translate_search(url)
        result = self._http_get(search_url, data=query, allow_redirect=False, cache_limit=.5)
        if 'files' in result:
            for item in result['files']:
                checks = [False] * 6
                if 'type' not in item or item['type'].upper() != 'VIDEO': checks[0] = True
                if 'is_ready' in item and item['is_ready'] != '1': checks[1] = True
                if 'av_result' in item and item['av_result'] in ['warning', 'infected']: checks[2] = True
                if 'video_info' not in item: checks[3] = True
                if 'video_info' in item and item['video_info'] and not re.search('#0:(?:0|1)(?:\(eng\)|\(und\))?:\s*Audio:', item['video_info']): checks[4] = True
                if video.video_type == VIDEO_TYPES.EPISODE:
                    sxe = '[. ][Ss]%02d[Ee]%02d[. ]' % (int(video.season), int(video.episode))
                    if not re.search(sxe, item['name']):
                        if video.ep_airdate:
                            airdate_pattern = '[. ]%s[. ]%02d[. ]%02d[. ]' % (video.ep_airdate.year, video.ep_airdate.month, video.ep_airdate.day)
                            if not re.search(airdate_pattern, item['name']): checks[5] = True
                    
                if any(checks):
                    log_utils.log('Furk.net result excluded: %s - |%s|' % (checks, item['name']), log_utils.LOGDEBUG)
                    continue
                
                match = re.search('(\d{3,})\s?x\s?(\d{3,})', item['video_info'])
                if match:
                    width, _ = match.groups()
                    quality = scraper_utils.width_get_quality(width)
                else:
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        _, _, height, _ = scraper_utils.parse_movie_link(item['name'])
                        quality = scraper_utils.height_get_quality(height)
                    elif video.video_type == VIDEO_TYPES.EPISODE:
                        _, _, _, height, _ = scraper_utils.parse_episode_link(item['name'])
                        if int(height) > -1:
                            quality = scraper_utils.height_get_quality(height)
                        else:
                            quality = QUALITIES.HIGH
                    else:
                        quality = QUALITIES.HIGH
                    
                if 'url_pls' in item:
                    stream_url = item['url_pls']
                    host = self._get_direct_hostname(stream_url)
                    hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
                    hoster['size'] = scraper_utils.format_size(int(item['size']), 'B')
                    hoster['extra'] = item['name']
                    hosters.append(hoster)
                else:
                    log_utils.log('Furk.net result skipped - no playlist: |%s|' % (json.dumps(item)), log_utils.LOGDEBUG)
                    
        return hosters
    
    def get_url(self, video):
        url = None
        self.create_db_connection()
        result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            if video.video_type == VIDEO_TYPES.MOVIE:
                query = 'title=%s&year=%s' % (urllib.quote_plus(video.title), video.year)
            else:
                query = 'title=%s&season=%s&episode=%s&air_date=%s' % (urllib.quote_plus(video.title), video.season, video.episode, video.ep_airdate)
            url = '/search?%s' % (query)
            self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    def search(self, video_type, title, year, season=''):
        return []

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-4,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('password')))
        settings.append('         <setting id="%s-result_limit" label="     %s" type="slider" default="10" range="10,100" option="int" visible="eq(-6,true)"/>' % (name, i18n('result_limit')))
        return settings

    def _http_get(self, url, data=None, retry=True, allow_redirect=True, cache_limit=8):
        if not self.username or not self.password:
            return {}
        
        js_result = {}
        result = super(self.__class__, self)._http_get(url, data=data, allow_redirect=allow_redirect, cache_limit=cache_limit)
        if result:
            try:
                js_result = json.loads(result)
            except ValueError:
                if 'msg_key=session_invalid' in result:
                    log_utils.log('Logging in for url (%s) (Session Expired)' % (url), log_utils.LOGDEBUG)
                    self.__login()
                    js_result = self._http_get(url, data=data, retry=False, allow_redirect=allow_redirect, cache_limit=0)
                else:
                    log_utils.log('Invalid JSON returned: %s: %s' % (url, result), log_utils.LOGWARNING)
                    js_result = {}
            else:
                if js_result['status'] == 'error':
                    if retry and js_result['error'] == 'access denied':
                        log_utils.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
                        self.__login()
                        js_result = self._http_get(url, data=data, retry=False, allow_redirect=allow_redirect, cache_limit=0)
                    else:
                        log_utils.log('Error received from furk.net (%s)' % (js_result['error']), log_utils.LOGWARNING)
                        js_result = {}
            
        return js_result
        
    def __login(self):
        url = urlparse.urljoin(self.base_url, LOGIN_URL)
        data = {'login': self.username, 'pwd': self.password}
        result = self._http_get(url, data=data, cache_limit=0)
        if result['status'] != 'ok':
            raise Exception('furk.net login failed: %s' % (result.get('error', 'Unknown Error')))
    
    def __translate_search(self, url):
        query = {'sort': 'relevance', 'filter': 'all', 'moderated': 'yes', 'offset': 0, 'limit': self.max_results, 'match': 'all'}
        query['q'] = urlparse.parse_qs(urlparse.urlparse(url).query)['query'][0]
        return query
