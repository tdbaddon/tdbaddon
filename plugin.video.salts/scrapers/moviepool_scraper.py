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
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://moviepool.net'
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
        return 'MoviePool'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = {}
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=8)
            iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
            if iframe_url:
                iframe_url = iframe_url[0]
                if 'cdn.moviepool.net' in iframe_url:
                    headers = {'Referer': page_url}
                    html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
                    sources = self._parse_sources_list(html)
                else:
                    sources[iframe_url] = {'quality': QUALITIES.HD720, 'direct': False}
                
            for source in sources:
                direct = sources[source]['direct']
                if direct:
                    host = self._get_direct_hostname(source)
                else:
                    host = urlparse.urlparse(source).hostname
                quality = sources[source]['quality']
                hoster = {'multi-part': False, 'url': source, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': '[^"]*listing-videos[^"]*'})
        if fragment:
            urls = dom_parser.parse_dom(fragment[0], 'a', ret='href')
            labels = dom_parser.parse_dom(fragment[0], 'a')
            for match_url, match_title_year in zip(urls, labels):
                match_title_year = re.sub('</?[^>]*>', '', match_title_year)
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
