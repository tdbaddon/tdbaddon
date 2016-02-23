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
import re
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'https://www.premiumize.me'
VIDEO_EXT = ['MKV', 'AVI', 'MP4']

class Premiumize_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Premiumize.me'

    def resolve_link(self, link):
        return link

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
            query = urlparse.parse_qs(source_url)
            if 'hash' in query:
                data = {'hash': query['hash'][0]}
                url = urlparse.urljoin(self.base_url, '/torrent/browse')
                js_data = self._http_get(url, data=data, cache_limit=1)
                if 'data' in js_data and 'content' in js_data['data']:
                    videos = self.__get_videos(js_data['data']['content'], video)
                    for video in videos:
                        host = self._get_direct_hostname(video['url'])
                        hoster = {'multi-part': False, 'class': self, 'views': None, 'url': video['url'], 'rating': None, 'host': host, 'quality': video['quality'], 'direct': True}
                        if 'size' in video: hoster['size'] = scraper_utils.format_size(video['size'])
                        if 'name' in video: hoster['extra'] = video['name']
                        hosters.append(hoster)
                         
        return hosters
    
    def __get_videos(self, contents, video):
        videos = []
        for key in contents:
            item = contents[key]
            if item['type'].lower() == 'dir':
                videos += self.__get_videos(item['children'], video)
            else:
                if item['ext'].upper() in VIDEO_EXT and int(item['size']) > (100 * 1024 * 1024):
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        _, _, height, _ = scraper_utils.parse_movie_link(item['name'])
                    else:
                        _, _, _, height, _ = scraper_utils.parse_episode_link(item['name'])
                    video = {'name': item['name'], 'size': item['size'], 'url': item['url'], 'quality': scraper_utils.height_get_quality(height)}
                    videos.append(video)
                    if item['stream'] is not None:
                        if int(height) > 720: height = 720
                        video = {'name': '(Transcode) %s' % (item['name']), 'url': item['stream'], 'quality': scraper_utils.height_get_quality(height)}
                        videos.append(video)
        return videos
    
    def get_url(self, video):
        url = None
        self.create_db_connection()
        result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url))
        else:
            if video.video_type == VIDEO_TYPES.MOVIE:
                results = self.search(video.video_type, video.title, video.year)
                if results:
                    url = results[0]['url']
                    self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url)
            else:
                url = self._get_episode_url(video)
                if url:
                    self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)

        return url

    def _get_episode_url(self, video):
        url = urlparse.urljoin(self.base_url, '/torrent/list')
        js_data = self._http_get(url, cache_limit=0)
        norm_title = scraper_utils.normalize_title(video.title)
        if 'torrents' in js_data:
            airdate_fallback = kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate
            show_title = ''
            if not scraper_utils.force_title(video):
                for item in js_data['torrents']:
                    sxe_pattern = '(.*?)[. ][Ss]%02d[Ee]%02d[. ]' % (int(video.season), int(video.episode))
                    match = re.search(sxe_pattern, item['name'])
                    if match:
                        show_title = match.group(1)
                    elif airdate_fallback:
                        airdate_pattern = '(.*?)[. ]%s[. ]%02d[. ]%02d[. ]' % (video.ep_airdate.year, video.ep_airdate.month, video.ep_airdate.day)
                        match = re.search(airdate_pattern, item['name'])
                        if match:
                            show_title = match.group(1)
                    
                    if show_title and norm_title in scraper_utils.normalize_title(show_title):
                        return 'hash=%s' % (item['hash'])
                
    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/torrent/list')
        js_data = self._http_get(url, cache_limit=0)
        norm_title = scraper_utils.normalize_title(title)
        results = []
        if 'torrents' in js_data:
            for item in js_data['torrents']:
                if re.search('[._ ]S\d+E\d+[._ ]', item['name']): continue  # skip episodes for movies
                match = re.search('(.*?)\(?(\d{4})\)?(.*)', item['name'])
                if match:
                    match_title, match_year, extra = match.groups()
                else:
                    match_title, match_year, extra = item['name'], '', ''
                match_title = match_title.strip()
                extra = extra.strip()
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result_title = match_title
                    if extra: result_title += ' [%s]' % (extra)
                    result = {'title': result_title, 'year': match_year, 'url': 'hash=%s' % (item['hash'])}
                    results.append(result)
        
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-4,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, data=None, retry=True, allow_redirect=True, cache_limit=8):
        if not self.username or not self.password:
            return {}
        
        if data is None: data = {}
        data.update({'customer_id': self.username, 'pin': self.password})
        result = super(Premiumize_Scraper, self)._http_get(url, data=data, allow_redirect=allow_redirect, cache_limit=cache_limit)
        js_result = scraper_utils.parse_json(result, url)
        if 'status' in js_result and js_result['status'] == 'error':
            log_utils.log('Error received from premiumize.me (%s)' % (js_result.get('message', 'Unknown Error')), log_utils.LOGWARNING)
            js_result = {}
            
        return js_result
