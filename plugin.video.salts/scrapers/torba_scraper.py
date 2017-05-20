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
import xbmcvfs
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib import gui_utils
import scraper

logger = log_utils.Logger.get_logger()

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
            query = scraper_utils.parse_query(link)
            auth_url = PL_URL % (query['vid_id'], query['stream_id'])
            result = self.__authorize_ip(auth_url)
            if not result: return
            key = '%sp' % (query['height'])
            if key not in result: return
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
            logger.log('Failure during torba resolver: %s' % (e), log_utils.LOGWARNING)

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
                logger.log('Unusable JSON from Torba: %s' % (response), log_utils.LOGWARNING)
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
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        vid_link = dom_parser2.parse_dom(html, 'a', {'class': 'video-play'}, req='href')
        if not vid_link: return hosters
        
        vid_id = vid_link[0].attrs['href'].split('/')[-1]
        for height, stream_id in self.__get_streams(vid_id).iteritems():
            stream_url = urllib.urlencode({'height': height, 'stream_id': stream_id, 'vid_id': vid_id})
            quality = scraper_utils.height_get_quality(height)
            hoster = {'multi-part': False, 'host': scraper_utils.get_direct_hostname(self, stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
            hosters.append(hoster)
                
        return hosters

    def __get_streams(self, vid_id):
        sources = {}
        tor_url = TOR_URL % (vid_id)
        html = self._http_get(tor_url, cache_limit=.5)
        js_data = scraper_utils.parse_json(html, tor_url)
        for file_info in js_data.get('files', []):
            for stream in file_info.get('streams', {}):
                sources[stream['height']] = file_info['_id']
        return sources
    
    def _get_episode_url(self, show_url, video):
        url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=24)
        fragment = dom_parser2.parse_dom(html, 'ul', {'class': 'season-list'})
        if not fragment: return

        match = re.search('href="([^"]+)[^>]+>\s*season\s+%s\s*<' % (video.season), fragment[0].content, re.I)
        if not match: return
        
        episode_pattern = 'href="([^"]*%s/%s/%s)"' % (show_url, video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+)"[^>]*>\s*<div class="series-item-title">(?P<title>[^<]+)'
        season_url = scraper_utils.urljoin(self.base_url, match.group(1))
        html = self._http_get(season_url, cache_limit=2)
        return self._default_get_episode_url(html, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, SEARCH_URL)
        search_url = search_url % (SEARCH_TYPES[video_type])
        params = {'order': 'relevance', 'title': title}
        html = self._http_get(search_url, params=params, headers=XHR, cache_limit=1)
        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            match_title = item.get('title')
            match_url = item.get('link')
            match_year = str(item.get('year', ''))
            if match_title and match_url and (not year or not match_year or year == match_year):
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
