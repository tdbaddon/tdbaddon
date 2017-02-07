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

BASE_URL = 'http://moviezone.ch'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):  # @UnusedVariable
        self.timeout = 2  # manually set timeout for slow iframe calls
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieZone'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=8)
            sources = dom_parser.parse_dom(html, 'source', ret='src')
            iframes = dom_parser.parse_dom(html, 'iframe', {'class': 'movieframe'}, ret='src')
            headers = {'Referer': url}
            for iframe_url in iframes:
                html = self._http_get(iframe_url, headers=headers, allow_redirect=False, method='HEAD', cache_limit=0)
                if html.startswith('http'):
                    sources.append(html)
                else:
                    iframe_url = urlparse.urljoin(self.base_url, iframe_url)
                    html = self._http_get(iframe_url, headers=headers, cache_limit=1)
                    sources += dom_parser.parse_dom(html, 'source', ret='src')
                    iframes += dom_parser.parse_dom(html, 'iframe', ret='src')
            
            for source in sources:
                host = self._get_direct_hostname(source)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(source)
                    direct = True
                else:
                    quality = QUALITIES.HIGH
                    direct = False
                    host = urlparse.urlparse(source).hostname
                source = {'multi-part': False, 'url': source, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, read_error=True, cache_limit=16)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
            post_type = dom_parser.parse_dom(item, 'div', {'class': 'typepost'})
            if post_type and post_type[0] == 'tv': continue
            match = re.search('href="([^"]+)', item)
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'tt'})
            year_frag = dom_parser.parse_dom(item, 'span', {'class': 'year'})
            if match and match_title:
                url = match.group(1)
                match_title, match_year = scraper_utils.extra_year(match_title[0])
                if not match_year and year_frag:
                    match = re.search('(\d{4})', year_frag[0])
                    if match:
                        match_year = match.group(1)

                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)

        return results
