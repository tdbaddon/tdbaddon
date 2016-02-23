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
import base64
import re
import time
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'http://www.moviesplanet.is'
GK_KEY = base64.urlsafe_b64decode('MllVcmlZQmhTM2swYU9BY0lmTzQ=')
QUALITY_MAP = {'HD': QUALITIES.HD720}
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class MoviesPlanet_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MoviesPlanet'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        stream_urls = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            for match in re.finditer("embeds\[(\d+)\]\s*=\s*'([^']+)", html):
                match = re.search('src="([^"]+)', match.group(2))
                if match:
                    iframe_url = match.group(1)
                    if 'play-en.php' in iframe_url:
                        match = re.search('id=([^"&]+)', iframe_url)
                        if match:
                            proxy_link = match.group(1)
                            proxy_link = proxy_link.split('*', 1)[-1]
                            picasa_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY, proxy_link)
                            stream_urls += self._parse_google(picasa_url)
                    else:
                        html = self._http_get(iframe_url, cache_limit=0)
                        match = re.search('sources\s*:\s*\[(.*?)\]', html, re.DOTALL)
                        if match:
                            for match in re.finditer('''['"]*file['"]*\s*:\s*['"]*([^'"]+).*?['"]*label['"]*\s*:\s*['"]*([^'"]+)''', match.group(1), re.DOTALL):
                                stream_url, label = match.groups()
                                if 'download.php' in stream_url:
                                    redir_html = self._http_get(stream_url, allow_redirect=False, cache_limit=0)
                                    if stream_url.startswith('http'): stream_url = redir_html
                                stream_urls.append(stream_url)
                
        for stream_url in list(set(stream_urls)):
            host = self._get_direct_hostname(stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = QUALITY_MAP.get(label, QUALITIES.HIGH)
            stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
            sources.append(source)

        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/ajax/search.php')
        timestamp = int(time.time() * 1000)
        query = {'q': title, 'limit': '100', 'timestamp': timestamp, 'verifiedCheck': ''}
        html = self._http_get(search_url, data=query, headers=XHR, cache_limit=1)
        if video_type in [VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE]:
            media_type = 'TV SHOW'
        else:
            media_type = 'MOVIE'

        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            if item['meta'].upper().startswith(media_type):
                result = {'title': item['title'], 'url': scraper_utils.pathify_url(item['permalink']), 'year': ''}
                results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/season/%s/episode/%s/?)"' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-4,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, data=None, headers=None, allow_redirect=True, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = self._cached_http_get(url, self.base_url, self.timeout, data=data, headers=headers, allow_redirect=allow_redirect, cache_limit=cache_limit)
        if re.search('Please Register or Login', html, re.I):
            log_utils.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = self._cached_http_get(url, self.base_url, self.timeout, data=data, headers=headers, allow_redirect=allow_redirect, cache_limit=0)
        return html

    def __login(self):
        url = urlparse.urljoin(self.base_url, '/login')
        data = {'username': self.username, 'password': self.password, 'action': 'login'}
        html = self._cached_http_get(url, self.base_url, self.timeout, data=data, headers=XHR, cache_limit=0)
        if 'incorrect login' in html.lower():
            raise Exception('moviesplanet login failed')
