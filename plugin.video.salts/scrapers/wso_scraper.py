# -*- coding: utf-8 -*-
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
import urllib
import urlparse

from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://watchseries-online.li'

class WSO_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'wso.ch'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=.5)
        match = re.search('''href=(?:\|")([^"']+)(?:"|')>Click Here to Play''', html)
        if match:
            return match.group(1)
        else:
            return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            pattern = 'class="[^"]*tdhost".*?href="([^"]+)">([^<]+)'
            for match in re.finditer(pattern, html, re.DOTALL):
                stream_url, host = match.groups()
                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/?s=%s&search=')
        url = url % (urllib.quote_plus(title))
        html = self._http_get(url, cache_limit=24)

        results = []
        for list_match in re.finditer('class="ddmcc"(.*?)</div>', html, re.DOTALL):
            list_frag = list_match.group(1)
            norm_title = scraper_utils.normalize_title(title)
            pattern = 'href="([^"]+)">([^<]+)'
            for match in re.finditer(pattern, list_frag):
                url, match_title = match.groups('')
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': ''}
                    results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = "href='([^']+)'>(?:[^<]*(?:[Ss]%02d[Ee]%02d |-\s*%s(?:[×xX]|&#215;)%s\s*-))" % (int(video.season), int(video.episode), video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)
