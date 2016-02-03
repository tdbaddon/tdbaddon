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
import scraper
import re
import urlparse
from salts_lib import kodi
import urllib
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://streamallthis.is'

class Stream_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'streamallthis.is'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s ' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            # keep pulling till we find neither a /watch iframe nor a /watch href
            while True:
                match = re.search('iframe\s+src="(/watch[^"]+)', html)
                if match:
                    new_url = match.group(1)
                    url = urlparse.urljoin(self.base_url, new_url)
                    html = self._http_get(url, cache_limit=.5)
                else:
                    match = re.search("location.href='(/watch[^']+)", html)
                    if match:
                        new_url = match.group(1)
                        url = urlparse.urljoin(self.base_url, new_url)
                        html = self._http_get(url, cache_limit=.5)
                    else:
                        break

            # assume we must be on the mail.ru link now
            # TODO: Once mail.ru resolver is pushed, this code needs to be removed
            match = re.search("iframe\s+src='([^']+)", html)
            if match:
                new_url = match.group(1)
                html = self._http_get(new_url, cache_limit=.5)
                match = re.search('metadataUrl"\s*:\s*"([^"]+)', html)
                if match:
                    new_url = match.group(1)
                    html = self._http_get(new_url, cache_limit=.5)
                    js_data = self._parse_json(html, new_url)
                    if 'videos' in js_data:
                        for video in js_data['videos']:
                            stream_url = video['url'] + '|Cookie=%s' % (self.__get_stream_cookies())
                            hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'url': stream_url, 'quality': self.__set_quality(video['key'][:-1]), 'views': None, 'rating': None, 'direct': True}
                            hosters.append(hoster)
        return hosters

    def __get_stream_cookies(self):
        cj = self._set_cookies(self.base_url, {})
        cookies = []
        for cookie in cj:
            if 'mail.ru' in cookie.domain:
                cookies.append('%s=%s' % (cookie.name, cookie.value))
        return urllib.quote(';'.join(cookies))

    def __set_quality(self, height):
        height = int(height)
        if height >= 720:
            quality = QUALITIES.HD720
        elif height >= 480:
            quality = QUALITIES.HIGH
        else:
            quality = QUALITIES.MEDIUM
        return quality

    def get_url(self, video):
        return super(Stream_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+s%02de%02d\.html)"\s+class="la"' % (int(video.season), int(video.episode))
        return super(Stream_Scraper, self)._default_get_episode_url(show_url, video, episode_pattern, '')

    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/tv-shows-list.html')
        html = self._http_get(url, cache_limit=8)

        results = []
        norm_title = self._normalize_title(title)
        pattern = 'href="([^"]+)"\s+class="lc">\s*(.*?)\s*<'
        for match in re.finditer(pattern, html):
            url, match_title = match.groups()
            if norm_title in self._normalize_title(match_title):
                result = {'url': self._pathify_url(url), 'title': match_title, 'year': ''}
                results.append(result)

        return results
