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

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://dizimag.co'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Dizimag_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizimag'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            # exit early if trailer
            if re.search('Şu an fragman*', html, re.I):
                return hosters
            
            match = re.search('''url\s*:\s*"([^"]+)"\s*,\s*data:\s*["'](id=\d+)''', html)
            if match:
                url, data = match.groups()
                url = urlparse.urljoin(self.base_url, url)
                result = self._http_get(url, data=data, headers=XHR, cache_limit=.5)
                for match in re.finditer('"videolink\d*"\s*:\s*"([^"]+)","videokalite\d*"\s*:\s*"?(\d+)p?', result):
                    stream_url, height = match.groups()
                    stream_url = stream_url.replace('\\/', '/')
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    else:
                        quality = scraper_utils.height_get_quality(height)
                        stream_url += '|User-Agent=%s&Referer=%s' % (scraper_utils.get_ua(), urllib.quote(page_url))

                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
        title_pattern = 'class="gizle".*?href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):
        html = self._http_get(self.base_url, cache_limit=8)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'fil'})
        norm_title = scraper_utils.normalize_title(title)
        if fragment:
            for match in re.finditer('href="([^"]+)"\s+title="([^"]+)', fragment[0]):
                url, match_title = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
