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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://watchinhd.io'
Q_MAP = {'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}

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
        return 'WatchInHD'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=8)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'playex'})
            if fragment:
                for stream_url in dom_parser.parse_dom(fragment[0], 'iframe', ret='src'):
                    if self._get_direct_hostname(stream_url) == 'gvideo':
                        links = self._parse_google(stream_url)
                        direct = True
                    else:
                        links = [stream_url]
                        direct = False

                    for link in links:
                        host = self._get_direct_hostname(stream_url)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(link)
                        else:
                            quality = QUALITIES.HIGH
                            host = urlparse.urlparse(stream_url).hostname
                        source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                        sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'result-item'}):
            match = dom_parser.parse_dom(item, 'div', {'class': 'title'})
            is_movie = dom_parser.parse_dom(item, 'span', {'class': 'movies'})
            if is_movie and match:
                match = match[0]
                match_url = dom_parser.parse_dom(match, 'a', ret='href')
                match_title = dom_parser.parse_dom(match, 'a')
                if match_url and match_title:
                    match_url = match_url[0]
                    match_title = match_title[0]
                    match_year = dom_parser.parse_dom(item, 'span', {'class': 'year'})
                    match_year = match_year[0] if match_year else ''
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results
