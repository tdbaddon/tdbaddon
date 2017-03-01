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
import os
import re
import urllib
import urlparse
import time
import xbmcvfs
import kodi
import log_utils  # @UnusedImport
import utils
import dom_parser
from salts_lib import scraper_utils
from salts_lib.utils2 import i18n
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib import gui_utils
import scraper

XHR = {'X-Requested-With': 'XMLHttpRequest'}
SEARCH_TYPES = {VIDEO_TYPES.MOVIE: 'movies', VIDEO_TYPES.TVSHOW: 'series'}

BASE_URL = 'http://torba.se'
SEARCH_URL = '/%s/autocomplete'

BASE_URL2 = 'https://streamtorrent.tv'
TOR_URL = BASE_URL2 + '/api/torrent/%s.json'
PL_URL = BASE_URL2 + '/api/torrent/%s/%s.m3u8?json=true'
OAUTH_GET_URL = BASE_URL2 + '/api/oauth/client'
OAUTH_CRED_URL = BASE_URL2 + '/api/oauth/credentials?device_code=%s'
OAUTH_TOKEN_URL = BASE_URL2 + '/api/oauth/token'

M3U8_PATH = os.path.join(kodi.translate_path(kodi.get_profile()), 'torbase.m3u8')
M3U8_TEMPLATE = [
    '#EXTM3U',
    '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",DEFAULT=YES,AUTOSELECT=YES,NAME="Stream 1",URI="{audio_stream}"',
    '',
    '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=0,NAME="{stream_name}",AUDIO="audio"',
    '{video_stream}']
                  

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    auth_url = False

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'torba.se'

    def resolve_link(self, link):
        try:
            xbmcvfs.delete(M3U8_PATH)
            query = urlparse.parse_qs(link)
            query = dict([(key, query[key][0]) if query[key] else (key, '') for key in query])
            if 'vid_id' in query and 'stream_id' in query and 'height' in query:
                auth_url = PL_URL % (query['vid_id'], query['stream_id'])
                result = self.__get_playlist_with_token(auth_url)
                if not result:
                    if int(query['height']) > 720:
                        if self.auth_torba():
                            result = self.__get_playlist_with_token(auth_url)
                    else:
                        result = self.__authorize_ip(auth_url)
                
                if result:
                    key = '%sp' % (query['height'])
                    if key in result:
                        if 'audio' in result:
                            streams = {'audio_stream': result['audio'], 'stream_name': key, 'video_stream': result[key]}
                            f = xbmcvfs.File(M3U8_PATH, 'w')
                            for line in M3U8_TEMPLATE:
                                line = line.format(**streams)
                                f.write(line + '\n')
                            return M3U8_PATH
                        else:
                            return result[key]
        except Exception as e:
            log_utils.log('Failure during torba resolver: %s' % (e), log_utils.LOGWARNING)

    # try to get the playlist using the token, try to refresh the token if it fails
    # reset all oauth params if the refresh fails
    def __get_playlist_with_token(self, pl_url):
        result = {}
        name = self.get_name()
        token = kodi.get_setting('%s-token' % (name))
        if token:
            authorized, result = self.__use_token(pl_url, token)
            if not authorized:
                client_id = kodi.get_setting('%s-client_id' % (name))
                client_secret = kodi.get_setting('%s-client_secret' % (name))
                refresh_token = kodi.get_setting('%s-refresh' % (name))
                if client_id and client_secret and refresh_token:
                    token = self.__get_token(client_id, client_secret, refresh_token)
                    if token:
                        authorized, result = self.__use_token(pl_url, token)
                    else:
                        self.reset_auth()
                    
        return result
    
    def reset_auth(self):
        name = self.get_name()
        kodi.set_setting('%s-client_id' % (name), '')
        kodi.set_setting('%s-client_secret' % (name), '')
        kodi.set_setting('%s-token' % (name), '')
        kodi.set_setting('%s-refresh' % (name), '')
        
    # try to use the oauth token to get a playlist
    def __use_token(self, pl_url, token):
        pl_url += '&token=%s' % (token)
        return self.check_auth2(pl_url)
        
    # do ip whitelist authorization
    def __authorize_ip(self, auth_url):
        authorized, response = self.check_auth2(auth_url)
        if authorized:
            return response
        else:
            if 'url' in response:
                self.auth_url = auth_url
                return gui_utils.do_ip_auth(self, response['url'], response.get('qrcode'))
            else:
                log_utils.log('Unusable JSON from Torba: %s' % (response), log_utils.LOGWARNING)
                return False
    
    def check_auth2(self, auth_url):
        js_data = scraper_utils.parse_json(self._http_get(auth_url, cache_limit=0), auth_url)
        if not js_data or 'url' in js_data:
            authorized = False
        else:
            authorized = True
        return authorized, js_data
        
    def check_auth(self):
        if not self.auth_url:
            return True, None
        
        return self.check_auth2(self.auth_url)
    
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            vid_link = dom_parser.parse_dom(html, 'a', {'class': '[^"]*video-play[^"]*'}, 'href')
            if vid_link:
                i = vid_link[0].rfind('/')
                if i > -1:
                    vid_id = vid_link[0][i + 1:]
                    sources = self.__get_streams(vid_id)
                    for height in sources:
                        stream_url = urllib.urlencode({'height': height, 'stream_id': sources[height], 'vid_id': vid_id})
                        quality = scraper_utils.height_get_quality(height)
                        hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                        hosters.append(hoster)
                
        return hosters

    def __get_streams(self, vid_id):
        sources = {}
        tor_url = TOR_URL % (vid_id)
        html = self._http_get(tor_url, cache_limit=.5)
        js_data = scraper_utils.parse_json(html, tor_url)
        if 'files' in js_data:
            for file_info in js_data['files']:
                if 'streams' in file_info and file_info['streams']:
                    for stream in file_info['streams']:
                        sources[stream['height']] = file_info['_id']
        return sources
    
    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=24)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'season-list'})
        if fragment:
            match = re.search('href="([^"]+)[^>]+>\s*season\s+%s\s*<' % (video.season), fragment[0], re.I)
            if match:
                season_url = match.group(1)
                episode_pattern = 'href="([^"]*%s/%s/%s)"' % (show_url, video.season, video.episode)
                title_pattern = 'href="(?P<url>[^"]+)"[^>]*>\s*<div class="series-item-title">(?P<title>[^<]+)'
                return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        search_url = search_url % (SEARCH_TYPES[video_type])
        params = {'order': 'relevance', 'title': title}
        html = self._http_get(search_url, params=params, headers=XHR, cache_limit=1)
        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            if 'title' in item and 'link' in item:
                match_title = item['title']
                match_url = item['link']
                match_year = str(item.get('year', ''))
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-get_token" label="    %s" type="action" action="RunPlugin(plugin://plugin.video.salts/?mode=auth_torba)" visible="eq(-3,true)"/>'
                        % (name, i18n('torba_auth')))
        settings.append('         <setting id="%s-reset_token" label="    %s" type="action" action="RunPlugin(plugin://plugin.video.salts/?mode=reset_torba)" visible="eq(-4,true)"/>'
                        % (name, i18n('reset_torba')))
        settings.append('         <setting id="%s-token" type="text" default="" visible="false"/>' % (name))
        settings.append('         <setting id="%s-refresh" type="text" default="" visible="false"/>' % (name))
        settings.append('         <setting id="%s-client_id" type="text" default="" visible="false"/>' % (name))
        settings.append('         <setting id="%s-client_secret" type="text" default="" visible="false"/>' % (name))
        return settings

    def auth_torba(self):
        html = self._http_get(OAUTH_GET_URL, cache_limit=0)
        js_data = scraper_utils.parse_json(html, OAUTH_GET_URL)
        line1 = i18n('verification_url') % (js_data['verification_short_url'])
        line2 = i18n('login_prompt')
        countdown = int(utils.iso_2_utc(js_data['expires_in']) - time.time())
        interval = js_data['interval'] / 1000
        with kodi.CountdownDialog(i18n('torba_acct_auth'), line1=line1, line2=line2, countdown=countdown, interval=interval) as cd:
            result = cd.start(self.check_oauth, [js_data['device_code']])
        
        # cancelled
        if result is None: return
        return self.__get_token(result['client_id'], result['client_secret'], js_data['device_code'])
        
    def __get_token(self, client_id, client_secret, code):
        try:
            name = self.get_name()
            kodi.set_setting('%s-client_id' % (name), client_id)
            kodi.set_setting('%s-client_secret' % (name), client_secret)
            data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
            html = self._http_get(OAUTH_TOKEN_URL, data=data, cache_limit=0)
            if not html:
                return False
            
            js_data = scraper_utils.parse_json(html, OAUTH_TOKEN_URL)
            kodi.set_setting('%s-token' % (name), js_data['access_token'])
            kodi.set_setting('%s-refresh' % (name), js_data['refresh_token'])
            return js_data['access_token']
        except Exception as e:
            log_utils.log('Torba Authorization failed: %s' % (e), log_utils.LOGWARNING)
            return False
    
    def check_oauth(self, device_code):
        url = OAUTH_CRED_URL % (device_code)
        html = self._http_get(url, cache_limit=0)
        js_data = scraper_utils.parse_json(html, url) if html else {}
        return js_data
