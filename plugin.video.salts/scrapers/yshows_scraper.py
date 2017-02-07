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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://yshow.me'
QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'yshows'

    def resolve_link(self, link):
        link_url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(link_url, cache_limit=.25)
        match = re.search('<iframe[^>]+src="([^"]+)', html, re.I)
        if match:
            return match.group(1)

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for tr in dom_parser.parse_dom(html, 'tr'):
                link = dom_parser.parse_dom(tr, 'a', ret='href')
                host = dom_parser.parse_dom(tr, 'a')
                q_str = dom_parser.parse_dom(tr, 'span')
                if link and host:
                    host = host[0]
                    link = link[0]
                    q_str = q_str[0] if q_str else ''
                    quality = scraper_utils.get_quality(video, host, QUALITY_MAP.get(q_str.upper(), QUALITIES.HIGH))
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': link, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'q': title}, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'col-sm-9'})
        if fragment:
            links = dom_parser.parse_dom(fragment[0], 'a', ret='href')
            titles = dom_parser.parse_dom(fragment[0], 'a')
            for match_url, match_title in zip(links, titles):
                match_title = re.sub('</?[^>]*>', '', match_title)
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)
        return results
